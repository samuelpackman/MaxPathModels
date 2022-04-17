#generates all values that add to target. uses recursive algorithm more
#found on web
#webpage is https://stackoverflow.com/questions/4632322/finding-all-possible-combinations-of-numbers-to-reach-a-given-sum
import numpy as np


def subset_sum_(numbers, target, partial=[], partial_sum=0):
    if partial_sum == target:
        yield partial
    if partial_sum >= target:
        return
    for i, n in enumerate(numbers):
        remaining = numbers[i + 1:]
        yield from subset_sum(remaining, target, partial + [n], partial_sum + n)

def nums_inc(num_vals_target, target, partial = [], max = -1): #yields list increasing to target,max is max of partial
    if len(partial) == target:
        yield partial
    for n in range(max+1, target+1):
        yield from nums_inc(num_vals_target, target, partial + [n], n)
#converts list that add to target to list increasing to target


#print(inc_seq(4))

#return list of k elements from list, in same order

def k_inc_list(nums, k, partial = []):
    if k == 0:
        yield partial
        return
    for i, n in enumerate(nums):
        remaining = nums[i + 1:]
        yield from k_inc_list(remaining, k - 1, partial + [n])

def inc_seq(start, stop, k): #start stop inclusive, exclusive
    return np.array(list(k_inc_list(list(range(start, stop)), k)))
