Provisioning a new site
=======================

## Required packages:

* nginx
* Python 3
* Git
* pip
* virtualenv

eg, on Ubuntu:

    sudo apt-get install nginx git python3 python3-pip
    sudo pip3 install virtualenv

## Nginx Virtual Host config

* see nginx.template.conf
* replace SITENAME with, eg, staging.my-domain.com
sed "s/SITENAME/agripo-staging.brice.xyz/g" ./source/deploy_tools/nginx.template.conf | sudo tee /etc/nginx/sites-available/agripo-staging.brice.xyz

## Upstart Job

* see gunicorn-upstart.template.conf
* replace SITENAME with, eg, staging.my-domain.com
sed "s/SITENAME/agripo-staging.brice.xyz/g" ./source/deploy_tools/gunicorn-upstart.template.conf | sudo tee /etc/init/gunicorn-agripo-staging.brice.xyz.conf

## Folder structure:
Assume we have a user account at /home/username

/home/username
└── sites
    └── SITENAME
         ├── database
         ├── source
         ├── static
         └── virtualenv
