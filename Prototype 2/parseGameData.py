import json

with open('gamedata.json') as file:
	data = json.load(file)
	# print(data['Settings'])
	# print(data['Users'])

Settings = data['Settings']
Users = data['Users']

print(Users['David']['Achievements'])
print(Users['David']['Highscores'])
Users['David']['Highscores']['Sarabande'] = -999
print(Users['David']['Highscores'])

with open('gamedata.json', 'w+') as file:
	json.dump(data, file, indent=4)