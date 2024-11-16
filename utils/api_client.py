import requests


a = requests.get(
    "https://data.tronk.info/convertb2b.ashx?key=cf6ceeb3-f69c-400b-82c0-95df925fb4ee&gosnumber=М523РВ32"
)

print(a)
print(a.content)
print(a.json())
