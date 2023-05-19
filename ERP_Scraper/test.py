import json
from collections import defaultdict

with open("op.json") as jsonf:
    dct=defaultdict(float)
    data=json.load(jsonf)
    for i in data:
        if "name" in i and len(i)>1:
            try:
                dct[i["name"]]+=float(i["awarded"])
            except Exception as e:
                print(i["name"], i["component"])
    print(dct)