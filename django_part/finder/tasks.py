import logging
import shutil
from urllib.request import urlretrieve
from zipfile import ZipFile
import os
import time
from .celery import app


logger = logging.getLogger(__name__)


@app.task
def create_zip(query, urls):
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

    return query + 'done'


@app.task
def clear_old():
    upload_folder = os.path.abspath(os.path.dirname(__file__))
    numdays = 1
    now = time.time()
    directory = os.path.join(upload_folder, '/upload/')
    for r, d, f in os.walk(directory):
        for dir in d:
            timestamp = os.path.getmtime(os.path.join(r, dir))
            print(timestamp)
            if now - numdays > timestamp:
                try:
                    shutil.rmtree(os.path.join(r, dir))
                except:
                    logging.error('Something goes wrong with removing old zip files!')
    return 'removed some folders'
