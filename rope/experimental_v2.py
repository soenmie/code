import numpy as np
import torch

from model import VectorRopeModel, apply_rotary_pos_emb


if __name__ == '__main__':
    # 设置 printoptions，threshold 参数为 float('inf') 以避免任何张量项的省略
    torch.set_printoptions(threshold=float('inf'))
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    e_range_start, e_range_end = 252, 263

    for eid in np.arange(e_range_start, e_range_end):
        torch.manual_seed(123)

        epochs = 1000
        dim = 64
        base = 200
        max_seq_len = eid

        print(f'eid: {eid}, max_seq_len: {max_seq_len}')
        with open('experimental_v2/eid_%03d.txt' % eid, mode='w') as f:
            model = VectorRopeModel(dim, max_seq_len, base, device)
            model.to(device)

            input_m, input_n = torch.meshgrid(torch.arange(max_seq_len, device=device), torch.arange(max_seq_len, device=device), indexing='ij')
            input_m = input_m.flatten()
            input_n = input_n.flatten()

            optimizer = torch.optim.SGD(params=model.parameters(), lr=0.001)

            for epoch in range(epochs):
                model.train()
                loss = -torch.sum(torch.sigmoid(model(input_m, input_n)))
                if (epoch + 1) % 10 == 0:
                    a, b = list(model.parameters())
                    B = apply_rotary_pos_emb(b.unsqueeze(0).expand(max_seq_len, -1), model.rotary_embedding)
                    cosine_of_angle_0 = torch.dot(a, b) / (torch.norm(a) * torch.norm(b))
                    cosine_of_angles = torch.einsum('i,bi -> b', a, B) / (torch.norm(a) * torch.norm(b))
                    cosine_of_angle_mean = torch.mean(cosine_of_angles)
                    cosine_of_angle_var = torch.var(cosine_of_angles)
                    print(f'epoch: {epoch}, loss: {loss}, cosine_of_angle_0: {cosine_of_angle_0}, cosine_of_angle_mean: {cosine_of_angle_mean}, cosine_of_angle_var: {cosine_of_angle_var}', file=f, flush=True)
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

            a, b = list(model.parameters())
            print('-' * 8 + 'a, b' + '-' * 8, file=f, flush=True)
            print(a, b, sep='\n', file=f, flush=True)
            print('-' * 8 + 'cosine_of_angle' + '-' * 8, file=f, flush=True)
            print(torch.dot(a, b) / (torch.norm(a) * torch.norm(b)), file=f, flush=True)
            print('-' * 8 + f'cosine_of_angle[0, {max_seq_len})' + '-' * 8, file=f, flush=True)
            B = apply_rotary_pos_emb(b.unsqueeze(0).expand(max_seq_len, -1), model.rotary_embedding)
            print(torch.einsum('i,bi -> b', a, B) / (torch.norm(a) * torch.norm(b)), file=f, flush=True)
            print('-' * 8 + f'dot product[0, {max_seq_len})' + '-' * 8, file=f, flush=True)
            print(torch.einsum('i,bi -> b', a, B), file=f, flush=True)
