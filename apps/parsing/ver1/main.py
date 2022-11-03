from apps.parsing.ver1.classes import ParsingSite
from apps.parsing.utils import get_max_keys

from logger_config import get_logger

from database import crud


def main():
    pars = ParsingSite("https://jobs.dou.ua/companies/")
    pars.build()

    headers = get_max_keys(pars._all_companys)
    crud.write_to_headers(headers)

    logger = get_logger(__name__)

    for company in pars._all_companys:
        try:
            crud.write_to_csv(company)
        except Exception as e:
            logger.error(e)
