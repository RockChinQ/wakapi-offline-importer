import os
import sys
import json
import pymysql
import re
import hashlib
import datetime

file_name = sys.argv[1]
user_id = sys.argv[2]
db_host = sys.argv[3]
db_user = sys.argv[4]
db_pass = sys.argv[5]
db_name = sys.argv[6]
start_date = datetime.datetime.strptime(sys.argv[7], '%Y-%m-%d')
user_agent_file = sys.argv[8]
machine_name_file = sys.argv[9]

# Read the file
file_obj: dict = {}

with open(file_name, 'r') as file:
    file_obj = json.load(file)

# Connect to the database
connection = pymysql.connect(host=db_host, user=db_user, password=db_pass, database=db_name)
cursor = connection.cursor()

# Read the user agent file
user_agent_dict = {}

with open(user_agent_file, 'r') as file:
    ua_file = json.load(file)

    for ua in ua_file['data']:
        user_agent_dict[ua['id']] = {
            "os": ua['os'],
            "editor": ua['editor']
        }

def get_os_editor(ua_id: str):
    if ua_id in user_agent_dict:
        return user_agent_dict[ua_id]
    else:
        return {
            "os": "Unknown",
            "editor": "Unknown"
        }
    
# Read the machine name file
machine_name_dict = {}

with open(machine_name_file, 'r') as file:
    mn_file = json.load(file)

    for mn in mn_file['data']:
        machine_name_dict[mn['id']] = mn['name']

def get_machine_name(mn_id: str):
    if mn_id in machine_name_dict:
        return machine_name_dict[mn_id]
    else:
        return "Unknown"

for data in file_obj['days']:

    print(data['date'])

    ddate = datetime.datetime.strptime(data['date'], '%Y-%m-%d')

    if ddate < start_date:
        continue

    # 关闭自动提交
    connection.autocommit(False)

    # id	user_id	entity	type	category	project	branch	language	is_write	editor	operating_system	machine	user_agent	time	hash	origin	origin_id	created_at
    amount = 0
    sql_this_day = """

INSERT INTO
    `heartbeats`
    (user_id, entity, type, category, project, branch, language, is_write, editor, operating_system, machine, user_agent, time, hash, origin, origin_id, created_at)
VALUES
"""
    hash_list = []
    for heartbeats in data['heartbeats']:
        os_editor = get_os_editor(heartbeats['user_agent_id'])
        os_name = os_editor['os']
        editor = os_editor['editor']

        machine_name = get_machine_name(heartbeats['machine_name_id'])

        time_str = datetime.datetime.fromtimestamp(int(heartbeats['time'])).strftime('%Y-%m-%d %H:%M:%S')

        # 从整个数据的str算md5取前17位
        hash = hashlib.md5(str(heartbeats).encode()).hexdigest()[:17]

        if hash in hash_list:
            continue

        hash_list.append(hash)

        sql_this_day += f"('{user_id}', '{heartbeats['entity']}', '{heartbeats['type']}', '{heartbeats['category']}', '{heartbeats['project']}', '{heartbeats['branch']}', '{heartbeats['language']}', {1 if heartbeats['is_write'] else 0}, '{editor}', '{os_name}', '{machine_name}', '{heartbeats['user_agent_id']}', '{time_str}', '{hash}', '', '', '{time_str}'),"

        amount += 1

    if amount == 0:
        continue

    sql_this_day = sql_this_day[:-1] + ';'
    cursor.execute(sql_this_day)

    print(f"done: {amount}, commit?")

    connection.commit()

cursor.close()