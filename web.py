from bs4 import BeautifulSoup
import requests

# Fetch the webpage
url = 'https://www.house.kg/snyat-kvartiru?rental_term=3&region=all&sort_by=price%20asc&page=2&timestamp=1724447600'
response = requests.get(url)

# Parse the content
soup = BeautifulSoup(response.content, 'lxml')

# Extract the body tag content
body_content = soup.prettify()

# Save the body content to a text file
with open('body_content.txt', 'w', encoding='utf-8') as file:
    file.write(body_content)

print("Body content saved to body_content.txt")
