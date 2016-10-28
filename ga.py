# coding=gbk

import numpy as np
import random

import settings


def mutate_matrix(m):
    row_size, col_size = m.shape

    for k in range(0, 100):
        i = random.randint(0, row_size - 1)
        j = random.randint(0, col_size - 1)
        if m[i, j] == 0:
            if random.random() < 1.0 / (settings.category_max_count - 1):
                m[i, j] = 1
        else:
            m[i, j] = 0


def crossover_matrix(m1, m2):
    row_size, col_size = m1.shape

    cut_col = random.randint(1, col_size - 1)
    if random.random() < 0.5:
        return np.concatenate((m2[:, :cut_col], m1[:, cut_col:]), axis=1)
    else:
        return np.concatenate((m1[:, :cut_col], m2[:, cut_col:]), axis=1)


if __name__ == '__main__':
    m = np.array([[2, 1, 3], [0, 0, 0], [1, 1, 1]])
    n = np.zeros([3, 3])
    # print m
    # print n
    # m = m.transpose()
    # l = np.concatenate((m[:, :1], n), axis=1)
    # l[0, 0] = 5
    # print l
    print m
    print n
    print crossover_matrix(m, n)
