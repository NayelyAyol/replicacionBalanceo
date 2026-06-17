FROM python:latest

COPY . .

RUN pip install flask
RUN pip install mysql-connector-python

EXPOSE 8100

CMD ["python", "app2.py"]