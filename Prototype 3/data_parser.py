import json

with open('gamedata.json') as file:
	data = json.load(file)

def get_sys_config(data_file= "gamedata.json"):
	with open(data_file) as file:
		data = json.load(file)
	
	return data["System"]

def get_config(data_file= "gamedata.json"):
	with open(data_file) as file:
		data = json.load(file)
	
	config= data["Settings"]
	return config

def ch_config(key, new_val):
	try:
		data["Settings"][key]["Value"]= new_val
		save_json(data)
	except:
		print("Failed!")
		return -1

def get_user_data(data_file= "gamedata.json"):
	with open(data_file) as file:
		data = json.load(file)
	
	user_data= data["Users"]["Guest"]
	return user_data

def update_user_data(key, new_val):
	try:
		data["Users"]["Guest"][key[0]][key[1]]= new_val
		save_json(data)
	except:
		print("Failed!")
		return -1		


def save_json(data= data, data_file= "gamedata.json"):
	try:
		with open(data_file, 'w+') as file:
			json.dump(data, file, indent=4)
		print("Save successful!")
	except:
		print("Failed!")
		return -1




