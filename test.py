import requests

url = "https://www.amazon.com.be/gp/bestsellers/"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

response = requests.get(url, headers=headers)
if response.status_code == 200:
    print(response.text[:1000])  # Print first 1000 characters to check if Amazon is blocking the request
else:
    print("Failed to fetch page, Status Code:", response.status_code)
