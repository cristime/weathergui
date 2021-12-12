import json

data = {}

with open("temp.txt", "r") as f:
    i = 1
    for line in f:
        if i == 2:
            i = 1
            continue
        cityName = line.split(",")[0]
        cityCode = line.split(",")[1].split("\n")[0]
        data[cityName] = cityCode
        i = i + 1

with open("citycode.json", "w") as f:
    json.dump(data, f)
