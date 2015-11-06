#!/bin/bash

type="$2"
tag="$1"

list_available_tags () {
    echo "List of all the tags on current branch : "
    tags=`git for-each-ref --format='%(*committerdate:raw)%(committerdate:raw) %(refname) %(*objectname) %(objectname)' refs/tags | sort -n | awk '{ print $3; }'`
    for word in $tags
    do
        tag="${word:10}"
        on_branch=`git branch --contains $tag | grep "*"`
        if [ "$on_branch" != "" ]; then
            echo "$tag"
        fi
    done
}

if [ -z $tag ]
    then
        echo "You should pass a git tag as first argument to this command."
        list_available_tags
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
        active_branch=`git name-rev --name-only HEAD`
        if [ "$active_branch" != "master" ]; then
            echo "Error! You have to be on master to push to production"
            exit
        fi
        server="www.agripo.net"
fi

fab deploy:$1 --host=$server
