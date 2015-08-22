#!/bin/bash

ps aux | grep gunicorn | grep agripo-staging.brice.xyz | awk '{ print $2 }' | xargs kill -HUP
