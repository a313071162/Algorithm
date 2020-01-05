#!/usr/bin/env python
#!/usr/bin/python
# -*- coding: UTF-8 -*-


"""
@File：QuickSort.py
@Data：2020/1/5
@param：
@return：
"""

def quicksort(A, start, end) -> list:
    """
    分治
    :param A:
    :param start:
    :param end:
    :return:
    """
    if start < end:
        q = position(A, start, end)
        quicksort(A, start, q - 1)
        quicksort(A, q + 1, end)
    return A

def position(A, start, end) -> int:
    """
    交换位置
    :param A:
    :param start:
    :param end:
    :return:
    """
    x = A[end]
    i = start
    for j in range(start, end):
        if A[j] <= x:
            temp = A[i]
            A[i] = A[j]
            A[j] = temp
            i = i + 1
    temp = A[i]
    A[i] = A[end]
    A[end] = temp

    return i



if __name__ == '__main__':
    A = [5, 9, 10, 22, 1, 80, 7, 4, 55]
    s = quicksort(A, 0, len(A) - 1)
    print(s)