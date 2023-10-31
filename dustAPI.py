from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus, unquote
import requests
import serial
import time

url = 'http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty'
#params = '?serviceKey=MA7tdZEbIwDeDNa%2FWKs6d0jRU6Jlk50aGLnFxwNPFGEZbsJFIcSFfOXh9iBk8Czri6eGKgyU5ErHpKRszyAmOw%3D%3D&returnType=xml&numOfRows=100&pageNo=1&stationName=주안&dataTerm=DAILY&ver=1.0'
queryParams='?' + urlencode({quote_plus('serviceKey'):'MA7tdZEbIwDeDNa/WKs6d0jRU6Jlk50aGLnFxwNPFGEZbsJFIcSFfOXh9iBk8Czri6eGKgyU5ErHpKRszyAmOw==',
							quote_plus('returnType'):'xml',
							quote_plus('numOfRows'):'100',
							quote_plus('pageNo'):'1',
							quote_plus('stationName'):'주안',
							quote_plus('dataTerm'):'DAILY',
							quote_plus('ver'):'1.0'})

#res = requests.get(url+params)
res = requests.get(url+queryParams)
soup = BeautifulSoup(res.content, 'html.parser')
data = soup.find_all('item')

port='/dev/ttyACM0'
brate=9600

seri=serial.Serial(port, baudrate=brate, timeout=None)
#rint(seri.name)

#seri.write('b\x0101')

a=1
while a:
	if seri.in_waiting != 0:
		content=seri.readline()
		innerDensity = content.decode()
		a=0


#print(data)
d_toggle=1
for item in data:
	if d_toggle==1:
		datatime=item.find('datatime')
		pm25value=item.find('pm25value')
		#print(datatime.get_text())
		#print(pm25value.get_text())
		d_toggle=0

datetime=datatime.get_text()
outerDensity=pm25value.get_text()

while 1:
	print(f'가장 최근 갱신 시각 : {datetime}')
	print(f'최신 미세먼지 밀도 : {outerDensity}')
	print(f'실내 미세먼지 밀도 : {innerDensity}\n')

	if outerDensity>innerDensity:
		print('밖의 미세먼지 농도가 더 높습니다. 외출을 자제하십시오\n')
	elif outerDensity<innerDensity:
		print('실내의 미세먼지 농도가 더 높습니다. 환기를 권장드립니다\n')
	else:
		print('값 오류\n')
	
	if seri.in_waiting != 0:
		content=seri.readline()
		innerDensity = content.decode()
	
	time.sleep(5)
	
