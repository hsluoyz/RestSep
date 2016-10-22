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
                row_api_list.append(api_list[j])
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


def evaluate_matrix(m):
    row_size, col_size = m.shape
    score_overlap = m.sum() - col_size
    print "score_overlap = " + str(score_overlap)


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

print "\n*****************************************************"
evaluate_matrix(m)

print "category number = " + str(get_category_number(m))

# print_result_from_matrix(m)

# a = [1, 32]
# b = [3, 4]
# c = np.array([a, b])
#
# print c[:,1]

# print c

