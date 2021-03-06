from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run, put
import random
import datetime

REPO_URL = 'git@github.com:agripo/website.git'
MAIN_APP = 'agripo_website'
VIRTUALENV_FOLDER_NAME = 'env'

env.forward_agent = True

STAGING = False


def deploy(tag):
    global STAGING

    server_type_name = "production"
    if 'staging.' in env.host:
        STAGING = True
        server_type_name = "staging"
    else:
        if not tag.lower().startswith("release-") and not tag.lower().startswith("hotfix-"):
            raise Exception('Deployment on production is limited to the "release-*" and "hotfix-*" tags')

    print("Deploying tag {} to {} ({})".format(tag, env.host, server_type_name))

    site_folder = '/home/%s/sites/%s' % (env.user, server_type_name)
    source_folder = site_folder + '/source'
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder, tag)
    _update_settings(source_folder, env.host)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)
    #_update_flatpages(source_folder)
    _restart_gunicorn(server_type_name)
    print("CAUTION! FlatPages are not automatically inserted anymore (they were not aware of newer versions)!!")


def _create_directory_structure_if_necessary(site_folder):
    run('mkdir -p {}'.format(site_folder))
    directories = ""
    for subfolder in ('database', 'static', VIRTUALENV_FOLDER_NAME, 'source'):
        directories = "{} {}".format(directories, subfolder)

    run('cd {} && mkdir -p {}'.format(site_folder, directories))


def _get_latest_source(source_folder, deploy_tag):
    local("git push && git push --tags")

    if exists(source_folder + '/.git'):
        run('cd %s && git fetch' % (source_folder,))
    else:
        run('cd {}/.. && mv source old_source 2>/dev/null'.format(source_folder))
        run('git clone %s %s' % (REPO_URL, source_folder))

    run('cd %s && git reset --hard %s' % (source_folder, deploy_tag))

    if not STAGING:
        # We add a tag to mark the deployment
        deploy_tag = 'deployed-{}'.format(datetime.datetime.today().strftime('%Y-%m-%d_%H-%M'))
        deploy_message = 'Deployed automatically using Fabric, from tag {}'.format(deploy_tag)
        local("cd .. && git tag -a '{}' -m '{}'".format(deploy_tag, deploy_message))
        local("cd .. && git push --tags")


def _update_settings(source_folder, site_name):
    settings_path = '{}/{}/settings.py'.format(source_folder, MAIN_APP)
    sed(settings_path, "DEBUG = True", "DEBUG = False")
    # We get the last line, which is the IP address (there might be a CNAME entry at the beginning of the output)
    ip = local('dig +short {} | tail -n1;'.format(site_name), capture=True)
    sed(settings_path, 'ALLOWED_HOSTS = [DOMAIN, "127.0.0.1"]', 'ALLOWED_HOSTS = [DOMAIN, "{}"]'.format(ip))
    sed(settings_path, 'DOMAIN = "agripo-dev.brice.xyz"', 'DOMAIN = "%s"' % (site_name,))
    if STAGING:
        sed(settings_path, 'SERVER_TYPE = SERVER_TYPE_DEVELOPMENT', 'SERVER_TYPE = SERVER_TYPE_STAGING')
    else:
        sed(settings_path, 'SERVER_TYPE = SERVER_TYPE_DEVELOPMENT', 'SERVER_TYPE = SERVER_TYPE_PRODUCTION')

    secret_key_file = '{}/{}/secret_key.py'.format(source_folder, MAIN_APP)
    if not exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, "SECRET_KEY = '%s'" % (key,))

    append(settings_path, '\nfrom .secret_key import SECRET_KEY')


def _update_virtualenv(source_folder):
    virtualenv_folder = '{}/../{}'.format(source_folder, VIRTUALENV_FOLDER_NAME)
    if not exists(virtualenv_folder + '/bin/pip'):
        run('virtualenv --python=python3 %s' % (virtualenv_folder,))

    print("The virtualenv should now exist at {}".format(virtualenv_folder))

    run('%s/bin/pip install -r %s/requirements.txt' % (
            virtualenv_folder, source_folder
    ))
    

def _get_manage_dot_py_command(source_folder):
    return 'cd {} && ../{}/bin/python3 manage.py'.format(source_folder, VIRTUALENV_FOLDER_NAME)


def _update_static_files(source_folder):
    run(_get_manage_dot_py_command(source_folder) + ' collectstatic --noinput')


def _update_database(source_folder):
    run(_get_manage_dot_py_command(source_folder) + ' migrate --noinput')


def _update_flatpages(source_folder):
    run(_get_manage_dot_py_command(source_folder) + ' loaddata core/flatpages_contents.json')


def _restart_gunicorn(server_type_name):
    run("sudo /root/reload_gunicorn/{}.sh".format(server_type_name))
