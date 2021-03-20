import requests
import csv
from bs4 import BeautifulSoup
from collections import defaultdict

URL = 'https://thegoodregistry.com/collections/all-charities'
web = requests.get(URL)
web.encoding = 'utf-8'
content = BeautifulSoup(web.content, 'html.parser')


def main():
    title_and_description = defaultdict()
    items = content.find_all('div', class_='centered')
    for i in items:
        encoded_string = i.encode('utf-8').decode('utf-8')
        clean_string = encoded_string.replace('<div class="centered">', '')\
                              .replace('<div style="padding-top: 10px;">', '')\
                              .replace('</div>', '')\
                              .replace('Click here to find out more.', '')\
                              .replace('-', '')\
                              .strip()
        unfiltered_list = clean_string.split('\n')
        title_and_description[unfiltered_list[0]] = unfiltered_list[2].strip() if len(unfiltered_list) == 3 else ''
    write_csv(title_and_description)


def write_csv(input: dict):
    with open('result.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        for key, value in input.items():
            writer.writerow([key, value])


if __name__ == "__main__":
    main()