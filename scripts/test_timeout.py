import requests
import time

url = "http://localhost:8000/chat"
payload = {"message": "hola"}

print(f"Sending request to {url}...")
start = time.time()
try:
    response = requests.post(url, json=payload, timeout=60)
    print(f"Response status: {response.status_code}")
    print(f"Response body: {response.text}")
except Exception as e:
    print(f"Request failed: {e}")
end = time.time()
print(f"Duration: {end - start:.2f} seconds")
