# coding=gbk

from pprint import pprint

import settings
import test
import ga


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

if __name__ == '__main__':
    do_init()
    do_demo()
