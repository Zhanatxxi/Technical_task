import os
import csv

from global_settings import settings
from logger_config import get_logger


logger = get_logger(__name__)

def create():
    pass

def write_to_headers(headers: list):
    file_path = settings.DATABASE_PATH + "/company.csv"
    with open(file_path, 'w') as file:
        writer = csv.DictWriter(file, delimiter=',', lineterminator='\n', fieldnames=headers)
        writer.writeheader()

def write_to_csv(data: dict):
    file_path = settings.DATABASE_PATH + "/company.csv"
    with open(file_path, 'a') as file:
        try:
            writer = csv.writer(file)
            writer.writerow(data.values())
        except Exception as e:
            logger.error(e)


