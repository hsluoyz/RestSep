# coding=gbk

from pprint import pprint
import random
import multiprocessing

import settings
import test
import ga
import threading
import cPickle as pickle

mutate_ratio = 0.2
crossover_ratio = 0.4
population = 160
population_limit = int((1 + crossover_ratio / 2) * population)
generation_count = 30000

thread_pool = None

generation = 0
matrix_list = []
score_list = []
top_score = 0
top_title = ''
max_score = 0
min_score = 0

temp_data_path = "temp.data"

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


def sort_matrix_list():
    global score_list
    global matrix_list

    together = zip(score_list, matrix_list)
    sorted_together = sorted(together, lambda a, b: b[0] - a[0])

    score_list = [x[0] for x in sorted_together]
    matrix_list = [x[1] for x in sorted_together]


def print_result_from_matrix_list():
    global max_score, min_score

    valid_score_list = score_list[:population]
    max_score = max(valid_score_list)
    min_score = min(valid_score_list)

    print "matrix list of %d instances result, generation = %d, average = %d, max = %d, min = %d" %\
          (len(valid_score_list), generation, sum(valid_score_list) / len(valid_score_list), max_score, min_score)
    # print valid_score_list
    print ga.get_uncovered_testcases(matrix_list[0])


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
    # settings.test_matrix, settings.case_list = test.cleanse_test_matrix2(settings.test_matrix, settings.case_list)
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


def do_init_generation():
    global score_list

    for i in range(population_limit):
        matrix_list.append(ga.init_random_matrix(settings.category_max_count, settings.api_count))
    score_list = [0] * population_limit
    # do_evaluate()
    # sort_matrix_list()
    # print "\n*****************************************************"
    # print_result_from_matrix_list()

    # init_thread_pool()


def do_mutate(start, end):
    for i in range(start, end):
        ga.mutate_matrix(matrix_list[i])
        # Evaluate the matrix: i
        score_list[i] = int(ga.evaluate_matrix(matrix_list[i]))


def do_crossover(start, end):
    for i in range(start, end, 2):
        new_i = population + int((i - (1 - crossover_ratio) * population) / 2)
        matrix_list[new_i] = ga.crossover_matrix(matrix_list[i], matrix_list[i + 1])
        # Evaluate the matrix: new_i
        score_list[new_i] = int(ga.evaluate_matrix(matrix_list[new_i]))


def do_evaluate(start, end):
    global score_list

    for i in range(start, end):
        score_list[i] = int(ga.evaluate_matrix(matrix_list[i]))


# def do_eliminate():
#     eliminate_size = len(matrix_list) - population
#     del matrix_list[-eliminate_size:]
#     del score_list[-eliminate_size:]


# 20% - mutate
# 40% - crossover
# 40% - no change
def do_evolve_once():
    global generation
    generation += 1

    # random.shuffle(matrix_list)
    matrix_list[:population] = random.sample(matrix_list[:population], population)
    # matrix_list[int((1 - crossover_ratio - mutate_ratio) * population):population] =\
    #    random.sample(matrix_list[int((1 - crossover_ratio - mutate_ratio) * population):population], int((crossover_ratio + mutate_ratio) * population))

    do_mutate(0, int(mutate_ratio * population))
    # do_mutate(int((1 - crossover_ratio - mutate_ratio) * population), int((1 - crossover_ratio) * population))
    do_crossover(int((1 - crossover_ratio) * population), population)
    # do_evaluate(0, population_limit)

    sort_matrix_list()
    # do_eliminate()


def init_thread_pool():
    global thread_pool
    thread_pool = multiprocessing.Pool(processes=10)


def do_evolve_once_multi_thread():
    global generation
    generation += 1

    matrix_list[:population] = random.sample(matrix_list[:population], population)

    thread_pool.apply_async(do_mutate, (0, int(mutate_ratio * population)))
    thread_pool.apply_async(do_crossover, (int((1 - crossover_ratio) * population), population))

    # thread_pool.close()
    # thread_pool.join()

    # do_mutate(0, int(mutate_ratio * population))
    # do_crossover(int((1 - crossover_ratio) * population), population)

    sort_matrix_list()


def do_evolve_generation(set_data_func, set_title_func):
    global top_score, top_title

    for i in range(generation_count):
        do_evolve_once()
        # do_evolve_once_multi_thread()
        print_result_from_matrix_list()
        if set_data_func:
            if top_score < score_list[0]:
                top_score = score_list[0]
                reduced_top_matrix = ga.get_reduced_matrix(matrix_list[0])
                top_title = "top generation: %d, top score: %d/%d, %s" % (i + 1, top_score, settings.full_score, ga.get_matrix_description(reduced_top_matrix))
                set_data_func(ga.remove_empty_rows_from_matrix(2 * matrix_list[0] - reduced_top_matrix))
            set_title_func("input: %s, population: %d, min/max: (%d, %d), current: %d/%d, %s" % (settings.filename, population, min_score, max_score, i + 1, generation_count, top_title))


class Data(object):
    def __init__(self, _generation, _matrix_list, _score_list, _top_score, _top_title):
        self.generation = _generation
        self.matrix_list = _matrix_list
        self.score_list = _score_list
        self.top_score = _top_score
        self.top_title = _top_title


class MyThread(threading.Thread):
    def __init__(self, set_data_func, set_title_func, _save_file_path=temp_data_path):
        super(MyThread, self).__init__()
        self.stopped = False
        self.set_data_func = set_data_func
        self.set_title_func = set_title_func
        self.cur_count = generation
        self.save_file_path = _save_file_path
        # 判断是否从上次中断的结果继续运行，还是直接重新运行
        with open(self.save_file_path, "r") as temp_file:
            content = temp_file.read().strip()
            if content != "":
                f = file(self.save_file_path, 'rb')
                data = pickle.load(f)
                global generation, matrix_list, score_list, top_score, top_title
                generation = data.generation
                matrix_list = data.matrix_list
                score_list = data.score_list
                top_score = data.top_score
                top_title = data.top_title
                self.cur_count = generation

    def stop(self, _save_file_path):
        self.stopped = True
        self.save_file_path = _save_file_path

    def run(self):
        do_init_generation()
        global top_score, top_title
        is_stopped = False
        for i in range(self.cur_count, generation_count):
            print("%dth iteration" % i)
            if self.stopped:
                is_stopped = True
                break
            else:
                do_evolve_once()
                print_result_from_matrix_list()
                if self.set_data_func and top_score < score_list[0]:
                    top_score = score_list[0]
                    top_title = "top generation: %d, top score: %d, %s" % (i + 1, top_score, ga.get_matrix_description(matrix_list[0]))
                    self.set_data_func(ga.remove_empty_rows_from_matrix(matrix_list[0]))
                self.set_title_func("input: %s, population: %d, current: %d/%d, %s" % (settings.filename, population, i + 1, generation_count, top_title))

        if is_stopped:
            print("sub thread is stopped!")
            # 构造data对象
            data = Data(generation, matrix_list, score_list, top_score, top_title)
            # 序列化到temp.data
            f = open(self.save_file_path, 'wb')
            pickle.dump(data, f)
            f.close()
            del data
            print("serialize into file")
        else:
            print("done")

if __name__ == '__main__':
    do_init()
    do_demo()

    do_init_generation()
    do_evolve_generation(None, None)
