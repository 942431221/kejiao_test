FROM mysql:5.7.20
ENV MYSQL_ALLOW_EMPTY_PASSWORD yes
COPY setup.sh /mysql/setup.sh
ADD flask.sql /tmp/flask.sql
ADD privileges.sql /tmp/privileges.sql
CMD ["sh", "/mysql/setup.sh"]

