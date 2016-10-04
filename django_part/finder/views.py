from django.shortcuts import render
import logging
from django.template.context_processors import csrf
from django.shortcuts import render_to_response, redirect
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from sendfile import sendfile
import os
import time
import shutil


numdays = 86400 * 1
now = time.time()
upload_folder = os.path.abspath(os.path.dirname(__file__))
logger = logging.getLogger(__name__)


def main(request):
    directory = os.path.join(upload_folder[:-6], '/upload/')
    for r, d, f in os.walk(directory):
        for dir in d:
            timestamp = os.path.getmtime(os.path.join(r, dir))
            if now - numdays > timestamp:
                logging.info("removing ", os.path.join(r, dir))
                shutil.rmtree(os.path.join(r, dir))
    return render(request, 'index.html')


def login(request):
    args = dict()
    args.update(csrf(request))
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            args['login_error'] = "User is not found"
            return render_to_response('index.html', args)
    else:
        return render_to_response('index.html')


def logout(request):
    auth.logout(request)
    return redirect('/')


def register(request):
    args = dict()
    args.update(csrf(request))
    args['form'] = UserCreationForm()
    if request.method == 'POST':
        newuser_form = UserCreationForm(request.POST)
        if newuser_form.is_valid():
            newuser_form.save()
            newuser = auth.authenticate(username=newuser_form.cleaned_data['username'],
                                        password=newuser_form.cleaned_data['password2'], )
            auth.login(request, newuser)
            return redirect('/')
        else:
            args['form'] = newuser_form
    return render_to_response('user/registration.html', args)


def download(request, query):
    return sendfile(request, upload_folder[:-6] + '/upload/' + query + '/' + query + '.zip')
