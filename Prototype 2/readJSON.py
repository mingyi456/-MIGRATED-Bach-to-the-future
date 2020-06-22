import json

with open('Achievements.json', 'r') as file:
	data = json.load(file)

print(data)