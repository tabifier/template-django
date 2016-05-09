alias d="docker"
alias dm="docker-machine"
alias dc="docker-compose"
# drm - force delete all containers expect the ones that have "data" in their names
alias drm='docker rm -f $(comm -13 <(docker ps -a -q --filter="name=data" | sort) <(docker ps -a -q | sort))'
# dps - docker ps -a
alias dps="docker ps -a"
# dsh - run bash in the app server
# alias dsh="dc run api_app bash"
alias dsh="docker exec -it euapi_api_app_1 bash"
# dstats - live stream stats on the running container
alias dstats="docker stats $(docker ps -a -q)"
# dcommit_last - take a snap shot and commit the latest app container - useful after installing packages like pip, bundle, and npm
alias dcommit_last='docker commit $(dps --filter="name=euapi_api_app" -l -q) $(docker inspect -f "{{ .Config.Image}}" $(dps --filter="name=euapi_api_app" -l -q))'
