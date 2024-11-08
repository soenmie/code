#!/usr/bin/env python

# 题目描述，给定一组非负数的数组，数值代表直方图柱子的高度，求直方图可以被分解成最小的若干个矩形的数量


def calc_min_rectangle_count(values):
    stack, result = [], 0
    for value in values:
        while stack and stack[-1] > value:
            stack.pop()
            result += 1
        if not stack or stack[-1] < value:
            stack.append(value)
    result += len(stack)
    return result


if __name__ == '__main__':
    values = [1, 2, 3, 4, 5]
    print(values, calc_min_rectangle_count(values))

    values = [5, 4, 3, 2, 1]
    print(values, calc_min_rectangle_count(values))

    values = []
    print(values, calc_min_rectangle_count(values))

    values = [1, 2, 1]
    print(values, calc_min_rectangle_count(values))

    values = [2, 1, 2]
    print(values, calc_min_rectangle_count(values))

    values = [1, 1, 1, 1]
    print(values, calc_min_rectangle_count(values))

    values = [2, 1, 3, 1, 0]
    print(values, calc_min_rectangle_count(values))
