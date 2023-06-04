import requests
import pyfiglet
import colorama
import time
import json
import os
import signal
import sys
from colorama import Fore, Back, Style, init
init()
if not os.path.exists('nanoleafsupport.json'):
	print(" ****  NANOLEAF CLI INITAL SETUP ****  ")
	print("")
	print("")
	nanoip = input("Nanoleaf Panel private IP address? ")
	print("")
	print("Thanks. For the next part, we need to generate an authorization token.")
	print("Please go over to your panel physical control panel, and hold the power")
	print("button for 5-7 seconds until the panel starts blinking. When it does,")
	print("hit enter. If nothing appears, your computer could not connect. In that")
	print("case, restart the program by hitting control+C and rerunning. If it works,")
	print('It should be a JSON dump that looks like, {"authtoken": "something"}. What')
	print("You are looking for in this case is the 'something'. ")
	input("")
	os.system(f"curl --location --request POST 'http://{nanoip}:16021/api/v1/new'")
	authtoken = input("Enter the generated authoken: ")
	var_val = {
		'nanoip': f'{nanoip}',
		'authtoken': f'{authtoken}'
	}
	while True:
		continue = input("Are you 100% sure these values are ABSOLUTELY CORRECT? (y/n): ")
		if continue == "y":
			print("Ok... ")
			break
		elif continue == "n":
			sys.exit()
		else:
			print("Invalid. Put, 'y' for yes or 'n' for no. ")
	with open('nanoleafsupport.json', 'w') as file:
		json.dump(var_val, file)
else:
	with open('nanoleafsupport.json', 'r') as file:
		var_val = json.load(file)
global nanoip
nanoip = var_val['nanoip']
global authtoken
authtoken = var_val['authtoken']
user_interrupt_occured = False
def user_interrupt(signal, frame):
	global user_interrupt_occured
	user_interrupt_occured = True
	print("")
	print(Fore.RED + "Program stopped." + Fore.RESET)
	print("")
	sys.exit()
signal.signal(signal.SIGINT, user_interrupt)
def type_text(text):
	for char in text:
		print(char, end='', flush=True)
		time.sleep(0.001)
	print("")
def type_text_slow(text):
	for char in text:
		print(char, end='', flush=True)
		time.sleep(0.05)
	print("")
def loading_screen(message):
	print(message, end="")
	spinner = ["|", "/", "-", "\\"]
	start_time = time.time()
	i = 0
	while True:
		if time.time() - start_time > 3:
			print("\b \b" * (len(message) + 1), end="")
			break
		print(f"\b{spinner[i%4]}", end="", flush=True)
		i += 1
		time.sleep(0.05)
while True:
	os.system("clear")
	logo = pyfiglet.figlet_format("Nanoleaf panels", font="doom", width=500)
	print(logo)
	options = '''
	Choose an option:

	[1] get scene list
	[2] get device info
	[3] change scene
	[4] change brightness
	[5] send custom JSON payload

	'''
	type_text(options)
	choice = input("")
	if choice == "3":
		def set_scene(ip_address, auth_token, scene_name):
			url = f"http://{ip_address}:16021/api/v1/{auth_token}/effects"
			payload = {"select": scene_name}
			response = requests.put(url, json=payload)
			if response.status_code == 204:
				print(Fore.GREEN + f"Nanoleaf scene set to '{scene_name}' successfully!" + Fore.RESET)
			else:
				print(Fore.RED + "Failed to set Nanoleaf scene." + Fore.RESET)
		nanoleaf_ip = f"{nanoip}"
		nanoleaf_token = f"{authtoken}"
		scene = input("Scene name? ")
		set_scene(nanoleaf_ip, nanoleaf_token, scene)
		time.sleep(3)
	elif choice == "2":
		print("")
		def get_nanoleaf_device_info(ip_address, auth_token):
			url = "http://{0}:16021/api/v1/{1}/".format(ip_address, auth_token)
			response = requests.get(url)
			if response.status_code == 200:
				device_info = response.json()
				print("Nanoleaf Device Information:")
				print("")
				print("Name: {}".format(device_info['name']))
				print("Manufacturer: {}".format(device_info['manufacturer']))
				print("Firmware Version: {}".format(device_info['firmwareVersion']))
				print("Model: {}".format(device_info['model']))
				print("Serial Number: {}".format(device_info['serialNo']))
				print("Current Brightness: {}%".format(device_info['state']['brightness']['value']))
			else:
				print("Failed to retrieve device information.")
		nanoleaf_ip = f"{nanoip}"
		nanoleaf_token = f"{authtoken}"
		get_nanoleaf_device_info(nanoleaf_ip, nanoleaf_token)
		time.sleep(3)
	elif choice == "1":
		response = requests.get(f"http://{nanoip}:16021/api/v1/{authtoken}/effects/effectsList")
		if response.status_code == 200:
			scenes = response.json()
			print("Available scenes:")
			print("")
			for scene in scenes:
				print(scene)
		else:
			print(Fore.RED + "Failed to retrive scene JSON list." + Fore.RESET)
		time.sleep(3)
	elif choice == "5":
		def custom(ip_address, auth_token):
			try:
				endpoint = input("API endpoint? ")
				payload = json.loads(input("Payload? "))
				url = f"http://{ip_address}:16021/api/v1/{auth_token}/{endpoint}"
				response = requests.put(url, json=payload)
				if response.status_code == 204:
					print(Fore.GREEN + "Payload sent successfully!" + Fore.RESET)
				else:
					print(Fore.RED + "Payload not sent." + Fore.RESET)
			except json.JSONDecodeError:
				print(Fore.RED + "Invalid payload. Must be in JSON." + Fore.RESET)
		nanoleaf_ip = f"{nanoip}"
		nanoleaf_token = f"{authtoken}"
		custom(nanoleaf_ip, nanoleaf_token)
		time.sleep(3)
	elif choice == "4":
		def changebright():
			url = f"http://{nanoip}:16021/api/v1/{authtoken}/state"
			brightnessstr = input("New brightness? (in %): ")
			brightness = int(brightnessstr)
			payload = {"brightness": {"value": brightness}}
			response = requests.put(url, json=payload)
			errcode = response.status_code
			if errcode == 204:
				print(Fore.GREEN + "Brightness changed successfully!" + Fore.RESET)
			else:
				print(Fore.RED + f"Failed to change Brightness. Error code {errcode}" + Fore.RESET)
		changebright()
		time.sleep(3)
if user_interrupt_occured:
	sys.exit(0)