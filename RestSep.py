# coding=gbk

import re
from pprint import pprint
import numpy as np
import random


test_dict = {}
case_list = []
api_list = []

def method_path_to_string(method, path):
    return path + " | " + method


def init_from_test():
    pattern_uuid = "[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
    regex_uuid = re.compile(pattern_uuid)

    pattern_id = "[0-9a-f]{32}"
    regex_id = re.compile(pattern_id)

    keywords = [
        # Nova
        "flavors",
        "os-extra_specs",
        "images",
        "os-agents",
        "os-aggregates",
        "os-hosts",
        "os-hypervisors",
        "os-instance_usage_audit_log",
        "os-keypairs",
        "os-quota-sets",
        "os-security-groups",
        "os-simple-tenant-usage",
        "os-volumes",
        "servers",

        "os-fixed-ips",
        "os-security-group-default-rules",

        # Cinder
        "extra_specs",
    ]

    pattern_name = "("
    for keyword in keywords:
        pattern_name += (keyword + "/|")
    pattern_name = pattern_name[:-1]
    pattern_name += ")[^/]+"

    # print "pattern_name = " + pattern_name

    # pattern_name = "(os-simple-tenant-usage/|os-quota-sets/|flavors/|servers/|os-agents/|os-aggregates/|os-fixed-ips/
    # |os-extra_specs/|os-hosts/|os-hypervisors/)[^/]+"
    regex_name = re.compile(pattern_name)

    filepath = "J:/OpenStack国家863项目/我的论文/RestSep/实验数据/"
    # filename = "stack.log.keystone"
    filename = "stack.log.nova"
    # filename = "stack.log.glance"
    # filename = "stack.log.cinder"

    current_line = ""

    for line in open(filepath + filename):
        # print "AAA" + line + "BBB"
        if line.startswith("#"):
            line = line.strip("\n").strip("#")

            # print "\n*****************************************************"
            # print line
            # print "*****************************************************"

            current_line = line

            case_list.append(line)

        elif line.startswith("2"):
            tmp_list = line.strip("\n").split('\t')
            method = tmp_list[1]
            path = tmp_list[2]

            # print method + " | " + path

            path = path[path.find("128:") + 4:]
            path = path.replace("8774", "NOVA")
            path = path.replace("9696", "NEUTRON")
            path = path.replace("9292", "GLANCE")
            path = path.replace("8776", "CINDER")
            path = path.replace("8004", "HEAT")
            path = path.replace("8777", "CEILOMETER")
            path = path.replace("5000", "KEYSTONE")

            path = path.replace("NOVA/v2.1/", "")
            path = path.replace("GLANCE/v1/", "")

            path = path.replace("/detail", "")

            question_mark = path.find("?")
            if question_mark != -1:
                path = path[:question_mark]

            path = regex_uuid.sub("%UUID%", path)
            path = regex_id.sub("%NAME%", path)
            path = regex_name.sub("\\1%NAME%", path)

            # print method + " | " + path

            if not test_dict.has_key(current_line):
                test_dict[current_line] = {}
            if not test_dict[current_line].has_key(method_path_to_string(method, path)):
                test_dict[current_line][method_path_to_string(method, path)] = 0
            test_dict[current_line][method_path_to_string(method, path)] += 1

            api_list.append(method_path_to_string(method, path))


def print_list(name_list):
    for i in range(0, len(name_list)):
        # print str(i) + ":\t" + name_list[i]
        print str(i) + ": " + name_list[i]
        i += 1


def init_test_matrix():
    m = np.zeros((case_count, api_count), dtype=np.int)
    for i in range(0, case_count):
        for j in range(0, api_count):
            if test_dict[case_list[i]].has_key(api_list[j]):
                # m[i, j] = test_dict[case_list[i]][api_list[j]]
                # We do not calculate the occurrence for now.
                m[i, j] = 1
    return m


def unique_rows(a):
    a = np.ascontiguousarray(a)
    unique_a = np.unique(a.view([('', a.dtype)]*a.shape[1]))
    return unique_a.view(a.dtype).reshape((unique_a.shape[0], a.shape[1]))


def cleanse_test_matrix(m, case_list):
    row_size, col_size = m.shape

    new_m = unique_rows(m)
    new_row_size, _ = new_m.shape
    # print_matrix(new_m)
    new_case_list = [""] * new_row_size

    for i in range(0, row_size):
        for i2 in range(0, new_row_size):
            if tuple(m[i, :]) == tuple(new_m[i2, :]):
                new_case_list[i2] += case_list[i] + ", "

    for i in range(0, len(new_case_list)):
        new_case_list[i] = new_case_list[i].rstrip(', ')

    #print_list(new_case_list)

    return new_m, new_case_list


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


init_from_test()

# Print the test dictionary.
# pprint(test_dict)

# Initialize the test case list.
case_list = list(set(case_list))
case_list.sort()
case_count = len(case_list)

# Initialize the API list.
api_list = list(set(api_list))
api_list.sort()
api_count = len(api_list)

# Initialize the test matrix.
test_matrix = init_test_matrix()

# Remove the duplicated rows in the test matrix.
print "\n*****************************************************"
print "cleansed test matrix:"
test_matrix, case_list = cleanse_test_matrix(test_matrix, case_list)
case_count = len(case_list)

print_matrix(test_matrix)


print "\n*****************************************************"
print "case list:"
print_list(case_list)


print "\n*****************************************************"
print "API list:"
print_list(api_list)



print "\n*****************************************************"
print "case number = " + str(case_count)
print "API number = " + str(api_count)


m = init_random_matrix(api_count / 4, api_count)

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

