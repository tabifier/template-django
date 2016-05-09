#! /bin/sh
SOURCE_DIR=`pwd`
source ./envs/localhost

KILL_CURRENT_CONNECTIONS_SQL="
  SELECT pg_terminate_backend(pg_stat_activity.pid)
  FROM pg_stat_activity
  WHERE 1=1
    AND pg_stat_activity.datname = '"$POSTGRES_DB"'
    AND pid <> pg_backend_pid();
"

# KILL_CURRENT_CONNECTIONS_SQL="SELECT * FROM pg_stat_activity where datname='postgres'"
docker exec euapi_api_postgres_db_1 runuser -l postgres -c "psql -c \"$KILL_CURRENT_CONNECTIONS_SQL\""
docker exec euapi_api_postgres_db_1 runuser -l postgres -c "dropdb \"$POSTGRES_DB\""
docker exec euapi_api_postgres_db_1 runuser -l postgres -c "createdb \"$POSTGRES_DB\""

# # # docker exec -ti euapi_api_app_1 python manage.py reset_db --router=default --noinput
docker exec -ti euapi_api_app_1 python manage.py migrate
