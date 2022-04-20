FROM python:3.8-buster

COPY . /app

WORKDIR /app

RUN pip install --upgrade setuptools

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]

CMD ["main.py"]