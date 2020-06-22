import json

with open('Achievements.json', 'r') as file:
	data = json.load(file)

list_of_strings = []

for i in data:
	for j in i.values():
		list_of_strings.append(str(j))

print(list_of_strings)