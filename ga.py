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


def get_covered_api_number(m):
    col_sums = m.sum(axis=0)
    res = 0
    for col_sum in col_sums:
        if col_sum > 0:
            res += 1
    return res


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


def get_covered_testcase_number_special(m):
    row_size, col_size = m.shape
    test_row_size, test_col_size = settings.test_matrix.shape

    # 1st matrix multiply
    res = np.dot(settings.test_matrix, np.where(m == 0, 1, 0).transpose())
    # print res

    # 2nd matrix multiply
    res = np.dot(np.where(res == 0, 1, 0), np.ones([row_size, 1]))

    # 3rd matrix multiply
    res = np.dot(np.ones([1, test_row_size]), np.where(res != 0, 1, 0))

    # Get the score.
    res = int(res[0, 0])

    return res


def get_reduced_matrix(m):
    row_size, col_size = m.shape
    original_covered = get_covered_testcase_number_special(m)
    new_m = np.copy(m)

    for i in range(row_size):
        for j in range(col_size):
            if new_m[i, j] == 1:
                new_m[i, j] = 0
                if get_covered_testcase_number_special(new_m) != original_covered:
                    new_m[i, j] = 1

    return new_m


def get_uncovered_testcases(m):
    uncovered_testcases = []

    row_size, col_size = m.shape
    test_row_size, test_col_size = settings.test_matrix.shape

    # 1st matrix multiply
    res = np.dot(settings.test_matrix, (1 - m).transpose())
    # print res

    # 2nd matrix multiply
    res = np.dot(np.where(res == 0, 1, 0), np.ones([row_size, 1]))

    for i in range(test_row_size):
        if res[i, 0] == 0:
            uncovered_testcases.append(i)
    return uncovered_testcases


settings.full_score = 800


def get_covered_api_score(number):
    return 100 * number / settings.api_count


def get_category_number_score(number):
    return max(100 - 3 * abs(number - settings.api_count / 10), 0)


def get_overuse_score(number, overall_number):
    return max(100 - 100 * number / overall_number, 0)


def get_covered_testcase_score(number):
    return 500 * number / settings.case_count


def evaluate_matrix(m):
    score = 0
    score += get_covered_api_score(get_covered_api_number(m))
    score += get_category_number_score(get_category_number(m))
    number, overall_number = get_overuse_number(m)
    score += get_overuse_score(number, overall_number)
    score += get_covered_testcase_score(get_covered_testcase_number(m))
    return score


def evaluate_matrix_from_numbers(m, n0, n1, n2, n3):
    row_size, col_size = m.shape

    score = 0
    score += get_covered_api_score(n0)
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

    covered_api_number = get_covered_api_number(m)
    category_number = get_category_number(m)
    overuse_number = get_overuse_number(m)[0]
    covered_testcase_number = get_covered_testcase_number(m)

    print "covered API number = " + str(covered_api_number) + " (expected: " + str(settings.api_count) + ", score: " + str(get_covered_api_score(covered_api_number)) + ")"
    print "category number = " + str(category_number) + " (expected: 10, score: " + str(get_category_number_score(category_number)) + ")"
    print "overuse number = " + str(overuse_number) + " (expected: 0, score: " + str(get_overuse_score(overuse_number, (row_size - 1) * col_size)) + ")"
    print "covered testcase number = " + str(covered_testcase_number) + " (expected: " + str(settings.case_count) + ", score: " + str(get_covered_testcase_score(covered_testcase_number)) + ")"
    print "final score = " + str(evaluate_matrix_from_numbers(m, covered_api_number, category_number, overuse_number, covered_testcase_number)) + "/" + str(settings.full_score)


def get_matrix_description(m):
    covered_api_number = get_covered_api_number(m)
    category_number = get_category_number(m)
    overuse_number = get_overuse_number(m)[0]
    covered_testcase_number = get_covered_testcase_number(m)

    return "covered APIs: %d/%d, categories: %d, overuse: %d, covered testcases: %d/%d" %\
           (covered_api_number, settings.api_count, category_number, overuse_number, covered_testcase_number, settings.case_count)


def mutate_matrix(m):
    row_size, col_size = m.shape

    for k in range(0, int(row_size * col_size * 0.1)):
        i = random.randint(0, row_size - 1)
        j = random.randint(0, col_size - 1)
        if m[i, j] == 0:
            if random.random() < 1.0 / (settings.category_max_count - 1):
                m[i, j] = 1
        else:
            m[i, j] = 0
            # if random.random() < 0.2:
            #     m[i, j] = 0

    # Clear a random row.
    # if random.random() < 0.5:
    #     i = random.randint(0, row_size - 1)
    #     m[i:] = 0

    # Cover a uncovered testcase.
    if random.random() < 0.8:
        i = random.randint(0, row_size - 1)
        uncovered_testcases = get_uncovered_testcases(m)
        testcase_index = random.randint(0, len(uncovered_testcases) - 1)
        m[i] += settings.test_matrix[uncovered_testcases[testcase_index]]
        m[i] = np.where(m[i] != 0, 1, 0)

    # Make sure we covered all APIs.
    col_sums = m.sum(axis=0)
    for j in range(len(col_sums)):
        if col_sums[j] == 0:
            i = random.randint(0, row_size - 1)
            m[i, j] = 1


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

    # print m
    # m = remove_empty_rows_from_matrix(m)
    # print m

    m[0] = n[0]
    print m
    print n
