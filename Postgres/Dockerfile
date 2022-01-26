FROM python:3

RUN apt-get install libpq-dev -y

RUN /usr/local/bin/python -m pip install --upgrade pip

RUN /usr/local/bin/python -m pip install --upgrade psycopg2

RUN mkdir /app

COPY create_user.py /app

ENTRYPOINT ["python","/app/create_user.py"]

CMD ["kiran","kiran.peddineni@duxxxby.com","Tesco_UK","Super User"]
