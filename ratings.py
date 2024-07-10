import sys
import json
import requests
from bs4 import BeautifulSoup

def get_player_details(cid):
    url = f'https://chessa.co.za/ratingsdatabase/playerpage.aspx?cid={cid}'
    response = requests.get(url)
    
    if response.status_code != 200:
        return None
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract necessary details from the page
    name = soup.find('h5').text.strip()
    
    # Default ratings in case they are not found
    raw_rating = weighted_rating = weighted_performance = '0'
    
    # Find the ratings
    try:
        raw_rating = soup.find(text='Current Raw rating').findNext('td').text.strip()
    except AttributeError:
        pass
    try:
        weighted_rating = soup.find(text='Current Weighted rating').findNext('td').text.strip()
    except AttributeError:
        pass
    try:
        weighted_performance = soup.find(text='Current Weighted performance').findNext('td').text.strip()
    except AttributeError:
        pass

    official_published_rating = max(raw_rating, weighted_rating, weighted_performance, key=float)
    
    # Find gender if available, otherwise set to 'N/A'
    sex = 'N/A'
    try:
        gender_element = soup.find(text='Gender:')
        if gender_element:
            sex = sex = gender_element.next_element.strip().upper()[0]
    except AttributeError:
        pass
    
    return {
        'cid': cid,
        'name': name,
        'official_published_rating': official_published_rating,
        'sex': sex
    }

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(json.dumps({'error': 'Invalid number of arguments'}))
        sys.exit(1)
    
    cid = sys.argv[1]
    player_details = get_player_details(cid)
    
    if player_details is None:
        print(json.dumps({'error': 'Player not found'}))
    else:
        print(json.dumps(player_details))
