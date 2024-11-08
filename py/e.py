#!/usr/bin/env python

# 题目描述，给定一个字符串，判断是否是否可以由给定集合中的字符串组成，集合中的字符串可以反复使用


def is_consist_of(target, string_set):
    n = len(target)
    state = [False] * (n + 1)
    state[0] = True
    for i in range(1, n + 1):
        for string in string_set:
            m = len(string)
            if i - m < 0:
                continue
            state[i] |= (state[i - m] and string == target[i - m:i])
            if state[i]:
                break
    return state[n]


if __name__ == '__main__':
    string_set = {'dog', 'cat'}
    target = 'dogcat'
    print(is_consist_of(target, string_set))
    target = 'catdog'
    print(is_consist_of(target, string_set))
    target = 'catcat'
    print(is_consist_of(target, string_set))
    target = 'catpig'
    print(is_consist_of(target, string_set))
    target = '1234'
    print(is_consist_of(target, string_set))
