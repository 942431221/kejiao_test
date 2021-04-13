FROM python:3
EXPOSE 5000
RUN mkdir -p /opt/project
WORKDIR /opt/project
COPY * /opt/project
RUN pip install --no-cache-dir -r requirements.txt
ENV MYSQL_ALLOW_EMPTY_PASSWORD yes
CMD mysql -uroot -p < flask.sql
CMD python test.py
