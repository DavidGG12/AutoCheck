import json
import os

current_file = os.path.abspath(__file__)
current_file_folder = os.path.dirname(current_file)

print(current_file_folder)



with open(fr"{current_file_folder}\appsettings.json") as f:
    d = json.load(f)
    print(d)

print(d["Users"]["SessionUser"])