import config
from importlib import reload

print(dir(config))

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

ch_config("FPS", 60)

