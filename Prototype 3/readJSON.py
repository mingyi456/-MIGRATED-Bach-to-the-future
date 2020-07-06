import json

with open('Achievements.json', 'r') as file:
	data = json.load(file)

list_of_strings = []


for i in data:
	for j in i.values():
		list_of_strings.append(str(j))

if __name__ == "__main__":
	for i in data:
		if i["achieved"]:
			print(i["name"], "achieved")
		else:
			print(i["name"], "not achieved")