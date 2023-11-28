import requests
from bs4 import BeautifulSoup

url = 'https://www.example.com'  # Replace with your URL
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    paragraphs = soup.find_all('p')
    for paragraph in paragraphs:
        print(paragraph.text)
else:
    print('Error loading page:', response.status_code)
