#!/usr/bin/env python

# 题目描述，给定若干不重复的元素，每个元素有一个权重(整型、非负)，初始化之后，会多次调用按照权重随机返回的函数和修改元素权重的函数

import bisect
import random


class BitArray():
    class PrefixSumArray():
        def __init__(self, bit_array):
            self.bit_array = bit_array

        def __len__(self):
            return len(self.bit_array) + 1

        def __getitem__(self, k):
            n = len(self)
            if k >= n or k < -n:
                raise IndexError('list index out of range')

            k %= n
            return self.bit_array.prefix_sum(k)

        def __repr__(self):
            return '[' + ', '.join(repr(self[i]) for i in range(len(self))) + ']'

    def __init__(self, values=[]):
        self.arr = []
        for i, value in enumerate(values):
            self.arr += [value]
            while i:
                i -= i & -i
                self.arr[i] += value
        self._prefix_sum_array = BitArray.PrefixSumArray(self)

    def __len__(self):
        return len(self.arr)

    def append(self, value):
        i = len(self)
        self.arr += [value]
        while i:
            i -= i & -i
            self.arr[i] += value

    def __getitem__(self, k):
        n = len(self)
        if k >= n or k < -n:
            raise IndexError('list index out of range')

        k %= n
        result = self.arr[k]
        i = 1
        while k & i == 0 and k | i < n:
            result -= self.arr[k | i]
            i <<= 1
        return result

    def __setitem__(self, k, v):
        n = len(self)
        if k >= n or k < -n:
            raise IndexError('list index out of range')

        k %= n
        diff = v - self[k]
        self.arr[k] += diff
        while k:
            k -= k & -k
            self.arr[k] += diff

    def __repr__(self):
        return '[' + ', '.join(repr(self[i]) for i in range(len(self))) + ']'

    def prefix_sum(self, k):
        n = len(self)
        if k > n or k < 0:
            raise ValueError('prefix count out of range')
        if not k:
            return 0
        result = self.arr[0]
        while k < n:
            result -= self.arr[k]
            k += k & -k
        return result

    def range_sum(self, start, end):
        assert 0 <= start <= end <= len(self)
        return self.prefix_sum(end) - self.prefix_sum(start)

    def prefix_sum_array(self):
        return self._prefix_sum_array


class WeightedRandomSelector():
    def __init__(self, item_weight_dict):
        self.item_index_dict, self.item_list, self.bit_array = {}, [], BitArray()
        for item, weight in item_weight_dict.items():
            self.item_index_dict[item] = len(self.item_list)
            self.item_list.append(item)
            self.bit_array.append(weight)

    def update_weight(self, item, weight):
        if item not in self.item_index_dict:
            self.item_index_dict[item] = len(self.item_list)
            self.item_list.append(item)
            self.bit_array.append(weight)
        else:
            self.bit_array[self.item_index_dict[item]] = weight

    def random_select(self):
        prefix_sum_array = self.bit_array.prefix_sum_array()
        random_weight = random.randrange(0, prefix_sum_array[-1])
        random_index = bisect.bisect_right(prefix_sum_array, random_weight) - 1
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

    weighted_random_selector.update_weight('d', 2)

    try_count = 110000
    item_count_dict = {}

    for i in range(try_count):
        value = weighted_random_selector.random_select()
        item_count_dict[value] = item_count_dict.get(value, 0) + 1

    print(item_count_dict)

    weighted_random_selector.update_weight('a', 0)

    try_count = 100000
    item_count_dict = {}

    for i in range(try_count):
        value = weighted_random_selector.random_select()
        item_count_dict[value] = item_count_dict.get(value, 0) + 1

    print(item_count_dict)
