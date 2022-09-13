import requests
r = requests.get("https://raw.githubusercontent.com/Anthony-Nguyen3/CMPUT-404-Labs/main/Lab_1/lab1.py")
print(r.text)