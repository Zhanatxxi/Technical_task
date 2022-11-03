FROM python:3.10.8-alpine3.16

WORKDIR /project/test_project/

COPY . .

RUN pip install -r requirements.txt

CMD [ "python", "manage.py", "parsing" ]