#!/bin/bash

type="$2"
tag="$1"

if [ -z $tag ]
    then
        echo "You should pass a git tag as first argument to this comand. Here are the available tags : "
        git log --tags --pretty="format:%ci %d" | grep "tag:"
        exit
fi

if [ -z $type ]
    then
        echo "Type automatically set to staging"
        type="staging"
fi

if [ $type = "staging" ]
    then
        server="agripo-staging.brice.xyz"
    else
        server="agripo.brice.xyz"
fi

fab deploy:$1 --host=$server

ssh brice.xyz "bash /home/brice/sites/agripo-staging.brice.xyz/source/deploy_tools/restart_gunicorn.sh"
