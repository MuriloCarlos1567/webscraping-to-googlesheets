import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
import requests
from bs4 import BeautifulSoup

page = requests.get('https://web.archive.org/web/20121007172955/http://www.nga.gov/collection/anZ1.htm')

soup = BeautifulSoup(page.text, 'html.parser')

last_links = soup.find(class_='AlphaNav')
last_links.decompose()

artist_name_list = soup.find(class_='BodyText')
artist_name_list_items = artist_name_list.find_all('a')

scope = ["https://spreadsheets.google.com/feeds",
'https://www.googleapis.com/auth/spreadsheets',
"https://www.googleapis.com/auth/drive.file",
"https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)

client = gspread.authorize(creds)
sheet = client.open("github-tutorial").sheet1
data = sheet.get_all_records()

for artist_name in artist_name_list_items:
  names = artist_name.contents[0]
  links = 'https://web.archive.org' + artist_name.get('href')
  row = [names, links]
  index = 1
  sheet.insert_row(row, index)