#Python2.7
import requests, re, json
from bs4 import BeautifulSoup

TUsername = raw_input('Enter User To Resolve: ')

r = requests.get('https://www.instagram.com/'+TUsername+'/')
soup = BeautifulSoup(r.content, "lxml")
scripts = soup.find_all('script', type="text/javascript", text=re.compile('window._sharedData'))
stringified_json = scripts[0].get_text().replace('window._sharedData = ', '')[:-1]
z = json.loads(stringified_json)['entry_data']['ProfilePage'][0]
y = z["logging_page_id"].replace("profilePage_", "")
print('Resolved User ID: '+y)
