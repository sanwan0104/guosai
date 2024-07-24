import requests
import websocket
import json
import pymongo
import time

# 定义基本的URL和参数
base_url = "https://fwwb.dasctf.com//mock/17/slab-match"
match_id = 123
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/46.0.2490.80'}

# 定义一个函数，用于处理JSON格式的响应数据
def handle_json_response(response):
    try:
        response.encoding = 'utf-8'
        data = response.json()
        print(data)
    except json.JSONDecodeError:
        print("Invalid JSON format")

# 定义一个函数，用于处理WebSocket接收到的消息
def handle_ws_message(message):
    try:
        data = json.loads(message)
        print(data)
    except json.JSONDecodeError:
        print("Invalid JSON format")

# 创建一个MongoDB的客户端对象，连接到本地的MongoDB服务器
client = pymongo.MongoClient('mongodb://sxd:sxd123@localhost/sxd')
db = client['sxd']

# 访问或创建集合
notice_col = db['notice']
user_info_col = db['user_info']
game_info_col = db['game_info']
exercise_info_col = db['exercise_info']
event_col = db['event']

# 定义一个函数，用于获取并存储数据
def get_and_store_data():
    # 获取公告信息
    notice_url = base_url + "/notice"
    notice_params = {"matchId": match_id}
    notice_response = requests.get(notice_url, headers=headers)
    handle_json_response(notice_response)
    notice_col.insert_one(notice_response.json())

    # 获取用户信息
    user_info_url = base_url + "/user-info"
    user_info_params = {"matchId": match_id}
    user_info_response = requests.get(user_info_url, headers=headers)
    handle_json_response(user_info_response)
    user_info_col.insert_one(user_info_response.json())

    # 获取竞赛信息
    game_info_url = base_url + "/game-info"
    game_info_params = {"matchId": match_id}
    game_info_response = requests.get(game_info_url, headers=headers)
    handle_json_response(game_info_response)
    game_info_col.insert_one(game_info_response.json())

    # 获取题目信息
    exercise_info_url = base_url + "/exercise-info"
    exercise_info_params = {"matchId": match_id}
    exercise_info_response = requests.get(exercise_info_url, headers=headers)
    handle_json_response(exercise_info_response)
    exercise_info_col.insert_one(exercise_info_response.json())

    # 获取实时事件
    ws_url = "wss://fwwb-ws.dasctf.com:443/ws"
    ws = websocket.WebSocket()
    ws.connect(ws_url)
    message = ws.recv()
    event_data = json.loads(message)
    event_col.insert_one(event_data)
    ws.close()

# 每 5 秒获取并存储数据
while True:
    get_and_store_data()
    time.sleep(5)