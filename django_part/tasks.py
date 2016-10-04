from celery import Celery
from urllib.request import urlretrieve
from zipfile import ZipFile
import os


app = Celery('tasks', backend='redis://localhost', broker='redis://localhost:6379/0')


@app.task
def create_zip(query, urls):
    if not os.path.exists('upload/' + query + '/'):
        os.makedirs('upload/' + query + '/')

    with ZipFile('upload/' + query + '/' + query + '.zip', 'w') as zip:
        for i in range(0, len(urls)):
            if '.jpg' in urls[i] or '.jpeg' in urls[i]:
                format_images = '.jpeg'
            elif '.png' in urls[i]:
                format_images = '.png'
            elif '.gif' in urls[i]:
                format_images = '.gif'
            elif '.pdf' in urls[i]:
                format_images = '.pdf'
            else:
                format_images = '.jpg'
            urlretrieve(urls[i], 'upload/' + query + '/' + str(i) + format_images)
            zip.write('upload/' + query + '/' + str(i) + format_images)

    return query + 'done'
