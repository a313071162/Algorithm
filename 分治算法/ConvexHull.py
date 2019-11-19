#!/usr/bin/env python
#!/usr/bin/python
# -*- coding: UTF-8 -*-


"""
@File：ConvexHull.py
@Data：2019/10/26
@param：
@return：
"""

import random
import time
import matplotlib.pyplot as plt

def calTri(x, y, z):
    """
    求三角形的面积S=(x1y2-x1y3+x2y3-x2y1+x3y1-x3y2) / 2
    :param x:
    :param y:
    :param z:
    :return: 三角形的面积
    """
    size = (x[0] * y[1] - x[0] * z[1] + y[0] * z[1] - y[0] * x[1] + z[0] * x[1] - z[0] * y[1]) / 2
    return size


def positive_number_size(left, min_dot, maxs, all_dot):
    """
    求连线的左侧包（结果为正，且为最大）
    :param left: 左侧含有点
    :param min_dot: 横坐标最小点
    :param maxs: 左侧面积最大的点
    :param all_dot: 存储点的数组
    :return:
    """
    # 存储当前的最大值
    cur_max_size = float()
    # 存储当前的最大点
    cur_dot = ()
    # 超过点的集合
    border_dot = []
    # 在这条线上的集合
    line = []

    for val in left:
        size = calTri(min_dot, maxs, val)
        if size < 0:
            # 若面积为负，则其肯定在凸包内部
            continue
        elif size == 0:
            # 此处是指若该点与连线在一条线上
            line.append(val)
        else:
            # 此处值都是为点在连线之上
            if size > cur_max_size:
                if len(cur_dot) > 0:
                    border_dot.append(cur_dot)
                cur_max_size = size
                cur_dot = val
            else:
                border_dot.append(val)
    # 判断是否有在连线之上的点
    if not border_dot:
        if not cur_dot:
            # 此处用extend则可将在一条线上的点全部存入
            all_dot.extend(line)
            return [], ()
        else:
            # 最大点只有一个
            all_dot.append(cur_dot)
            return [], cur_dot
    else:
        all_dot.append(cur_dot)
        return all_dot, cur_dot


def negative_number_size(right, mins, min_dot, all_dot):
    """
    求连线的右侧包（结果为负，且为最大）
    :param right: 右侧含有点
    :param mins: 左侧坐标最小点
    :param min_dot: 右侧面积最大的点
    :param all_dot: 存储点的数组
    :return:
    """
    # 存储当前的最小值
    cur_min_size = float()
    # 存储当前的最大点
    cur_dot = ()
    # 超过点的集合
    border_dot = []
    # 在这条线上的集合
    line = []

    for val in right:
        size = calTri(mins, min_dot, val)
        if size > 0:
            continue
        elif size == 0:
            line.append(val)
        else:
            # 此处值都是为点在连线之上
            if size < cur_min_size:
                if len(cur_dot) > 0:
                    border_dot.append(cur_dot)
                cur_min_size = size
                cur_dot = val
            else:
                border_dot.append(val)

    # 判断是否有在连线之上的点
    if not border_dot:
        if not cur_dot:
            # 此处用extend则可将在一条线上的点全部存入
            all_dot.extend(line)
            return [], ()
        else:
            # 最小点只有一个
            all_dot.append(cur_dot)
            return [], cur_dot
    else:
        all_dot.append(cur_dot)
        return all_dot, cur_dot



def divide_up(left, min_dot, max_dot, maxs, all_dot = []):
    """
    划分上凸包
    :param left: 左侧含有点
    :param min_dot: 横坐标最小点
    :param max_dot: 横坐标最大点
    :param maxs: 当前最大值(横坐标居中与min_dot,max_dot组成最大的三角形的点)
    :return:
    """
    if not left:
        return all_dot
    # 若left中只含一个元素，则其肯定为凸出点
    if len(left) == 1:
        all_dot.append(left[0])

    # 寻找左上包的点
    left_dot, cur_max_dot = positive_number_size(left, min_dot, maxs, all_dot)
    # 左上凸包继续分治
    if left_dot:
        divide_up(left, min_dot, maxs, cur_max_dot, all_dot)

    # 寻找右上包的点
    right_dot, cur_min_dot = positive_number_size(left, maxs, max_dot, all_dot)
    if right_dot:
        divide_up(left, maxs, max_dot, cur_min_dot, all_dot)

    return all_dot


