import sys

from apps.parsing.ver1.main import main
from database.crud import write_to_csv, write_to_headers


if __name__ == "__main__":

    try:
        match sys.argv[1]:
            case "parsing":
                main()
    except IndexError:
        ...