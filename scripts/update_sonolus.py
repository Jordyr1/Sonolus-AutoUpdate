import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import re

def get_sonolus_info():
    url = "https://sonolus.com"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    description = soup.find('p', class_='text-center').text.strip()

    version = soup.find('p', class_='font-bold').text.strip()
    fixed_version = re.search(r'\d+(\.\d+)+', version).group()
  
    release_notes_url = "https://wiki.sonolus.com/release-notes/"
    response = requests.get(release_notes_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    latest_version_tag = soup.find('a', href=lambda href: href and '/release-notes/versions/' in href)

    # check if latest ver
    if latest_version_tag:
        latest_version_link = latest_version_tag['href']
        latest_version_url = f"https://wiki.sonolus.com{latest_version_link}"  
      
        response = requests.get(latest_version_url)
        version_soup = BeautifulSoup(response.text, 'html.parser')
      
        # get changelog
        changelog_list = version_soup.find('h2', id='changelog')
        if changelog_list:
            changelog_items = changelog_list.find_next('ul') 
            changelog = "\n".join([li.text.strip() for li in changelog_items.find_all('li')])
        else:
            changelog = "Changelog not found."
    else:
        latest_version_url = None
        changelog = "No latest version found."

    # find download link
    wikiurl = "https://wiki.sonolus.com/getting-started/installing/ios.html#apple-s-testflight"
    response = requests.get(wikiurl)
    soup = BeautifulSoup(response.text, 'html.parser')

    links = soup.find_all('a', href=True)
    download_link = None 
    for link in links:
        if 'download.sonolus.com' in link['href']:
            download_link = link['href']
            break
    else:
        download_link = "No download link found."

    file_size = 0
    if download_link != "No download link found.":
        head_response = requests.head(download_link)
        file_size = int(head_response.headers.get('Content-Length', 0))

    current_date = datetime.now().strftime("%Y-%m-%d")

    sonolus_data = {
        "name": "Sonolus (Beta)",
        "identifier": "com.FosFenes.Sonolus",
        "apps": [
            {
                "name": "Sonolus",
                "bundleIdentifier": "com.FosFenes.Sonolus",
                "subtitle": f"Sonolus v{fixed_version} Beta",
                "localizedDescription": f"Sonolus v{fixed_version} Beta\n\n{changelog}\n\nCredit: Jordyr1 (Modified repository)",
                "downloadURL": download_link,
                "iconURL": "https://sonolus.com/icon.png",
                "version": fixed_version,
                "size": file_size
            }
        ]
    }
    with open("sonolus_data.json", "w") as json_file:
        json.dump(sonolus_data, json_file, indent=4)


# profit
get_sonolus_info()
