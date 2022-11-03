import logging

import requests
from bs4 import BeautifulSoup as BS

from apps.parsing.utils import cfDecodeEmail
from logger_config import get_logger


logger = get_logger(__name__)

class ParsingSite:

    _unique_email = set()
    _all_companys = list()

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        instance.request = requests.Session()
        instance.request.headers = cls.Meta.headers
    
        return instance

    def __init__(self, url: str):
        self.url = url

    def _get_html(self, url: str):
        """
        return response object 
        """
        return self.request.get(url).text

    def _get_soup(self, html):
        """
        response BS object for scraiping
        """
        return BS(html, 'lxml')

    def _get_all_company(self, soup: BS):
        blocks = soup.find("ul", class_="l-items")
        all_company: list[BS] = blocks.find_all("div", class_="company") 
        return all_company

    @staticmethod
    def _update_dict_to_emails(company_data: dict, unique_email: tuple[str]):
        """
        it's function for update company_info more emails
        """
        emails = dict()
        for index, val in enumerate(tuple(unique_email)):
            emails[f"email{index+1}"] = val

        company_data.update(emails)

        return company_data

    def build(self):
        """
        build and parsing all project
        """
        html = self._get_html(self.url)
        soup = self._get_soup(html)
        all_company = self._get_all_company(soup)

        for company in all_company:
            link_on_dou = company.find("div", class_="h2").find("a").get("href")
            title = company.find("div", class_="h2").find("a").get_text()
            desc = company.find("div", class_ = "descr").get_text().strip()

            deep_site = self._get_html(link_on_dou)
            soup = self._get_soup(deep_site)

            try:
                link_on_website = soup.find("div", class_="site").find("a").get("href")
            except AttributeError as e:
                logger.error(e)
                link_on_website = None

            offices_link = link_on_dou + "offices/"
            column_contacts = self._get_html(offices_link)
            soup = self._get_soup(column_contacts)
            citys: list[BS] = soup.find_all("div", class_="city")

            for city in citys:
                try:
                    cf_email = city.find("div", class_="mail").find("span").get("data-cfemail")
                except AttributeError as e:
                    logging.error(e)
                else:
                    self._unique_email.add(cfDecodeEmail(cf_email))

            company_data = {
                "title": title,
                "desc": desc,
                "url_on_dou": link_on_dou,
                "link_on_website": link_on_website,
            } 
            
            update_emails_company = self._update_dict_to_emails(company_data, self._unique_email)

            self._all_companys.append(update_emails_company)
            
    

    class Meta:
        HEADERS = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0'
        }

        headers = HEADERS
