import requests
from bs4 import BeautifulSoup

def get_search_results(api_key, cx, query, num_results=3):
    url = f'https://www.googleapis.com/customsearch/v1?key={api_key}&cx={cx}&q={query}'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        results = []

        for item in data.get('items', [])[:num_results]:
            title = item.get('title')
            link = item.get('link')
            results.append({'title': title, 'link': link})

        return results
    else:
        print("Failed to retrieve search results.")
        return None

def scrape_website(url):
    try:
        # Send an HTTP GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses

        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Example: Extracting specific information (modify as needed)
        relevant_info_element = soup.find('div', class_='relevant-class')

        if relevant_info_element:
            relevant_info = relevant_info_element.text.strip()
            return relevant_info
        else:
            print("No relevant information found on the webpage.")
            return None
    
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Error: {err}")
    
    return None
