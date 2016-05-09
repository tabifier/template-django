SOURCE_DIR=`pwd`
source ./envs/localhost

docker exec euapi_api_mysql_db_1 mysql -uroot -p$MYSQL_ROOT_PASSWORD -e "
    DROP DATABASE IF EXISTS $MYSQL_DATABASE;
    CREATE DATABASE IF NOT EXISTS $MYSQL_DATABASE CHARACTER SET utf8;
    GRANT ALL PRIVILEGES ON *.* TO '$MYSQL_USER'@'%' IDENTIFIED BY '$MYSQL_PASSWORD';
    FLUSH PRIVILEGES;"

# docker exec -ti euapi_api_app_1 python manage.py reset_db --router=default --noinput
docker exec -ti euapi_api_app_1 python manage.py migrate
cd $SOURCE_DIR
