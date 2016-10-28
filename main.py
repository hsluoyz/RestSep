# coding=gbk

from pprint import pprint
import numpy as np
import random

import settings
import test


def print_list(name_list):
    for i in range(0, len(name_list)):
        # print str(i) + ":\t" + name_list[i]
        print str(i) + ": " + name_list[i]
        i += 1


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


def init_random_matrix(row_size, col_size):
    m = np.zeros((row_size, col_size), dtype=np.int)
    for j in range(0, col_size):
        m[random.randrange(0, row_size, 1), j] = 1
    return m


def print_result_from_matrix(m):
    row_size, col_size = m.shape
    res = []

    for i in range(0, row_size):
        row_api_list = []
        for j in range(0, col_size):
            if m[i, j] == 1:
                row_api_list.append(settings.api_list[j])
        if len(row_api_list) != 0:
            res.append(row_api_list)

    pprint(res)
    print "Category number = " + str(len(res))


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


test.init_from_test()

# Print the test dictionary.
# pprint(test_dict)

test.init_lists()


# Initialize the test matrix.
settings.test_matrix = test.init_test_matrix()

print "\n*****************************************************"
print "cleansed test matrix:"
# Remove the duplicated rows in the test matrix.
settings.test_matrix, settings.case_list = test.cleanse_test_matrix(settings.test_matrix, settings.case_list)
# Remove the shadow-covered rows in the test matrix.
settings.test_matrix, settings.case_list = test.cleanse_test_matrix2(settings.test_matrix, settings.case_list)
settings.case_count = len(settings.case_list)

print_matrix(settings.test_matrix)


print "\n*****************************************************"
print "case list:"
print_list(settings.case_list)


print "\n*****************************************************"
print "API list:"
print_list(settings.api_list)


print "\n*****************************************************"
print "case number = " + str(settings.case_count)
print "API number = " + str(settings.api_count)


m = init_random_matrix(settings.api_count / 4, settings.api_count)

print_matrix(m)

# print "\n*****************************************************"
# evaluate_matrix(m)


# print_result_from_matrix(m)

# a = [1, 32]
# b = [3, 4]
# c = np.array([a, b])
#
# print c[:,1]

# print c

