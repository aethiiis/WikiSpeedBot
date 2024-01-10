import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def get_wikipedia_links(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Trouver tous les liens dans le corps de l'article
        links = soup.find_all('a', href=True)

        # Filtrer les liens qui pointent vers des pages Wikipédia
        wikipedia_links = [link['href'] for link in links if is_wikipedia_link(link['href'])]

        # Construire les URL absolues en utilisant urljoin
        wikipedia_links = [urljoin(url, link) for link in wikipedia_links]

        return wikipedia_links
    else:
        print(f"Erreur {response.status_code} lors de la requête.")
        return None

def is_wikipedia_link(href):
    # Vérifier si le lien pointe vers une page Wikipédia
    return href and href.startswith('/wiki/') and 'Special' not in href and 'Portal' not in href and 'Wikipedia' not in href and 'Special' not in href and 'Help' not in href and 'Talk' not in href and 'File' not in href and 'Category' not in href and '_(identifier)' not in href and 'Main_Page' not in href
