#!/usr/bin/env python
#!/usr/bin/python
# -*- coding: UTF-8 -*-


"""
@File：Steel_Cutting.py
@Data：2019/7/10
@param：
@return：
"""

def top_to_bottom(p:list, n:int) -> list:
    """
    递归
    :param p:
    :param n:
    :return:
    """
    if n == 0:
        return 0
    q = 0
    for i in range(1, n + 1):
        q = max(q, p[i] + top_to_bottom(p, n - i))
    return q

def memorize(p:list, n:int):
    """
    备忘录
    :param p:
    :param n:
    :return:
    """
    r = [-1] * (n + 1)
    def memorize_cut(p:list, n:int, r:list):
        if r[n] >= 0:
            return r[n]
        q = 0
        if n == 0:
            q = 0
        else:
            for i in range(1, n +1):
                q = max(q, p[i] + memorize_cut(p, n - i, r))
        r[n] = q
        return q
    return memorize_cut(p, n, r), r


def steel_cutting(p: list, n: int) -> (list, int):
    r = [0] * (n + 1)
    for i in range(1, n + 1):
        if n == 0:
            return 0
        q = 0
        for j in range(1, i + 1):
            q = max(q, p[j] + r[i - j])
            r[i] = q
    return r[n], r

if __name__ == '__main__':
    p = [0, 1, 5, 8, 9, 10, 17, 17, 20, 24, 30]
    r = top_to_bottom(p, 4)
    print(r)
    s, r= memorize(p, 5)
    print(s, r)
    s, r = steel_cutting(p, 5)
    print(s, r)