FROM python:3.8.5 

WORKDIR /code
COPY requirements.txt ./
RUN pip install -r /code/requirements.txt 
COPY . /code 
RUN python manage.py collectstatic --noinput