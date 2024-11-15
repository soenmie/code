import logging
import itertools
import json
import operator
import os
import tempfile
import stat
import subprocess

import gradio as gr
import requests

logging.basicConfig(level=logging.INFO)


def get_access_token(is_debug=False):
    url = os.environ.get('OAUTH_TOKEN_URL')

    if is_debug:
        params = {
            'grant_type': 'client_credentials',
            'client_id': os.environ.get('OFFLINE_AK'),
            'client_secret': os.environ.get('OFFLINE_SK')
        }
    else:
        params = {
            'grant_type': 'client_credentials',
            'client_id': os.environ.get('ONLINE_AK'),
            'client_secret': os.environ.get('ONLINE_SK'),
        }

    response = requests.get(url, params=params)
    response_json = response.json()

    access_token = response_json['access_token']
    return access_token


def iter_response(response):
    # 处理响应流
    data_id, last_byte = 0, b''
    for byte in response.iter_content(chunk_size=1):
        yield data_id, byte
        if last_byte == b'\n' and byte == b'\n':
            data_id += 1
        last_byte = byte


def execute_script(script_text):
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(script_text.encode('utf-8'))
        tmp_file_path = tmp_file.name

    os.chmod(tmp_file_path, os.stat(tmp_file_path).st_mode | stat.S_IEXEC)

    p = subprocess.Popen([tmp_file_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    output = ''
    for line in iter(p.stdout.readline, b''):
        output += line.decode('utf-8')

    p.stdout.close()
    p.wait()

    os.remove(tmp_file_path)
    return output


def predict(url, chatbot, history, system_info_text, is_debug, temperature, top_k, top_p, enable_tts, enable_vilg, enable_citation, append_newline):
    prompt, answer = chatbot[-1]

    if prompt.startswith('#!'):
        answer = execute_script(prompt)
        chatbot[-1] = (prompt, answer)
        history.append((prompt, answer))
        yield chatbot, history
        return

    if append_newline:
        prompt += '\n'
    if not answer:
        messages = []
        for user_history, assistant_history in history:
            messages += [
                {'role': 'user', 'content': user_history},
                {'role': 'assistant', 'content': assistant_history},
            ]

        messages += [{'role': 'user', 'content': prompt}]

        data = {
            'messages': messages,
            'stream': True,
        }
        if enable_tts:
            data['enable_tts'] = enable_tts
        if enable_vilg:
            data['enable_vilg'] = enable_vilg
        if enable_citation:
            data['enable_citation'] = enable_citation
        if system_info_text:
            data['system'] = system_info_text
        if temperature:
            data['temperature'] = float(temperature)
        if top_k:
            data['top_k'] = int(top_k)
        if top_p:
            data['top_p'] = float(top_p)
        logging.info('request_data: %s', json.dumps(data, ensure_ascii=False))

        # 将数据转换为JSON格式
        json_data = json.dumps(data)

        # 设置请求头，指定发送的是JSON数据
        headers = {'Content-Type': 'application/json'}
        access_token = get_access_token(is_debug=is_debug)
        for _ in range(3):
            try:
                # 发送 POST 请求
                response = requests.post(f'{url}?access_token={access_token}', data=json_data, headers=headers, stream=True)

                answer = ''

                for data_id, data_group in itertools.groupby(iter_response(response), operator.itemgetter(0)):
                    stream_data = json.loads(b''.join(data_chunk for _, data_chunk in data_group)[len(b'data:'):])
                    stream_result = stream_data['result']

                    answer += stream_result
                    chatbot[-1] = (prompt, answer)

                    yield chatbot, history
                logging.info('answer: %s', answer)
                break
            except:
                pass

    history.append((prompt, answer))
    yield chatbot, history


def clear_history():
    return [], []


def withdraw(input_text, chatbot, history):
    if not chatbot or not history:
        return gr.update(value=''), chatbot, history
    last_input, _ = history[-1]
    chatbot, history = chatbot[:-1], history[:-1]
    return gr.update(value=last_input), chatbot, history


def submit_preprocess(input_text, response_text, chatbot):
    chatbot.append((input_text, response_text))
    return gr.update(value=''), gr.update(value=''), chatbot


def get_input_components(block):
    input_components = []

    for component in block.children:
        if hasattr(component, 'children') and isinstance(component.children, list):
            input_components += get_input_components(component)
        else:
            input_components += [component]

    return input_components


def get_query_params(request: gr.Request):
    return dict(request.query_params)


def initialize_components(*args):
    (query_params, component_ids), component_values = args[:2], args[2:]
    params = json.loads(query_params.get('params', '{}'))
    return list(params.get(component_id, component_value) for component_id, component_value in zip(component_ids, component_values))


if __name__ == '__main__':
    with gr.Blocks(theme=gr.themes.Soft()) as demo:
        url_box = gr.Textbox(label='大模型url', value=os.environ.get('LLM_SERVING_URL'), elem_id='url')
        with gr.Row():
            is_debug_checkbox = gr.Checkbox(value=True, label='是否使用Debug环境', elem_id='is_debug')
            append_newline_checkbox = gr.Checkbox(label='是否结尾添加新行', elem_id='append_newline')
        with gr.Row():
            temperature_box = gr.Textbox(label='Temperature', elem_id='temperature')
            top_k_box = gr.Textbox(label='Top K', elem_id='top_k')
            top_p_box = gr.Textbox(label='Top P', elem_id='top_p')
        with gr.Row():
            enable_tts_checkbox = gr.Checkbox(value=False, label='enable_tts', elem_id='enable_tts')
            enable_vilg_checkbox = gr.Checkbox(value=True, label='enable_vilg', elem_id='enable_vilg')
            enable_citation_checkbox = gr.Checkbox(value=True, label='enable_citation', elem_id='enable_citation')
        chatbot = gr.Chatbot(height=400, show_copy_button=True, elem_id='chatbot')
        system_info_box = gr.TextArea(label='System Info', elem_id='system_info')
        with gr.Row():
            input_box = gr.TextArea(show_label=False, placeholder='输入', elem_id='input')
            response_box = gr.TextArea(show_label=False, placeholder='输出', elem_id='response')
        with gr.Row():
            submit_button = gr.Button("提交", interactive=True, variant="primary")
            undo_button = gr.Button("撤回", interactive=True)
            clear_button = gr.Button("重置对话", interactive=True)

        history = gr.State([])
        submit_button.click(
            submit_preprocess, [input_box, response_box, chatbot], [input_box, response_box, chatbot]
        ).then(
            predict, [url_box, chatbot, history, system_info_box, is_debug_checkbox, temperature_box, top_k_box, top_p_box, enable_tts_checkbox, enable_vilg_checkbox, enable_citation_checkbox, append_newline_checkbox], [chatbot, history]
        )

        undo_button.click(
            withdraw, [input_box, chatbot, history], [input_box, chatbot, history]
        )

        clear_button.click(
            clear_history, [], [chatbot, history]
        )

        input_components = get_input_components(demo)
        input_component_ids = gr.State([component.elem_id for component in input_components])
        query_params = gr.State({})
        demo.load(get_query_params, inputs=[], outputs=[query_params]).then(
            initialize_components,
            [query_params, input_component_ids] + input_components,
            input_components
        )

    demo.queue().launch(debug=False, server_name="0.0.0.0", server_port=8227, inbrowser=True)
