#!/usr/bin/env python

# 题目描述: 返回两个字符串的编辑距离，如何编辑距离大于k (k 小于两个字符串的长度)，返回正无穷

def solution0(a, b, k):
    m, n = len(a), len(b)
    if n > m:
        return solution0(b, a, k)
    if m - n > k:
        return float('inf')

    state = [[float('inf') for _ in range(n + 1)] for _ in range(m + 1)]

    state[0][0] = 0

    for i in range(1, m + 1):
        state[i][0] = i

    for j in range(1, n + 1):
        state[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                state[i][j] = state[i - 1][j - 1]
            else:
                state[i][j] = min(state[i][j - 1], state[i - 1][j], state[i - 1][j - 1]) + 1

    return float('inf') if state[m][n] > k else state[m][n]


def solution1(a, b, k):
    m, n = len(a), len(b)
    if n > m:
        return solution1(b, a, k)
    if m - n > k:
        return float('inf')

    state = [[float('inf') for _ in range(n + 1)] for _ in range(m + 1)]

    state[0][0] = 0

    for i in range(1, min(k, m) + 1):
        state[i][0] = i

    for j in range(1, min(k + n - m, n) + 1):
        state[0][j] = j

    for i in range(1, m + 1):
        for j in range(max(i - k, 1), min(k + n - m + i, n) + 1):
            if a[i - 1] == b[j - 1]:
                state[i][j] = state[i - 1][j - 1]
            else:
                state[i][j] = min(state[i][j - 1], state[i - 1][j], state[i - 1][j - 1]) + 1
                if state[i][j] > k and i - j == m - n:
                    return float('inf')

    return state[m][n]


def solution2(a, b, k):
    m, n = len(a), len(b)
    if n > m:
        return solution2(b, a, k)
    if m - n > k:
        return float('inf')

    state = [[float('inf') for _ in range(n + 1)] for _ in range(m + 1)]

    state[0][0] = 0

    for i in range(1, min(k, m) + 1):
        state[i][0] = i

    for j in range(1, min(k + n - m, n) + 1):
        state[0][j] = j

    low, high = -k, k + n - m
    for i in range(1, m + 1):
        low, high = low + 1, high + 1
        for j in range(max(low, 1), min(high, n) + 1):
            if a[i - 1] == b[j - 1]:
                state[i][j] = state[i - 1][j - 1]
            else:
                state[i][j] = min(state[i][j - 1], state[i - 1][j], state[i - 1][j - 1]) + 1
                if state[i][j] > k:
                    if i - j > m - n:
                        low = j + 1
                    elif i - j < m - n:
                        high = j - 1
                        break
                    else:
                        return float('inf')

    return state[m][n]


def solution3(a, b, k):
    m, n = len(a), len(b)
    if n > m:
        return solution3(b, a, k)
    if m - n > k:
        return float('inf')

    state = [float('inf') for _ in range(n + 1)]

    for j in range(0, min(k + n - m, n) + 1):
        state[j] = j

    low, high = -k, k + n - m
    for i in range(1, m + 1):
        low, high = low + 1, high + 1
        top_left_value = state[max(low, 1) - 1]
        state[0] = i if i <= k else float('inf')
        for j in range(max(low, 1), min(high, n) + 1):
            new_top_left_value = state[j]
            if a[i - 1] == b[j - 1]:
                state[j] = top_left_value
            else:
                state[j] = min(state[j - 1], state[j] if j < high else float('inf'), top_left_value) + 1
                if state[j] > k:
                    if i - j > m - n:
                        low = j + 1
                    elif i - j < m - n:
                        high = j - 1
                        break
                    else:
                        return float('inf')

            top_left_value = new_top_left_value

    return state[n]


def solution4(a, b, k):
    m, n = len(a), len(b)
    if n > m:
        return solution4(b, a, k)
    if m - n > k:
        return float('inf')

    state = [float('inf') for _ in range(k + min(k + n - m, n) + 1)]

    for j in range(k, k + min(k + n - m, n) + 1):
        state[j] = j - k

    low, high = 0, k + k + n - m
    for i in range(1, m + 1):
        if i <= k:
            state[k - i] = i

        for j in range(max(low, k - i + 1), min(high, k - i + n) + 1):
            if a[i - 1] != b[j + i - k - 1]:
                state[j] = min(state[max(j - 1, 0): min(j + 1, k - i + n + 1) + 1]) + 1
                if state[j] > k:
                    if i - (j + i - k) > m - n:
                        low = j + 1
                    elif i - (j + i - k) < m - n:
                        high = j - 1
                        break
                    else:
                        return float('inf')

    return state[k - max(0, m - n)]


def solution5(a, b, k):
    m, n = len(a), len(b)
    if n > m:
        return solution5(b, a, k)
    if m - n > k:
        return float('inf')

    state = [float('inf') for _ in range(min(k, m) + min(k + n - m, n) + 1)]

    for j in range(min(k, m), min(k, m) + min(k + n - m, n) + 1):
        state[j] = j + max(0, k - m) - k

    low, high = 0, k + k + n - m
    for i in range(1, m + 1):
        if i <= k:
            state[k - i - max(0, k - m)] = i

        for j in range(max(low, k - i + 1), min(high, k - i + n) + 1):
            if a[i - 1] != b[j + i - k - 1]:
                state[j - max(0, k - m)] = min(state[max(j - 1, 0) - max(0, k - m): min(j + 1, k - i + n + 1) - max(0, k - m) + 1]) + 1
                if state[j - max(0, k - m)] > k:
                    if i - (j + i - k) > m - n:
                        low = j + 1
                    elif i - (j + i - k) < m - n:
                        high = j - 1
                        break
                    else:
                        return float('inf')

    return state[k - max(0, m - n) - max(0, k - m)]


if __name__ == '__main__':
    import random
    from tqdm import tqdm

    max_str_len, max_k, vocab_size = 20, 20, 5

    for _ in tqdm(range(1000)):
        a = ''.join(str(random.randrange(0, vocab_size)) for i in range(random.randint(0, max_str_len)))
        b = ''.join(str(random.randrange(0, vocab_size)) for i in range(random.randint(0, max_str_len)))
        k = random.randint(0, max_k)

        assert solution0(a, b, k) == solution1(a, b, k) == solution2(a, b, k) == solution3(a, b, k) == solution4(a, b, k) == solution5(a, b, k)
