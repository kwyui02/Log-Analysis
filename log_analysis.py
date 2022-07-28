#!/usr/bin/env python3

import re
import operator
import csv

error = {}
per_user = {}

with open("syslog.log") as f:
    loglines = f.readlines()
    for line in loglines:
        error_desc = re.search(r"ticky: ERROR (.*)\s\(", line)
        user_match = re.search(r" \(([\w\. ]*)\)", line)

        # error
        if error_desc != None:
            if error_desc.group(1) not in error.keys():
                error[error_desc.group(1)] = 1
            else:
                error[error_desc.group(1)] += 1

        # per_user
        if user_match.group(1) not in per_user.keys():
            # initialize key
            per_user[user_match.group(1)] = {}
            per_user[user_match.group(1)]["INFO"] = 0
            per_user[user_match.group(1)]["ERROR"] = 0
            if error_desc != None:  # ERROR
                per_user[user_match.group(1)]["ERROR"] = 1
            else:  # INFO
                per_user[user_match.group(1)]["INFO"] = 1
        else:
            if error_desc != None:  # ERROR
                per_user[user_match.group(1)]["ERROR"] += 1
            else:  # INFO
                per_user[user_match.group(1)]["INFO"] += 1

        # sort error
        error_list = sorted(
            error.items(), key=operator.itemgetter(1), reverse=True)
        # insert header
        error_list.insert(0, ('Error', 'Count'))
        # sort per_user
        per_user_list = sorted(per_user.items(), key=operator.itemgetter(0))
        # insert the header
        per_user_list.insert(0, ('Username', {'INFO', 'ERROR'}))

with open("error_message.csv", "w") as f:
    writer = csv.writer(f)
    for key, value in error_list:
        writer.writerow([key, value])

with open("user_statistics.csv", "w") as f2:
    writer = csv.writer(f2)
    for statsList in per_user_list:
        username = statsList[0]
        statsDict = statsList[1]
        if username != "Username":
            a, b = statsDict.values()
            writer.writerow([username, a, b])
