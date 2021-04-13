FROM python:3
EXPOSE 5000
WORKDIR /opt/project
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . /opt/project
CMD python manage.py