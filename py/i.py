#!/usr/bin/env python

# 实现二分搜索upper_bound的多种方式


def bisect_right0(arr, target):
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] <= target:
            low = mid + 1
        else:
            high = mid - 1
    return low


def bisect_right1(arr, target):
    low, high = 0, len(arr)
    while low < high:
        mid = (low + high) // 2
        if arr[mid] <= target:
            low = mid + 1
        else:
            high = mid
    return low


def bisect_right2(arr, target):
    if not arr:
        return 0
    low, high = 0, len(arr)
    while low < high - 1:
        mid = (low + high) // 2
        if arr[mid] <= target:
            low = mid
        else:
            high = mid
    return high if arr[low] <= target else low


def bisect_right3(arr, target):
    if not arr:
        return 0
    n = len(arr)
    size = 1
    while size < n:
        size <<= 1
    low = 0
    while size > 1:
        size >>= 1
        mid = low + size
        if mid < n and arr[mid] <= target:
            low = mid
    return (low + size) if arr[low] <= target else low


if __name__ == '__main__':
    import bisect
    import random
    from tqdm import tqdm
    n, c = 5000, 20
    for i in tqdm(range(n + 1)):
        for _ in range(c):
            arr = sorted(random.randrange(i) for j in range(i))
            for j in range(-1, i):
                assert bisect.bisect_right(arr, j) == bisect_right0(arr, j) == bisect_right1(arr, j) == bisect_right2(arr, j) == bisect_right3(arr, j)
