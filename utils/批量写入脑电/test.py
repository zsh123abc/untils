import requests

cookies = {
    'Admin-Token': 'b4T0hQV5+OOu7ABM6utLigG5QvTkTfiTdhQ6uGDLHk0zKGYbUZm2tc/ZKx0FH7pX2/4JNK8ueZFK5tabvYQ9ugk81PamieS722Svs4xAdHjcAriPZhBMOYTc7F6x+ZWa7uM/URkJU1GFRNHakQsq0A==',
    'sidebarStatus': '0',
}

headers = {
    'Host': 'admin-brain.17yund.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Content-Type': 'application/json;charset=utf-8',
    'Authorization': 'Bearer b4T0hQV5+OOu7ABM6utLigG5QvTkTfiTdhQ6uGDLHk0zKGYbUZm2tc/ZKx0FH7pX2/4JNK8ueZFK5tabvYQ9ugk81PamieS722Svs4xAdHjcAriPZhBMOYTc7F6x+ZWa7uM/URkJU1GFRNHakQsq0A==',
    'Origin': 'http://admin-brain.17yund.com',
    # Requests sorts cookies= alphabetically
    # 'Cookie': 'Admin-Token=b4T0hQV5+OOu7ABM6utLigG5QvTkTfiTdhQ6uGDLHk0zKGYbUZm2tc/ZKx0FH7pX2/4JNK8ueZFK5tabvYQ9ugk81PamieS722Svs4xAdHjcAriPZhBMOYTc7F6x+ZWa7uM/URkJU1GFRNHakQsq0A==; sidebarStatus=0',
}

json_data = {
    'userId': 137,
    'familyMemberId': 516,
    'beginAt': '680',
    'endAt': '2080',
    'labelId': '5',
    'logDataId': 3382,
}

response = requests.post('http://admin-brain.17yund.com/api/brain/data/logLabels/add', cookies=cookies, headers=headers, json=json_data)

