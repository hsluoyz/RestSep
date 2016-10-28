# coding=gbk

from pprint import pprint
import random

import settings
import test
import ga


capacity = 100
generation = 0
matrix_list = []
score_list = []


def print_list(name_list):
    for i in range(0, len(name_list)):
        # print str(i) + ":\t" + name_list[i]
        print str(i) + ": " + name_list[i]
        i += 1


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


def evaluate_matrix_list():
    global score_list
    score_list = []

    for m in matrix_list:
        score_list.append(int(ga.evaluate_matrix(m)))


def sort_matrix_list():
    global score_list
    global matrix_list

    together = zip(score_list, matrix_list)
    sorted_together = sorted(together, lambda a, b: b[0] - a[0])

    score_list = [x[0] for x in sorted_together]
    matrix_list = [x[1] for x in sorted_together]


def print_result_from_matrix_list():
    print "matrix list of %d instances result, generation = %d, average = %d, max = %d, min = %d" %\
          (len(score_list), generation, sum(score_list) / len(score_list), max(score_list), min(score_list))
    print score_list


def do_init():
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

    ga.print_matrix(settings.test_matrix)

    print "\n*****************************************************"
    print "case list:"
    print_list(settings.case_list)

    print "\n*****************************************************"
    print "API list:"
    print_list(settings.api_list)

    print "\n*****************************************************"
    print "case number = " + str(settings.case_count)
    print "API number = " + str(settings.api_count)


def do_demo():
    m = ga.init_random_matrix(settings.category_max_count, settings.api_count)

    ga.print_matrix(m)

    print "\n*****************************************************"
    print "After mutation:"

    ga.mutate_matrix(m)
    ga.print_matrix(m)

    # print "\n*****************************************************"
    # evaluate_matrix(m)

    # print_result_from_matrix(m)

    # a = [1, 32]
    # b = [3, 4]
    # c = np.array([a, b])
    #
    # print c[:,1]

    # print c


# 20% - mutate
# 40% - no change
# 40% - crossover
def do_evolve():
    mutate_ratio = 0.2
    crossover_ratio = 0.4

    global generation
    generation += 1
    random.shuffle(matrix_list)
    for i in range(0, int(mutate_ratio * capacity)):
        ga.mutate_matrix(matrix_list[i])
    for i in range(int((1 - crossover_ratio) * capacity), capacity, 2):
        matrix_list.append(ga.crossover_matrix(matrix_list[i], matrix_list[i + 1]))

    evaluate_matrix_list()
    sort_matrix_list()
    eliminate_size = int(crossover_ratio / 2 * capacity)
    del matrix_list[-eliminate_size:]
    del score_list[-eliminate_size:]


if __name__ == '__main__':
    do_init()
    do_demo()

    for i in range(capacity):
        matrix_list.append(ga.init_random_matrix(settings.category_max_count, settings.api_count))
    evaluate_matrix_list()
    sort_matrix_list()
    print "\n*****************************************************"
    print_result_from_matrix_list()

    for i in range(100):
        do_evolve()
        print_result_from_matrix_list()
