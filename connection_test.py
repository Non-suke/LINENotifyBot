import requests
res = requests.get('https://tokyo-mc.hosp.go.jp/profession/tour_for_students.html')
print(res.status_code)