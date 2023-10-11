import random


def distribute(self, degree_sum, part_num, covariance):
    result = []
    for i in range(part_num):
        result.append(max(6, int(random.normalvariate(degree_sum/part_num, covariance)))) #Guarante the lower limit
    cur_sum = sum(result)
    # 这个就是超出result的长度
    if cur_sum > degree_sum:
        diff = cur_sum-degree_sum
        k = int(diff/part_num)
        remain = diff%part_num
        for i in range(part_num):
            if i < remain:
                result[i] -=(1+k)
            else:
                result[i] -= (k)
    elif cur_sum < degree_sum:
        diff = degree_sum-cur_sum
        k = int(diff/part_num)
        remain = diff%part_num
        for i in range(part_num):
            if i < remain:
                result[i] +=(1+k)
            else:
                result[i] += (k)
    return result