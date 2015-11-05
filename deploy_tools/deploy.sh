#!/bin/bash

type="$2"
tag="$1"

list_available_tags () {
    echo "List of all the tags on current branch : "
    git for-each-ref --sort='*authordate' --shell | \
    while read entry
    do
        it_s_a_tag=false
        c=0
        for word in $entry
        do
            if [ "$c" -eq 1 ]; then
                if [ "$word" = "'tag'" ]; then
                    it_s_a_tag=true
                fi
            elif [ "$c" -eq 2 ]; then
                if [ "$it_s_a_tag" = true ]; then
                    tag="${word:11:${#word}-12}"
                    on_branch=`git branch --contains $tag | grep "*"`
                    if [ "$on_branch" != "" ]; then
                        echo "$tag"
                    fi
                fi
            fi
            c=$((c+1))
        done
    done
}

if [ -z $tag ]
    then
        echo "You should pass a git tag as first argument to this command. Here are the available tags : "
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
