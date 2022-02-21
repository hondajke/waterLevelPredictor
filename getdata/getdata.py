import sys
import requests
import json
import csv
from datetime import datetime

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'content-length': '13',
    'content-type': 'application/json',
    'cookie': '_ym_d=1644129280; _ym_uid=1644129280136311546; _ym_isad=2; XSRF-TOKEN=eyJpdiI6IjRIVzBJYlR6MVBTTXFLODdGZUt0U3c9PSIsInZhbHVlIjoiS3BzWDdYbWwzRURyc0RRYlpFQksrYVMzZHY3T1lZcXI0VDNsVXloNGVJbjZjZWZJQ2FNZkNTYjQxRE5LZFZzWkFSbXN1SFhvOGZCd0RISzNibENlMXQxWXRXWFBDUWkzRUJ6YkNXOU9lNWUrREJaWlRpL1VUVDd6V0RRSzZ0aCsiLCJtYWMiOiI3Y2M4Mjg4ZDY1MzQ1MDJkMjM4YTAyYzBmM2JkNDA4NGMwNmFjZDc2NDBmZGQ5NmU0Y2Q0ZTgzNmIxZmIxMTQ5IiwidGFnIjoiIn0%3D; allriversinfo_session=eyJpdiI6IjFBYXI3Q1NaeXVCaU5MT2pKVDdxcEE9PSIsInZhbHVlIjoiRGNmUG56VDdDTElTUTI1S2hqTWx4c3grMkJlWjdNcGpacnBQdC85ZUZlOG9jYlFLYmZ4U3NtMG1EUml1UHVwQ0tDYjdIUmhrNXc5WkxIQ0lManlEUXd1Tk1hejBZVnZOeS8rbTZMY2FHUkM1cUQ0K2ZXTUVIUGZyV3AwSXZIV0UiLCJtYWMiOiJmYjA3NGQ1ZGI3ZTMzNWI5OWVhZTU5ZTY1MjYxNThhN2FhMTY1MTkyZjc1YWViNGM4OTJmNGNiNDM0Y2Q5NTEyIiwidGFnIjoiIn0%3D',
    'origin': 'https://allrivers.info',
    'referer': 'https://allrivers.info/gauge/lena-habarova',
    'sec-ch-ua': '"Opera GX";v="83", "Chromium";v="97", ";Not A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 OPR/83.0.4254.46',
    'x-csrf-token': 'op6AIY2AGRnCDik1KFzXsGUBnMBMjA4GeZMSlJMf',
    'x-requested-with': 'XMLHttpRequest',
    'x-xsrf-token': 'eyJpdiI6IitWNFZTV1N2NzlzS3RqWm54QUlwb3c9PSIsInZhbHVlIjoiVkc5ZXFLWHQxYXF0cXJnZGYwL3RtMG0wVVovVUVwQkJEVFU5ZjN0VjlJNTZSdnBKTHhScWVSRDRwMVZObkFpVTdPZVhaMUNNR3kwN2M2WjR3RTFIMnVGTFZ1Um1zcEp3QjJCbWZ2RjlnTnUwK3c1UFFEbEZTa3VGV3QzNmhQcFAiLCJtYWMiOiJmMDJmNjY1ZWM3MmFiZDQwMmZhYTRlZTc0NzRjZTIwMWE4MDQzMTY3OTUyNDA3YmJkNzhmZTVlODUxYmE0NGJhIiwidGFnIjoiIn0%3D'
}

r = requests.post('https://allrivers.info/graph', json={"item": 929}, headers=headers)
print(r.status_code)
if r.status_code == 200:
    json_data = json.loads(r.content)
    with open('data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['data', 'water_level'])
        for i in range(18, 22):
            year_str = '20' + str(i)
            print(year_str)
            print(len(json_data['graphdata'][year_str]))
            for j in range(len(json_data['graphdata'][year_str])):
                #print(json_data['graphdata'][year_str][j][0])
                date = str(json_data['graphdata'][year_str][j][0])
                #print(date[:-3])
                print(datetime.utcfromtimestamp(int(date[:-3])).strftime(f'%d-%m-{year_str}'))
                writer.writerow([datetime.utcfromtimestamp(int(date[:-3])).strftime(f'%d-%m-{year_str}'), json_data['graphdata'][year_str][j][1]])
            #writer.writerow([json_data[]])