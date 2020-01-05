#!/usr/bin/env python
#!/usr/bin/python
# -*- coding: UTF-8 -*-


"""
@File：BigInt.py
@Data：2020/1/5
@param：
@return：
"""

def bigint(s1: list, s2: list) -> list:
    """
    大整数相乘
    :param s1:
    :param s2:
    :return:
    """
    data = []
    for i in range(len(s1 + s2)):
        data.append(0)

    for m in range(len(s1)):
        for n in range(len(s2)):
            data[len(s1 + s2) - m - n - 1] = data[len(s1 + s2) - m - n - 1] + int(s1[len(s1) - m - 1]) * int(s2[len(s2) - n - 1])

    for i in range(len(s1 + s2)):
        if data[len(data) - 1 - i] >= 10:
            data[len(data) - i - 2] = data[len(data) - i - 2] + data[len(data) - i - 1] // 10
            data[len(data) - i - 1] = data[len(data) - i - 1] % 10
    if data[0] == 0:
        data.pop(0)
    return "".join([str(x) for x in data])


if __name__ == '__main__':

    s = bigint("123445234", "324236572")
    print(s)
    print(int(123445234) * int(324236572))