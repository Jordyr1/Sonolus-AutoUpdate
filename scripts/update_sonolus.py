# dw about my horrible code lol
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json

def get_sonolus_info():
    url = "https://sonolus.com"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    description = soup.find('p', class_='text-center').text.strip()

    version = soup.find('p', class_='font-bold').text.strip()
  
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
        "apps": [
            {
                "appPermissions": {
                    "entitlements": [
                        "com.apple.security.network.client",
                        "com.apple.developer.networking.wifi-info"
                    ],
                    "privacy": {
                        "NSLocalNetworkUsageDescription": "This app scans the local network for nearby devices."
                    }
                },
                "bundleIdentifier": "com.FosFenes.Sonolus",
                "developerName": "Sonolus Team", 
                "downloadURL": download_link,
                "iconURL": "https://sonolus.com/icon.png",
                "localizedDescription": f" {version} \n \n {changelog} \n \n Credit: \n Jordyr1 (Modified repository)\n\n",
                "name": "Sonolus",
                "versions": [
                    {
                        "date": current_date,
                        "downloadURL": download_link,
                        "localizedDescription": description,
                        "size": file_size, 
                        "version": version
                    }
                ]
            }
        ],
        "author": "Sonolus Team", 
        "name": "Sonolus"
    }
    with open("sonolus_data.json", "w") as json_file:
        json.dump(sonolus_data, json_file, indent=4)


# profit
get_sonolus_info()

