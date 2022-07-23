from bs4 import BeautifulSoup
import requests
import pandas as pd

# If code doesn't work, try to change useragent
HEADERS = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36','Accept-Language': 'en-US, en;q=0.5'})

base_url = "https://www.amazon.in/s?k=bags"

items = []

for i in range (1, 21):
    print('Processing {0}...'.format(base_url + '&page={0}'.format(i)))
    url = requests.get(base_url + '&page={0}'.format(i), headers=HEADERS).text
    soup = BeautifulSoup(url,'lxml')

    bags = soup.find_all('div',class_='s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col s-widget-spacing-small sg-col-12-of-16')

    for bag in bags:

        try:
            product_url = bag.h2.a['href']
            product_name = bag.find('span',class_='a-size-medium a-color-base a-text-normal').text 
            product_price = bag.find('span',class_='a-price-whole').text
        
            product_rating = bag.find('span',class_='a-icon-alt').text
            product_numberofreviews = bag.find('span',class_='a-size-base s-underline-text').text


            # To get data of each product
            product_link = requests.get('https://www.amazon.in' + product_url, headers=HEADERS).text
            soup_link = BeautifulSoup(product_link, 'lxml')

            raw_desc = soup_link.find_all('div',class_='a-section a-spacing-medium a-spacing-top-small')
            for whole_desc in raw_desc:
                desc = whole_desc.find('ul', class_='a-unordered-list a-vertical a-spacing-mini').text[2:100] + '.....'
            

            product_details = soup_link.find('div',id='detailBullets_feature_div').find_all('span',class_='a-list-item')


            for product_asin in product_details:
                if "ASIN" in product_asin.text:
                    asin = product_asin.find('span',class_='').text
                    break


            product_desc = soup_link.find('div',id='productDescription').text


            for product_manufacturer in product_details:
                if " Manufacturer" in product_manufacturer.text:
                    if "No" in product_manufacturer.find('span',class_='').text:
                        continue
                    else :
                        manufacturer = product_manufacturer.find('span',class_='').text
                        break
            items.append([f'https://www.amazon.in{product_url}', product_name, product_price, product_rating, product_numberofreviews, desc, asin, product_desc[:150], manufacturer])
        except AttributeError:
            continue

df = pd.DataFrame(items, columns=['URL', 'Name', 'Price', 'Ratings', 'Number of Reviews', 'Description', 'ASIN', 'Product Description', 'Manufacturer'])
df.to_csv('output.csv', index=False)