import logging

import requests
from bs4 import BeautifulSoup

from apps.parsing.utils import cfDecodeEmail
from logger_config import get_logger


logger = get_logger(__name__)


HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0'
}


all_companys = list()
unique_email = set()

request = requests.Session()
request.headers = HEADERS
data = request.get("https://jobs.dou.ua/companies/").text

soup = BeautifulSoup(data, "lxml")

blocks = soup.find("ul", class_="l-items")
all_company: list[BeautifulSoup] = blocks.find_all("div", class_="company")

for company in all_company:
    link_on_dou = company.find("div", class_="h2").find("a").get("href")
    title = company.find("div", class_="h2").find("a").get_text()
    desc = company.find("div", class_ = "descr").get_text()

    deep_site = request.get(link_on_dou).text
    soup = BeautifulSoup(deep_site, "lxml")

    try:
        link_on_website = soup.find("div", class_="site").find("a").get("href")
    except AttributeError as e:
        logger.error(e)
        link_on_website = None

    offices_link = link_on_dou + "offices/"
    column_contacts = request.get(offices_link).text
    soup = BeautifulSoup(column_contacts, "lxml")
    citys: list[BeautifulSoup] = soup.find_all("div", class_="city")

    for city in citys:
        try:
            cf_email = city.find("div", class_="mail").find("span").get("data-cfemail")
        except AttributeError as e:
            logging.error(e)
        else:
            unique_email.add(cfDecodeEmail(cf_email))

    company_data = {
        "title": title,
        "desc": desc,
        "url_on_dou": link_on_dou,
        "link_on_website": link_on_website,
        "emails": tuple(unique_email)
    } 

    all_companys.append(company_data)

print(all_companys)
print(len(all_companys))

"""
In the repo https://github.com/Sergii-7/scrap_sites you may show some code.
Please fork it and transform Parser_jobs_dou.py for new things:
1. Parse all companies profiles from dou
2. Each profile must have URL, Name, Size, Description, Website, Phones and Email
3. If a company have more than one Phone or Email - add new field called Phone1 or Email1 for each (and more)
4. Output should be in a CSV, UTF-8
5. Don't shady ask additional information
"""