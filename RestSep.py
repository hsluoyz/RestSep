# coding=gbk

import re
from pprint import pprint
import numpy as np


test_matrix = {}
api_set = set()
api_array = []

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

            if not test_matrix.has_key(current_line):
                test_matrix[current_line] = {}
            if not test_matrix[current_line].has_key(method_path_to_string(method, path)):
                test_matrix[current_line][method_path_to_string(method, path)] = 0
            test_matrix[current_line][method_path_to_string(method, path)] += 1

            api_set.add(method_path_to_string(method, path))


def print_matrix(matrix):
    x_count, y_count = matrix.shape
    res = ""
    for y in range(0, y_count):
        for x in range(x_count):
            res += str(matrix[x, y])
        res += '\n'
    print res

init_from_test()

# Print the integration test matrix.
pprint(test_matrix)

# Print the APIs.

api_array = list(api_set)
api_array.sort()

for i in range(0, len(api_array)):
    print str(i) + ":\t" + api_array[i]
    i += 1

api_count = len(api_array)

print "Test case number = " + str(len(test_matrix))
print "API number = " + str(api_count)

# matrix_np = np.array(matrix)

m = np.ones((api_count, api_count), dtype=np.int)
print_matrix(m)

# a = [1, 32]
# b = [3, 4]
# c = np.array([a, b])
#
# print c[:,1]

# print c

