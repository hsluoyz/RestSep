# coding=gbk

import re

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

# pattern_name = "(os-simple-tenant-usage/|os-quota-sets/|flavors/|servers/|os-agents/|os-aggregates/|os-fixed-ips/|os-extra_specs/|os-hosts/|os-hypervisors/)[^/]+"
regex_name = re.compile(pattern_name)


filepath = "J:/OpenStack����863��Ŀ/�ҵ�����/RestSep/ʵ������/"
# filename = "stack.log.keystone"
filename = "stack.log.nova"
# filename = "stack.log.glance"
# filename = "stack.log.cinder"


class Entry:
    method = ""
    path = ""
    count = 0

    def __init__(self, method, path):
        self.method = method
        self.path = path
        self.count = 1
        self.count_maps = {}
        self.grouphead = None

entries = []
grouphead_entry = None

for line in open(filepath + filename):
    # print "AAA" + line + "BBB"
    if line.startswith("#"):
        line = line.strip("\n").strip("#")

        # print "\n*****************************************************"
        # print line
        # print "*****************************************************"

        entry = Entry("", line)
        entries.append(entry)
        grouphead_entry = entry

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

        path = path.replace("/detail", "")

        question_mark = path.find("?")
        if question_mark != -1:
            path = path[:question_mark]

        path = regex_uuid.sub("%UUID%", path)
        path = regex_id.sub("%NAME%", path)
        path = regex_name.sub("\\1%NAME%", path)

        # print method + " | " + path

        if not grouphead_entry.count_maps.has_key(method + " | " + path):
            entry = Entry(method, path)
            entries.append(entry)
            grouphead_entry.count_maps[method + " | " + path] = 0
            entry.grouphead = grouphead_entry
        grouphead_entry.count_maps[method + " | " + path] += 1

# Print the entries.
for entry in entries:
    if entry.method == "":
        print "\n*****************************************************"
        print entry.path
        print "*****************************************************"
    else:
        entry.count = entry.grouphead.count_maps[entry.method + " | " + entry.path]
        print entry.method + " | " + entry.path + " | " + str(entry.count)