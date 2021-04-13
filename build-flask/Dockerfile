#FROM python:3
FROM docker.io/larsklitzke/mysql-python3.5
ENV MYSQL_ALLOW_EMPTY_PASSWORD yes
WORKDIR /opt/project
RUN mkdir -p /opt/project
COPY * /opt/project/
RUN pip3 install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD ["python3","test.py"]
