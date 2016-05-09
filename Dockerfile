FROM python:2.7

RUN     apt-get update && apt-get install -y --no-install-recommends \
            postgresql-client \
            mysql-client libmysqlclient-dev \
            sqlite3
RUN     rm -rf /var/lib/apt/lists/*


ENV     PACKAGE_PATH /src
RUN     mkdir -p $PACKAGE_PATH
RUN     mkdir -p /nginx
COPY    . $PACKAGE_PATH
WORKDIR $PACKAGE_PATH/src
RUN     pip install --upgrade pip
RUN     pip install -r ../requirements.txt
RUN     python manage.py collectstatic --noinput

EXPOSE  8000
