import json


def t():
    with open("local.json") as f:
        data = json.load(f)
        print(data[0])
        # hn = filter(lambda c: c['id'] == "1", data)
        # import pdb; pdb.set_trace()
        # print(hn)
t()