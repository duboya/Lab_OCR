# -*- coding:utf-8 -*-
class Solution:
    def find_min(self, nums):
        if not nums:
            return False
        length = len(nums)
        left, right = 0, length - 1
        while nums[left] >= nums[right]:
            if right - left == 1:
                return nums[right]
            mid = int((left + right) / 2)
            if nums[left] == nums[mid] == nums[right]:
                return min(nums)
            if nums[left] <= nums[mid]:
                left = mid
            if nums[right] >= nums[mid]:
                right = mid
        return nums[0]

    def minNumberInRotateArray(self, rotateArray):
        # write code here
        if not rotateArray:
            return 0

        start, end, mid = 0, len(rotateArray) - 1, int((len(rotateArray) - 1) / 2)
        # mid = int((start - end)/2)
        while True:
            # rotateArray = rotateArray[start:end]
            if end > start + 1:
                mid = round(start + (end - start) / 2)
                if rotateArray[mid] < rotateArray[end]:
                    # the back of array is the sorted
                    end = mid
                else:  # find the reverse list in the back of array
                    start = mid
            else:
                if rotateArray[start] > rotateArray[end]:
                    return rotateArray[end]
                else:
                    return rotateArray[start]


def bubble_sort3(ary):
    n = len(ary)
    k = n  # k为循环的范围，初始值n
    for i in range(n):
        flag = True
        for j in range(i + 1, k):  # 只遍历到最后交换的位置即可
            if ary[j - 1] > ary[j]:
                ary[j - 1], ary[j] = ary[j], ary[j - 1]
                k = j  # 记录最后交换的位置
                flag = False
        if flag:
            break
    return ary


def bubble_sort(arry):
    n = len(arry)  # 获得数组的长度
    for i in range(n):
        for j in range(1, n - i):  # 每轮找到最大数值 或者用 for j in range(i+1, n)
            if arry[j - 1] > arry[j]:  # 如果前者比后者大
                arry[j - 1], arry[j] = arry[j - 1], arry[i]  # 则交换两者
    return arry


def insert_sort(arry):
    n = len(arry)  # 获得数组的长度
    for i in range(1, n):
        key = i - 1
        temp = arry[i]
        while key >= 0 and temp > arry[key]:
            arry[key + 1] = arry[key]
            key -= 1
        arry[key + 1] = temp
    return arry


def shell_sort(arry):
    count = len(arry)
    gap = round(count / 2)
    while gap >= 1:
        for i in range(gap, count):
            j = i
            temp = arry[j]
            while j - gap >= 0 and temp > arry[j - gap]:
                arry[j] = arry[j - gap]
                j -= gap
            arry[j] = temp
        gap = round(gap / 2)
    return arry


def merge_sort(arry):
    if len(arry) <= 1:
        return arry
    mid = int(len(arry) / 2)
    left = merge_sort(arry[:mid])
    right = merge_sort(arry[mid:])
    return merge(left, right)


def merge(left, right):
    res = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] > right[j]:
            res.append(left[i])
            i += 1
        else:
            res.append(right[j])
            j += 1
        res = res + left[i:] + right[j:]
        return res


# def merge_sort(ary):
#
#     if len(ary) <= 1:
#         return ary
#
#     median = int(len(ary) / 2)  # 二分分解
#     left = merge_sort(ary[:median])
#     right = merge_sort(ary[median:])
#     return merge(left, right)  # 合并数组

# def merge(left, right):
#     '''合并操作，
#    将两个有序数组left[]和right[]合并成一个大的有序数组'''
#     res = []
#     i = j = k = 0
#     while (i < len(left) and j < len(right)):
#         if left[i] < right[j]:
#             res.append(left[i])
#             i += 1
#         else:
#             res.append(right[j])
#             j += 1
#
#     res = res + left[i:] + right[j:]
#     return res

def quick_sort(arry):
    return qsort(arry, 0, len(arry) - 1)


def qsort(arry, start, end):
    if start < end:
        left, right, key = start, end, arry[start]
    else:
        return arry
    while left < right:
        while left < right and arry[right] > key:
            right -= 1
        if left < right:
            arry[left] = arry[right]
            left += 1
        while left < right and arry[left] < key:
            left += 1
        if left < right:
            arry[right] = arry[left]
            right -= 1
        # if left == right:
    arry[left] = key
    qsort(arry, start, left - 1)
    qsort(arry, left + 1, end)
    return arry


def quick_sort_v2(ary):
    if len(ary) <= 1:
        return ary
    greater = []
    less = []
    base = ary.pop()
    for count in ary:
        if count > base:
            greater.append(count)
        else:
            less.append(count)
    return quick_sort_v2(greater) + [base] + quick_sort_v2(less)


# -*- coding:utf-8 -*-
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution_v2:
    def FindKthToTail(self, head, k):
        # write code here
        index, length = -k, 0
        index_node = head
        start = head
        while start:
            start = start.next
            length += 1
            index += 1
            if index > 0:
                index_node = index_node.next
        return index_node


class Solution_v3:
    # matrix类型为二维列表，需要返回列表
    def printMatrix(self, matrix):
        # write code here
        if not matrix:
            return []
        len_row = len(matrix)
        len_col = len(matrix[0])
        min_loop = min(len_row, len_col)
        res = []
        start_loop, start_row, start_col, end_row, end_col = 1, 0, 0, len_row-1, len_col-1
        if min_loop == 1:
            if len_row == 1:
                return matrix[0][::-1]
            if len_col == 1:
                return matrix[::-1][0]
        while start_loop < min_loop:
            m = matrix[start_row][:]
            n = matrix[:][end_col]
            teemp_n = matrix[end_col][:]
            p = matrix[end_row][::-1]
            q = matrix[::-1][start_col]
            start_loop += 1
            temp_x = matrix[0][end_col]
            temp_y = matrix[1][end_col]
        return res


if __name__ == '__main__':
    test = Solution_v3()
    print(test.printMatrix([[1,2,3],[4,5,6],[7,8,9]]))
    # print(quick_sort_v2([3, 4, 5, 1, 2]))
