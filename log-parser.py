import os
import re
import json
import argparse
from collections import defaultdict


def parse_arguments():
    parser = argparse.ArgumentParser(description='Analysis access.log')
    parser.add_argument('-path', dest='file', action='store', help='Path to log file')
    return parser.parse_args()


def file_or_directory(path):
    _path_to_logfiles = []
    if os.path.isfile(path.file):
        return path.file

    elif os.path.isdir(path.file):
        for file in os.listdir(path.file):
            if file.endswith(".log"):
                _path_to_logfile = os.path.join(path.file, file)
                _path_to_logfiles.append(_path_to_logfile)
        return _path_to_logfiles

    else:
        print("ERROR: Incorrect path to log file or directory")


def parse_log_file(log_file):
    count_request = {"COUNT_REQUEST": 0, "METHOD": {"GET": 0, "POST": 0, "PUT": 0, "DELETE": 0, "HEAD": 0, "OPTIONS": 0}}
    dict_ip_requests = defaultdict(int)
    list_ip_duration = []

    with open(log_file) as logfile:
        for line in logfile:
            ip_match = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", line).group()
            method = re.search(r"\] \"(POST|GET|PUT|DELETE|HEAD|OPTIONS)", line)
            duration = int(line.split()[-1])
            date = re.search(r"\[\d.*?\]", line)
            url = re.search(r"\"http.*?\"", line)
            count_request["COUNT_REQUEST"] += 1
            if method:
                count_request["METHOD"][method.group(1)] += 1
                dict_ip_requests[ip_match] += 1
                dict_data_request = {"METHOD": method.group(1), "URL": "None", "IP": ip_match, "DURATION": duration,
                                     "DATE": date.group(0).split(" ")[0].lstrip("[")}
                if url:
                    dict_data_request["URL"] = url.group(0).strip("\"")

                list_ip_duration.append(dict_data_request)

        top_3_ip = dict(sorted(dict_ip_requests.items(), key=lambda x: x[1], reverse=True)[0:3])
        top_3_longest_requests = sorted(list_ip_duration, key=lambda x: x["DURATION"], reverse=True)[0:3]

        result = {"count_request": count_request["COUNT_REQUEST"],
                  "count_stat_method": count_request["METHOD"],
                  "top_3_ip": top_3_ip,
                  "top_3_longest_requests": top_3_longest_requests
                  }
    return write_json_file(log_file, result)


def write_json_file(name_file, data):
    with open(f"{name_file[:-4]}_result.json", "w", encoding="utf-8") as result_file:
        result = json.dumps(data, indent=4)
        result_file.write(result)
        print(f" Result file: {name_file[:-4]}.json \n {result}")


if __name__ == '__main__':
    path_files = parse_arguments()
    selected_files = file_or_directory(path_files)
    if isinstance(selected_files,
                  list):
        for path_f in selected_files:
            parse_log_file(path_f)
    else:
        parse_log_file(selected_files)
