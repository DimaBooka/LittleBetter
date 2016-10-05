import logging
from sendfile import sendfile
from .models import ZipFiles
import os


logger = logging.getLogger(__name__)


def download(request, query):

    upload_folder = os.path.abspath(os.path.dirname(__file__))[:-7]
    logging.info(upload_folder)
    zip = ZipFiles.objects.get(way=upload_folder + '/upload/' + query + '/')
    zip.downloaded = True
    zip.save()
    return sendfile(request, upload_folder + '/upload/' + query + '/' + query + '.zip')
