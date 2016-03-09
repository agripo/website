import io
import json
import os
import subprocess
import tarfile

from django.conf import settings
from django.core.management import call_command
from django.utils import timezone
from django.utils import dateparse


def get_backup_file():
    if hasattr(settings, 'BACKUP_DIR'):
        base_dir = settings.BACKUP_DIR
    else:
        base_dir = settings.BASE_DIR + "/backup/"

    date = timezone.now().date().strftime('%Y-%m-%d')
    name = base_dir + date + ".tar.gz"
    return name


def _add_json_file_to_tar(tar, filename, content):
    tarinfo = tarfile.TarInfo(filename)
    content = json.dumps(content)
    tarinfo.size = len(content)
    tar.addfile(tarinfo, io.BytesIO(content.encode('utf8')))


def backup():
    """
    Creating a backup of the database and the media files, and removes older backups.
    We keep the following backups :
    - the last one for today
    - one for the last 7 days
    - every monday's for the last 5 weeks
    - every first monday's for the last 12 months
    """
    # backup file name
    backup_file = get_backup_file()

    backup_dir = os.path.dirname(backup_file)
    if not os.path.exists(backup_dir):
        os.mkdir(backup_dir)

    # db backup
    json_temp_dump = backup_dir + 'db.json'
    call_command('dumpdata', output=json_temp_dump)

    # media files backup
    tar = tarfile.open(backup_file, "w:gz")
    tar.add(settings.MEDIA_ROOT, arcname="media")
    tar.add(json_temp_dump, arcname="db.json")
    tag = subprocess.check_output(["git", "describe"])
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"])
    data = dict(
        date=timezone.now().strftime("%Y-%m-%d"),
        time=timezone.now().strftime("%H:%m"),
        tag=str(tag.strip()),
        commit=str(commit.strip())
    )
    _add_json_file_to_tar(tar, "data.json", data)
    tar.close()

    # Cleaning
    os.unlink(json_temp_dump)

    # Removing older backups
    for backup_file in os.listdir(backup_dir):
        if backup_file.endswith(".tar.gz"):
            backup_date = dateparse.parse_date(backup_file[:-7])
            now = timezone.now()
            last_week = (now - timezone.timedelta(8)).date()
            last_monday = (now - timezone.timedelta(now.isoweekday() - 1))
            five_weeks_ago = (last_monday - timezone.timedelta(7 * 5)).date()
            one_year_ago = (last_monday - timezone.timedelta(7 * 52)).date()

            keep = backup_date > last_week  # Last week's backups
            is_monday = backup_date.isoweekday() == 1
            keep = keep or (is_monday and backup_date > five_weeks_ago)  # last 5 mondays' backups
            # Last year's first mondays of the months
            keep = keep or (is_monday and backup_date.day < 8 and backup_date > one_year_ago)

            if not keep:
                os.unlink(backup_dir + "/" + backup_file)
