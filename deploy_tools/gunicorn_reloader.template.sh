#!/bin/bash

echo "Restarting gunicorn for {SITE_TYPE} server"

systemctl restart gunicorn-{SITE_TYPE}
