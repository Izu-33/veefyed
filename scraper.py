import requests
import json

url = "https://snapklik.com/a/g/?id=11060451&i=24&bi=8"

payload = {}
headers = {
  'accept': 'application/json, text/plain, */*',
  'accept-language': 'en-GB,en;q=0.9,en-US;q=0.8',
  'authorization': 'eyJhbGciOiJSUzI1NiIsImtpZCI6Ijk1MWRkZTkzMmViYWNkODhhZmIwMDM3YmZlZDhmNjJiMDdmMDg2NmIiLCJ0eXAiOiJKV1QifQ.eyJwcm92aWRlcl9pZCI6ImFub255bW91cyIsImlzcyI6Imh0dHBzOi8vc2VjdXJldG9rZW4uZ29vZ2xlLmNvbS9zbmFwa2xpa3N0b3JlIiwiYXVkIjoic25hcGtsaWtzdG9yZSIsImF1dGhfdGltZSI6MTc1MzkwNzE4MSwidXNlcl9pZCI6ImhKNmhOWm1oNldPRExTR3d1RTRFWWU1eTFuZTIiLCJzdWIiOiJoSjZoTlptaDZXT0RMU0d3dUU0RVllNXkxbmUyIiwiaWF0IjoxNzUzOTEzMTQ5LCJleHAiOjE3NTM5MTY3NDksImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnt9LCJzaWduX2luX3Byb3ZpZGVyIjoiYW5vbnltb3VzIn19.imRwS5IXPIVYkj2JDsgn7z59BNcXYAgItyt-Py7u1Ywng-O5LkGTi6eS2B9R4LHMcOGmUnBbhCapHt6WtnLBsuHlE4KHpSvTiD0HdbA6o094rudwsg8i15reUxTCW-_m0nCNUGRmi3X2SM7Eeq0VITcwt4VK-PTHruz1OmApt5M6vAjpxY1A3_dFKMvvWjpvhX1ZDaaNnZsIStbvuR3dL6WpcPMtFa1n4j0bYvH2ld_vZ8mdxb6yLLfKG7lRd2GsGp1IYoprIck8z398OqoMQpROOkq5citN6lhjBuI6YbWX6216fMCP5FABPhlP0gTaiQNZIZ5qqVKcCkSNJZ3tHg',
  'cache-control': 'no-cache',
  'content-type': 'application/json',
  'ct': 'default',
  'ip': '',
  'lc': 'en-gb',
  'pragma': 'no-cache',
  'priority': 'u=1, i',
  'referer': 'https://snapklik.com/en-gb/g/c?id=11060451&i=8',
  'sc': '',
  'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Microsoft Edge";v="138"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-origin',
  'ua': '',
  'url': 'https://snapklik.com/en-gb/g/c?id=11060451&i=8',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0',
  'v': '2',
  'xcc': '',
  'Cookie': '_ga=GA1.1.2460731.1753908252; _gcl_au=1.1.1140001857.1753908252; _ga_KCY0CEWFX2=GS2.1.s1753913100^$o2^$g1^$t1753914036^$j50^$l0^$h0'
}

response = requests.request("GET", url, headers=headers, data=payload)

# print(response.text)
with open('response_data.json', 'w', encoding='utf-8') as f:
    json.dump(response.json(), f, indent=2, ensure_ascii=False)

# Extract the products list
response_data = response.json()
# print(response_data)
products = response_data['data']['hits']

# List to store extracted product information
extracted_products = []

for product in products:
    # Extract each field
    product_info = {
        'Product ID': product.get('skid', ''),
        'Product Line Name': product.get('rankName', ''),
        'Brand Name': product.get('brand', ''),
        'Product Name': product.get('text', ''),
        'Product Description': product.get('text', ''),
        'Product Images': [product.get('image', '')],
        'Price': product.get('price', 0) / 100,
        'Size/Volume': product.get('OptionMap', {}).get('Style', '')
    }

    extracted_products.append(product_info)

for product in extracted_products:
    print(json.dumps(product, indent=2))
    print("\n---\n")