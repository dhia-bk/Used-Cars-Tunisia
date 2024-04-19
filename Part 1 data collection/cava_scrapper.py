from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import pandas as pd


# List to store the scraped data
cava_data_list =  [ ['titre' , 'prix' , 'date de publication' , 'localisation' , 
                    'numéro telephone' , 'couleur', 'Puissance fiscale',
                    'Cylindrée', 'Carburant', 'Marque de voiture',
                    'Kilométrage', 'Model', 'Boîte de vitesse' , 'Année', 'Number of Pictures', 'Description'] ]


async def scrape_data_cava(url, session, max_retries = 20):
        
        """
            Asynchronous function to scrape detailed information about each car from www.cava.tn.

            Parameters:
            
            - url (str): The URL of the car listing to scrape.
            - session (aiohttp.ClientSession): Asynchronous session for making HTTP requests.
            - max_retries (int): Maximum number of retries in case of an error.
            
        """
        
        for attempt in range(max_retries):
          try:
                    async with session.get(url) as response:
                
                      response.raise_for_status()
                      html_content = await response.text()
                      sett = []

                      soup1 = BeautifulSoup(html_content, "html.parser")
                      soup2 = BeautifulSoup(soup1.prettify(), 'html.parser')
                      
                      details_1 = soup2.find('div',{'class':'col-lg-4 col-md-4 col-sm-12 col-12 mt-2'})

                      title = details_1.find('h1',{'class':'p-title px-3 font-p-r pt-1'}).text.strip()
                      sett.append(title)
                    
                      price = details_1.find('div' , {'class' : 'price font-p-s-b'}).find('label').text
                      sett.append(price)

                      posting_date = details_1.find('div',{'class':'d-flex justify-content-between cv-publish-date-delivery'}).find('label', {'class': 'font-p-e-l cv-text-start'}).text.strip()
                      sett.append(posting_date)
                      
                      place_tag = details_1.find('div',{'class':'cv-product-location mt-2 cv-info-icons cv-text-start ng-star-inserted'})
                      place=''
                      for a in place_tag.find_all('a') :
                        place += ',' + a.text.strip()
                      place = place[1:]
                      sett.append(place)
                      

                      #locating and appending the phone number  
                      phone_number = details_1.find('div',{'class':'contact-phone cv-details-buttons mt-3 text-center pointer ng-star-inserted'}).find('span').text.strip()
                      sett.append(phone_number)
                    

                      """
                          
                      In the next section, I encountered a challenge where the order of values was inconsistent across different webpages.
                      To address this, I implemented the following approach:
                      1. Created an empty list, 'car_1', to store characteristics and their corresponding values.
                      2. Appended each characteristic and its value to 'car_1'.
                      3. Created an 'index_mapping' dictionary to match the indexes with the desired order in the final list containing the data.
                      This method ensures that the values are correctly aligned with their corresponding characteristics, regardless of variations in webpage structures.

                      """

                      details_3 = soup2.find('div',{'class':'mb-3 ng-star-inserted'}).find_all('div',{'class':'product-specify mr-3 mt-2 pr-5 ng-star-inserted'})

                      car_1 = []

                      for div in details_3 :

                        span = div.find('span').text.strip()
                        car_1.append(span)
                        
                  
                        value = div.find('a',{'class':'font-p-m'}).text.strip()
                        car_1.append(value)
                        
                      if (len(car_1)) == 18:
                          dict_1 = {car_1[i]: car_1[i + 1] for i in range(0, len(car_1), 2)}
                          index_mapping = {
                          'Couleur': 5,
                          'Puissance fiscale': 6,
                          'Cylindrée': 7,
                          'Carburant': 8,
                          'Marque de voiture': 9,
                          'Kilométrage': 10,
                          'Model': 11,
                          'Boîte de vitesse': 12,
                          'Année' : 13
                          }
                      else:
                          while len(car_1) < 18:
                              car_1.append('')  
                      for i in range (9):
                            sett.append('')
                      for i , j in dict_1.items():
                            index = index_mapping.get(i)
                            if index is not None:
                              sett[index] = j
                              car_1.append(sett)

                      

                      try:
                        nbr_pictures = soup2.select_one('body > app > div > div:nth-child(1) > div > app-product-details > div.container-full.bg-grey.mt-5 > div > div:nth-child(1) > div.col-lg-8.col-md-8.col-sm-12.col-12.mt-2 > div.p-1.bg-white.rounded.position-relative.cv-product-images.ng-star-inserted > div.menu-slider-container.d-flex.justify-content-center.align-items-center.py-2.ng-star-inserted')
                        nbr_pictures = len(nbr_pictures.find_all('img'))
                        sett.append(nbr_pictures)

                      except Exception as e:
                           
                           sett.append(0) 

                      try:

                        description =  soup2.select_one('body > app > div > div:nth-child(1) > div > app-product-details > div.container-full.bg-grey.mt-5 > div > div:nth-child(2) > div.col-lg-8.col-md-8.col-sm-12.col-12.mt-2 > div.product-specify.product-description.p-3.col-12.col-md-12.cv-text-start.mt-1 > p').text
                        sett.append(description)

                      except Exception as e:
                           
                           sett.append('')

                      cava_data_list.append(sett)

                      break 
                    

          except Exception as e:
              await asyncio.sleep(1)   # a 1-second delay before retrying
              pass
        else:
              pass

async def main(): 

    url = 'https://www.cava.tn/category/voitures'  

    options = webdriver.ChromeOptions()
    options.add_argument('--headless') 
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-extensions')

    # Creating a Chrome WebDriver
    driver = webdriver.Chrome(options=options)

    driver.get(url)

    wait = WebDriverWait(driver, 10) 




    for i in range(550):
        try:
            css_selector = "body > app > div > div:nth-child(1) > div > app-category-product > div > div > app-product-list > div.d-flex.justify-content-center.align-items-center.py-4.ng-star-inserted > button"
            button = driver.find_element(By.CSS_SELECTOR, css_selector)

            driver.execute_script("window.scrollTo(0, 0);")
            driver.execute_script("arguments[0].scrollIntoView(true);", button)
            button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector)))
            button.click()
            time.sleep(2)
        except Exception as e:
                continue
        
    element_1 = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'body > app > div > div:nth-child(1) > div > app-category-product > div > div > app-product-list > div.cv-items-grid.py-4.ng-star-inserted')))
        
    final_page_source = driver.page_source
    hrefs_cava = []

    soup = BeautifulSoup(final_page_source, "html.parser")

    driver.quit()

    element = soup.find('div', {'class': 'cv-items-grid py-4 ng-star-inserted'})
    elements = element.find_all(class_="ng-star-inserted")


    for listing in elements:
        try:
            div = listing.find('div', class_='cv-product').find('a')
            href = div['href']
            hrefs_cava.append(href)
        except Exception as e:
            continue
    hrefs_cava = [f'https://www.cava.tn{car}'for car in hrefs_cava]

    async with aiohttp.ClientSession() as session:
        tasks = [scrape_data_cava(url, session) for url in hrefs_cava]
        await asyncio.gather(*tasks)


    cava_df = pd.DataFrame(cava_data_list[1:], columns=cava_data_list[0])
    file_path = "##########"
    cava_df.to_csv(file_path, index=False)


if __name__ == '__main__' :
    main()


