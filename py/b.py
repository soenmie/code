#!/usr/bin/env python


# 题目描述，给定若干不重复的元素，每个元素有一个权重(整型、非负)，初始化之后，会多次调用按照权重随机返回的函数

# import bisect
import random


def bisect_right(arr, target):
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] <= target:
            low = mid + 1
        else:
            high = mid - 1
    return low


class WeightedRandomSelector():
    def __init__(self, item_weight_dict):
        self.item_list, self.accumlated_sum_list = [], []
        self.accumlated_sum_list += [0]
        for item, weight in item_weight_dict.items():
            self.item_list += [item]
            self.accumlated_sum_list += [self.accumlated_sum_list[-1] + weight]

    def random_select(self):
        random_weight = random.randrange(0, self.accumlated_sum_list[-1])
        # random_index = bisect.bisect_right(self.accumlated_sum_list, random_weight) - 1
        random_index = bisect_right(self.accumlated_sum_list, random_weight) - 1
        return self.item_list[random_index]


if __name__ == '__main__':
    item_weight_dict = {'a': 1, 'b': 3, 'c': 5}

    weighted_random_selector = WeightedRandomSelector(item_weight_dict)

    try_count = 90000
    item_count_dict = {}

    for i in range(try_count):
        value = weighted_random_selector.random_select()
        item_count_dict[value] = item_count_dict.get(value, 0) + 1

    print(item_count_dict)
