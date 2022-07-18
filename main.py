import json
from datetime import datetime, timedelta
from tkinter import dialog


HARDCODE_PATH = "test_hello_world/"
TG_DATE_FORMAT = '%Y-%m-%dT%H:%M:%S'
MAX_WAITING_TIME_M  = int(30)

def open_json(file_path):
    with open(HARDCODE_PATH+file_path, "r", encoding='utf-8') as read_file:
        return json.load(read_file, cls= json.JSONDecoder)

def parse_date_string(str):
    return datetime.strptime(str, TG_DATE_FORMAT)

chat = open_json("result.json")
messages = chat["messages"]

dialog_stack = []
dialogs = []
dialog_id_counter = 0

for message in messages:
    if(len(dialog_stack) == 0):
        dialog_stack.append(message)
        continue
    top_date = parse_date_string(dialog_stack[len(dialog_stack)-1]["date"])
    current_date = parse_date_string(message["date"])
    date_delta = current_date - top_date
    if(date_delta < timedelta(seconds=MAX_WAITING_TIME_M*60)):
        dialog_stack.append(message)
    else:
        dialog = {
            'id': dialog_id_counter,
            'start_msg_id': dialog_stack[0]["id"],
            'end_msg_id': dialog_stack[len(dialog_stack)-1]["id"]
        }
        dialogs.append(dialog)
        dialog_stack.clear()
        dialog_stack.append(message)
        inc(dialog_id_counter)

if(len(dialog_stack) != 0):
    dialog = {
            'id': dialog_id_counter,
            'start_msg_id': dialog_stack[0]["id"],
            'end_msg_id': dialog_stack[len(dialog_stack)-1]["id"]
        }
    dialogs.append(dialog)
    dialog_stack.clear()

print(json.dumps(dialogs, indent=4))




