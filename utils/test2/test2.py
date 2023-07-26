# Importing necessary libraries
import requests
from bs4 import BeautifulSoup
import os

# Defining the URL to scrape
url = 'https://s.taobao.com/search?q=basketball&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20220106&ie=utf8'

# Sending a GET request to the URL
response = requests.get(url)

# Parsing the HTML content of the page
soup = BeautifulSoup(response.content, 'html.parser')

# Finding all the image tags on the page
images = soup.find_all('img')

# Creating a directory to store the images
if not os.path.exists('basketball_images'):
    os.makedirs('basketball_images')

# Downloading and saving the images
for i, image in enumerate(images):
    image_url = image['src']
    response = requests.get(image_url)
    with open(f'basketball_images/image_{i}.jpg', 'wb') as f:
        f.write(response.content)