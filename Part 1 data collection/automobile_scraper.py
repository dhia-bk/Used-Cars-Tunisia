# Importing necessary libraries for automobile.tn
import aiohttp
import asyncio
from bs4 import BeautifulSoup
import pandas as pd


# List to store the scraped data
automobile_data_list = [['Titre', 'Prix', 'Fabricant', 'Carrosserie', 'Energie',
                         'Puissance fiscale', 'Boite', 'Transmission',  
                         'Kilometrage', 'Annee', 'Inserée le'
                           ]]

# List of car manufacturers for identification
manufacturers_list = ['Alfa Romeo', 'Audi', 'BAIC', 'YX', 'BMW', 'BYD', 'Chery', 'Chevrolet', 'Citroën', 'Cupra',
                      'Dacia', 'DFSK', 'Dodge', 'Dongfeng', 'DS', 'Faw', 'Fiat', 'Ford', 'Foton', 'GAC', 'Geely',
                      'Great Wall', 'Haval', 'Honda', 'Hummer', 'Hyundai', 'Infiniti', 'Isuzu', 'Iveco', 'Jaguar',
                      'Jeep', 'KIA', 'Lada', 'Lancia', 'Land Rover', 'Mahindra', 'Maserati', 'Mazda', 'Mercedes',
                      'MG', 'Mini', 'Mitsubishi', 'Nissan', 'Opel', 'Peugeot', 'Piaggio', 'Porsche', 'Renault', 'Seat',
                      'Skoda', 'Smart', 'Ssangyong', 'Suzuki', 'TATA', 'Toyota', 'Volkswagen', 'Volvo', 'Wallyscar']

# Base URL for automobile listings
base_url = 'https://www.automobile.tn/fr/occasion/'

automobile_urls = [f"{base_url}{i}" for i in range(1, 135)]

# List to store individual car listing URLs
automobile_cars_urls = []


async def get_automobile_urls(url, session, max_retries=3):
    """
    Asynchronous function to fetch and parse individual car listing URLs with retry mechanism.

    Parameters:
    - url (str): The URL to fetch and parse.
    - session (aiohttp.ClientSession): Asynchronous session for making HTTP requests.
    - max_retries (int): Maximum number of retries in case of an error.

    """
    for attempt in range(max_retries):
        try:
            # Fetching HTML content of the page
            async with session.get(url, timeout=30) as response:
                response.raise_for_status()
                html_content = await response.text()

                soup1 = BeautifulSoup(html_content, "html.parser")
                soup2 = BeautifulSoup(soup1.prettify(), 'html.parser')

                articles = soup2.find_all('div', {'data-key': True})
                data_keys = [div['data-key'] for div in articles]

                for data_key in data_keys:
                    article = soup2.find('div', {'data-key': data_key})
                    href = article.find('a', {'class': 'occasion-link-overlay'}).get('href')
                    link = f'https://www.automobile.tn{href}'
                    automobile_cars_urls.append(link)
                automobile_urls.remove(url)

        except asyncio.TimeoutError:
            await asyncio.sleep(2 ** attempt)   

        except aiohttp.ClientError as e:
            await asyncio.sleep(2 ** attempt)   # an exponential delay before retrying
            pass
           
        else :
            # Break the loop if successful
            break
    else:
        pass

async def scrape_automobile(url, session, max_retries=5):

    """
    Asynchronous function to scrape detailed information about each car from www.automobile.tn.

    Parameters:
    - url (str): The URL of the car listing to scrape.
    - session (aiohttp.ClientSession): Asynchronous session for making HTTP requests.
    - max_retries (int): Maximum number of retries in case of an error.

    """

    car = []
    for attempt in range(max_retries):
        try:
            async with session.get(url, timeout=10) as response:
                response.raise_for_status()
                html_content = await response.text()
                # Parsing HTML content
                soup1 = BeautifulSoup(html_content, "html.parser")
                soup2 = BeautifulSoup(soup1.prettify(), 'html.parser')
                

                title = soup2.select_one('#content_container > div.occasion-details-v2 > h1').text.strip()
                car.append(title)

                price = str(soup2.select_one('#content_container > div.occasion-details-v2 > div:nth-child(5) > div.col-md-4 > div > div:nth-child(1) > div.price-box > div').text[:-18].strip()).replace(' ','')
                car.append(price)
                
                manufacturer = next((manuf for manuf in manufacturers_list if manuf.lower() in title.lower()), 'Other')
                car.append(manufacturer)

                carroserie = soup2.select_one('#content_container > div.occasion-details-v2 > div:nth-child(5) > div.col-md-4 > div > div:nth-child(1) > div.main-specs > ul > li:nth-child(7) > span.spec-value').text.strip()
                car.append(carroserie)
                energie = soup2.select_one('#content_container > div.occasion-details-v2 > div:nth-child(5) > div.col-md-4 > div > div:nth-child(1) > div.main-specs > ul > li:nth-child(3) > span.spec-value').text.strip()
                car.append(energie)
                Boite = soup2.select_one('#content_container > div.occasion-details-v2 > div:nth-child(5) > div.col-md-4 > div > div:nth-child(1) > div.main-specs > ul > li:nth-child(5) > span.spec-value').text.replace('cv','').strip()
                car.append(Boite)
                transmission = soup2.select_one('#content_container > div.occasion-details-v2 > div:nth-child(5) > div.col-md-8 > div.row > div:nth-child(2) > div > div.divided-specs > ul > li:nth-child(4) > span.spec-value.text-end').text.strip()
                car.append(transmission)
         
                kilo = soup2.select_one('#content_container > div.occasion-details-v2 > div:nth-child(5) > div.col-md-4 > div > div:nth-child(1) > div.main-specs > ul > li:nth-child(1) > span.spec-value').text.replace('km','').strip().replace(' ','')
                car.append(kilo)
                annee = soup2.select_one('#content_container > div.occasion-details-v2 > div:nth-child(5) > div.col-md-4 > div > div:nth-child(1) > div.main-specs > ul > li:nth-child(2) > span.spec-value').text.strip()
                car.append(annee)

                Inserée = soup2.select_one('#content_container > div.occasion-details-v2 > div:nth-child(5) > div.col-md-4 > div > div:nth-child(1) > div.main-specs > ul > li:nth-child(8) > span.spec-value').text.strip()
                car.append(Inserée)

                automobile_data_list.append(car)


        except Exception as e:
            await asyncio.sleep(5)
            pass     
    else:
        print(f"Failed to scrape {url} after {max_retries} attempts. index {automobile_cars_urls.index(url)}")


async def main():
    """
    Asynchronous main function to orchestrate the fetching and parsing of car listing URLs.

    """
    async with aiohttp.ClientSession() as session:
        tasks = [get_automobile_urls(link, session) for link in automobile_urls]
        await asyncio.gather(*tasks)


    
    async with aiohttp.ClientSession() as session:
        tasks = [scrape_automobile(url, session) for url in automobile_cars_urls]
        await asyncio.gather(*tasks)

    automobile_df = pd.DataFrame(automobile_data_list[1:], columns=automobile_data_list[0])
    
    automobile_df['Model'] = automobile_df.apply(lambda row: row['Titre'].replace(row['Fabricant'], '').strip(), axis=1)

    file_path = "############"
    automobile_df.to_csv(file_path, index=False)

if __name__ == '__main__':
    main()
