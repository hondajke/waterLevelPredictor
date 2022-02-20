import sys
import requests
import json

client = requests.session()

r = client.get('http://allrivers.info/gauge/lena-yakutsk')
#r = client.get('http://allrivers.info/comments/gauge/929')
#print(r.headers['Set-Cookie'])

headers = {
    'x-csrf-token': 'op6AIY2AGRnCDik1KFzXsGUBnMBMjA4GeZMSlJMf',
    'x-requested-with': 'XMLHttpRequest',
    'x-xsrf-token': 'eyJpdiI6IitWNFZTV1N2NzlzS3RqWm54QUlwb3c9PSIsInZhbHVlIjoiVkc5ZXFLWHQxYXF0cXJnZGYwL3RtMG0wVVovVUVwQkJEVFU5ZjN0VjlJNTZSdnBKTHhScWVSRDRwMVZObkFpVTdPZVhaMUNNR3kwN2M2WjR3RTFIMnVGTFZ1Um1zcEp3QjJCbWZ2RjlnTnUwK3c1UFFEbEZTa3VGV3QzNmhQcFAiLCJtYWMiOiJmMDJmNjY1ZWM3MmFiZDQwMmZhYTRlZTc0NzRjZTIwMWE4MDQzMTY3OTUyNDA3YmJkNzhmZTVlODUxYmE0NGJhIiwidGFnIjoiIn0%3D'
}
r = client.post('http://allrivers.info/graph', json={"item": 929}, headers=headers)
print(r.status_code)
if r.status_code == 200:
    print(r.json()())
