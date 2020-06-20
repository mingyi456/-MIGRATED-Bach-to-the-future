import config
from importlib import reload

def ch_config(key, new_val):
	try:
		old_val= eval(f"config.{key}")
	except:
		print("Key does not exist!")
		return

	file= open("config.py", 'r')
	file_str= file.read()
	new_file_str= file_str.replace(f"{key}= {old_val}", f"{key}= {new_val}", 1)
	exec(f"config.{key}= new_val")

	file.close()
	file= None
	file= open("config.py", 'w')
	file.write(new_file_str)
	file.close()
	reload(config)

if __name__ == "__main__":
	configs= dir(config)
	print(configs)
	for i, setting in enumerate(configs):
		val= eval(f"config.{setting}")
		print(i, f"{setting} = {val}")

	ch_config("FPS", 60)

