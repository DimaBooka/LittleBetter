from celery.task import periodic_task
from datetime import timedelta
import logging
from urllib.request import urlretrieve
from zipfile import ZipFile
import os
from djcelery import celery
from finder.models import ZipFiles
import shutil


logger = logging.getLogger(__name__)


@celery.task
def create_zip(query, urls):
    upload_folder = os.path.abspath(os.path.dirname(__file__))[:-7]
    if not os.path.exists('upload/' + query + '/'):
        os.makedirs('upload/' + query + '/')
    with ZipFile('upload/' + query + '/' + query + '.zip', 'w') as zip:
        for i in range(0, len(urls)):
            name_file = urls[i].split('/')[-1]
            try:
                format_images = name_file[name_file.find('.'):]
            except:
                format_images = '.jpg'
            urlretrieve(urls[i], 'upload/' + query + '/' + str(i) + format_images)
            zip.write('upload/' + query + '/' + str(i) + format_images)

    way = ''.join([upload_folder + '/upload/' + query + '/'])
    ZipFiles.objects.create(way=way, downloaded=False)
    return query + ' - done'


@periodic_task(run_every=timedelta(seconds=1000))
def clear_old():
    old_zip_files = ZipFiles.objects.filter(downloaded=True)
    for old in old_zip_files:
        shutil.rmtree(old.way)
    logging.info('May be some old zip files was remove!')
