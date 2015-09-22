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

## This will only work when using Systemd. For upstart, the scripts in /root/reload_gunicorn have to be
#rewritten


# In the following, make those changes to the content of the files on the destination and in the command line
SITE_PORT : The port to listen to (set it to 80, most of the time)
DEFAULT_SERVER : Set it to "default_server" (without the ") if this host should be used by default, or remove it if not
SERVER_NAME : Set it to whatever you want to match this config (like staging.*, www.domain.tld, etc)
SITE_TYPE : Set it to whatever you want (like "staging" or "production". For any other value, a change should be made
            in the deploy script, in the last step, to launch the right gunicorn reloader script)
USER : The system user to use (no root user, please)

## Nginx Virtual Host config
# Send the content of nginx.template.conf to /etc/nginx/sites-available/{SITE_TYPE}_{SITE_PORT}
# Then execute the commands :
$ sudo ln -s /etc/nginx/sites-available/{SITE_TYPE}_{SITE_PORT} /etc/nginx/sites-enabled/{SITE_TYPE}_{SITE_PORT}
$ sudo service nginx restart

## Systemd Job for GUnicorn
# Send the content of gunicorn-systemd.template.conf to /etc/systemd/system/{SITE_TYPE}_{SITE_PORT}.conf

## Add sudo ability to the user without password
$ sudo visudo -f /etc/sudoers.d/reload_gunicorn
# and enter the following (don't forget to replace {USER} :
{USER} ALL=(root) NOPASSWD: /root/reload_gunicorn/

## Create the file /root/reload_gunicorn/{SITE_TYPE}.sh with the content of gunicorn_reloader.template.sh
# and set execute bit
$ sudo chmod +x /root/reload_gunicorn/{SITE_TYPE}.sh

## We should now be able to see a welcome message

## Before running the deploy.sh script for the first time, we have to update the gunicorn-systemd script
# to have it launch the good python wsgi script (replace mainapp by your main django application name).

## Folder structure
/home/{USER}
└── sites
    └── {SITE_TYPE}
         ├── database
         ├── source
         |   └── media
         ├── static
         └── virtualenv

