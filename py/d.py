#!/usr/bin/env python

# 题目描述，给定正整数N，将从1到N的N个数字，按照字符串字典序排列


def get_next(i, n):
    next_value = i * 10
    if next_value <= n:
        return next_value
    next_value = i + 1
    while True:
        while next_value % 10 == 0:
            next_value //= 10
        if next_value == 1:
            return None
        if next_value > n:
            next_value = next_value // 10 + 1
            continue
        return next_value


def get_lexico_order(n):
    i = 1
    while i:
        yield i
        i = get_next(i, n)


if __name__ == '__main__':
    for n in range(1, 10000):
        n = 200
        arr = [str(i + 1) for i in range(n)]
        result = []
        for value in sorted(arr):
            result += [int(value)]

        my_result = []
        for value in get_lexico_order(n):
            my_result += [value]

        assert result == my_result
