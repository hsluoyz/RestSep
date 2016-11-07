# coding=gbk

import numpy as np
import random

import settings


def init_random_matrix(row_size, col_size):
    m = np.zeros((row_size, col_size), dtype=np.int)
    for j in range(0, col_size):
        m[random.randrange(0, row_size, 1), j] = 1
    return m


def remove_empty_rows_from_matrix(m):
    row_size, col_size = m.shape
    row_sums = m.sum(axis=1)
    new_m = np.empty([0, col_size], dtype=int)

    for i in range(row_size):
        if row_sums[i] != 0:
            new_m = np.append(new_m, m[i: i+1, :], axis=0)
    return new_m


def get_category_number(m):
    row_sums = m.sum(axis=1)
    res = 0
    for row_sum in row_sums:
        if row_sum > 0:
            res += 1
    return res


def get_overuse_number(m):
    row_size, col_size = m.shape
    return m.sum() - col_size, (row_size - 1) * col_size


def get_covered_testcase_number(m):
    row_size, col_size = m.shape
    test_row_size, test_col_size = settings.test_matrix.shape

    # 1st matrix multiply
    res = np.dot(settings.test_matrix, (1 - m).transpose())
    # print res

    # 2nd matrix multiply
    res = np.dot(np.where(res == 0, 1, 0), np.ones([row_size, 1]))

    # 3rd matrix multiply
    res = np.dot(np.ones([1, test_row_size]), np.where(res != 0, 1, 0))

    # Get the score.
    res = int(res[0, 0])

    return res


def get_category_number_score(number):
    return max(100 - 3 * abs(number - settings.api_count / 10), 0)


def get_overuse_score(number, overall_number):
    return max(100 - 100 * 2 * number / overall_number, 0)


def get_covered_testcase_score(number):
    return 100 * number / settings.case_count


def evaluate_matrix(m):
    score = 0
    score += get_category_number_score(get_category_number(m))
    number, overall_number = get_overuse_number(m)
    score += get_overuse_score(number, overall_number)
    score += get_covered_testcase_score(get_covered_testcase_number(m))
    return score


def evaluate_matrix_from_numbers(m, n1, n2, n3):
    row_size, col_size = m.shape

    score = 0
    score += get_category_number_score(n1)
    score += get_overuse_score(n2, (row_size - 1) * col_size)
    score += get_covered_testcase_score(n3)
    return score


def print_matrix(m):
    row_size, col_size = m.shape
    res = ""
    for i in range(0, row_size):
        for j in range(0, col_size):
            res += str(m[i, j])
        if i != row_size - 1:
            res += '\n'
    print res
    print "row size = " + str(row_size) + ", column size = " + str(col_size)

    category_number = get_category_number(m)
    overuse_number = get_overuse_number(m)[0]
    covered_testcase_number = get_covered_testcase_number(m)

    print "category number = " + str(category_number) + " (expected: 10, score: " + str(get_category_number_score(category_number)) + ")"
    print "overuse number = " + str(overuse_number) + " (expected: 0, score: " + str(get_overuse_score(overuse_number, (row_size - 1) * col_size)) + ")"
    print "covered testcase number = " + str(covered_testcase_number) + " (expected: " + str(settings.case_count) + ", score: " + str(get_covered_testcase_score(covered_testcase_number)) + ")"
    print "final score = " + str(evaluate_matrix_from_numbers(m, category_number, overuse_number, covered_testcase_number)) + "/300"


def get_matrix_description(m):
    category_number = get_category_number(m)
    overuse_number = get_overuse_number(m)[0]
    covered_testcase_number = get_covered_testcase_number(m)

    return "categories: %d, overuse: %d, covered testcases: %d/%d" % (category_number, overuse_number, covered_testcase_number, settings.case_count)


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

    # print m
    # print n
    # print crossover_matrix(m, n)

    print m
    m = remove_empty_rows_from_matrix(m)
    print m
