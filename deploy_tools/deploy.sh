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
        server="staging.agripo-website.brice.xyz"
    else
        server="www.agripo.net"
fi

fab deploy:$1 --host=$server