def divide_down(right, min_dot, max_dot, mins, all_dot = []):
    """
    划分下凸包
    :param right: 右侧含有点
    :param min_dot: 横坐标最小点
    :param max_dot: 横坐标最大点
    :param mins: 当前最小值(横坐标居中与min_dot,max_dot组成最大的负三角形的点)
    :return:
    """
    if not right:
        return all_dot
    # 若right中只含一个元素，则其肯定为凸出点
    if len(right) == 1:
        all_dot.append(right[0])

    # 寻找左下包的点
    left_dot, cur_max_dot = negative_number_size(right, min_dot, mins, all_dot)
    # 左下凸包继续分治
    if left_dot:
        divide_down(right, min_dot, mins, cur_max_dot, all_dot)

    # 寻找右下包的点
    right_dot, cur_min_dot = negative_number_size(right, mins, max_dot, all_dot)
    if right_dot:
        divide_down(right, mins, max_dot, cur_min_dot, all_dot)

    return all_dot


def divide(random_list):
    """
    生成一个随机的元组
    :param random_list:
    :return: 返回最终结果信息（包括凸包表示点坐标，上凸包点，下凸包点，和横坐标最小最大值）
    """
    # 对随机数组进行排序，好选取最外围点(横坐标最大值和最小值)
    random_list = sorted(random_list)
    # 横坐标最大点
    max_dot = random_list[-1]
    # 横坐标最小点
    min_dot = random_list[0]

    # 面积最大和最小
    max_size = float()
    min_size = float()

    # 横坐标最大最小连线点左侧和右侧
    left = []
    right = []

    # 当前最大点和最小点
    maxs = ()
    mins = ()
    # 取上下部分面积最大的三角形的值
    for val in random_list[1: -1]:
        cur_size = calTri(min_dot, max_dot, val)
        # 判断是在左侧还是右侧
        if cur_size > 0:
            # 判断是否比当前最大值大
            if cur_size > max_size:
                if len(maxs) > 0:
                    left.append(maxs)
                # 最大点赋值，只找比其点面积更大的点
                max_size = cur_size
                maxs = val
                continue
            else:
                left.append(val)
        elif cur_size < 0:
            if cur_size < min_size:
                if len(mins) > 0:
                    right.append(mins)
                min_size = cur_size
                mins = val
                continue
            else:
                right.append(val)
    res = []
    # 此处开始通过分治的方法对凸包进行划分
    # 在此处进行分包时，一定要缩小范围，若在左侧，则变化最大点，在右侧变化最小点
    res_left = divide_up(left, min_dot, max_dot, maxs)
    res_right = divide_down(right, min_dot, max_dot, mins)

    # 此处可能有重复元素，需要去重
    if res_left:
        res.extend(set(res_left))
    if res_right:
        res.extend(set(res_right))
    # 加上4个点
    res.append(max_dot)
    res.append(min_dot)
    if maxs:
        res.append(maxs)
        res_left.append(maxs)
    if mins:
        res.append(mins)
        res_right.append(mins)
    # 返回左侧分包和右侧分包
    return res, res_left, res_right, max_dot, min_dot

def main():
    """
    对函数进行调度
    :return:
    """
    # 首先生成20个-1000～1000的随机点
    random_list = [(random.randint(-500, 500), random.randint(-500, 500)) for x in range(20)]
    print(random_list)
    # random_list = [(-394, -33), (-480, -425), (396, -387), (-350, -284), (220, 189), (-139, -271), (-381, 155), (-353, 82), (-463, 207), (248, -80), (27, -76), (-402, 475), (179, -91), (169, 191), (-233, -396), (379, 418), (-467, 16), (185, -271), (336, -54), (-416, 209)]
    # 若生成重复值则去除重复值
    random_list = set(random_list)
    # 获取结果，方便显示
    res, res_left, res_right, maxs, mins = divide(random_list)

    plt.scatter([dot[0] for dot in random_list], [dot[1] for dot in random_list], color='blue')
    plt.scatter([dot[0] for dot in res], [dot[1] for dot in res], color='red')

    res_left = sorted(res_left)
    res_right = sorted(res_right)

    # 画出凸包连线
    if res_left:
        plt.plot([mins[0], res_left[0][0]], [mins[1], res_left[0][1]], color='r')
        plt.plot([maxs[0], res_left[-1][0]], [maxs[1], res_left[-1][1]], color='r')
    if res_right:
        plt.plot([mins[0], res_right[0][0]], [mins[1], res_right[0][1]], color='r')
        plt.plot([maxs[0], res_right[-1][0]], [maxs[1], res_right[-1][1]], color='r')
    if (res_left and not res_right) or (not res_left and res_right):
        plt.plot([maxs[0], mins[0]], [maxs[1], mins[1]], color='r')
    # else:
    for i in range(len(res_left) - 1):
        plt.plot([res_left[i][0], res_left[i + 1][0]], [res_left[i][1], res_left[i + 1][1]], color='r')
    for i in range(len(res_right) - 1):
        plt.plot([res_right[i][0], res_right[i + 1][0]], [res_right[i][1], res_right[i + 1][1]], color='r')
    # plt.plot([left_set[-1][0], right_set[-1][0]], [left_set[-1][1], right_set[-1][1]], color='r')

    plt.show()


if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    print(end - start)


