FROM python:3.8-alpine

COPY . /SmartHome-FrontEnd
WORKDIR /SmartHome-FrontEnd

RUN pip install -r requirements.txt

EXPOSE 5000
CMD ["gunicorn"  , "--bind", "0.0.0.0:5000", "flaskr:create_app()"]