from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Query, Result
from .forms import QueryForm
from .scrapyd_file import RunSpider
import logging
from.send_email import send_email as ALERT


logging.basicConfig(format=u'%(filename) 8s [LINE:%(lineno)d]# %(levelname)-3s [%(asctime)s] %(message)s',
                    level=logging.DEBUG, filename=u'all_logs.log')


def start(request):
    """

    Just show all old query for client.

    """
    form = QueryForm()
    links = Query.objects.filter(status='done').values_list('query', flat=True)
    return render(request, 'base.html', {'links': links, 'form': form})


def find(request):
    """

    Gets a word-query and runs skrapyd or redirect on url which shows images.

    """
    links = Query.objects.values_list('query', flat=True)
    urls = [q.replace(' ', '_') for q in links]
    if request.method == "POST":
        form = QueryForm(request.POST)
        if form.is_valid():
            try:
                query = request.POST.get('query')
                logging.info(u'Entered query is OK.')
            except:
                ALERT()
                logging.warning(u'Entered query is incorrect.')
                return HttpResponseRedirect('/')

            if query.replace(' ', '_') in urls:
                return HttpResponseRedirect('/' + query.replace(' ', '_') + '/')
            ret = RunSpider(query)
            response = ret.run()
            if isinstance(response, HttpResponseRedirect):
                return response
            Query.objects.create(query=query, status='create')
    else:
        form = QueryForm()
    return render(request, 'client.html', {'links': links, 'form': form, 'query': query})


def show(request, query):
    """
    Just shows the images at the word-query.

    :param:
        query: query-word from client (position);

    """
    form = QueryForm()
    try:
        pic = Result.objects.filter(query__query=query.replace('_', ' '),
                                    query__status='done').order_by('rang')
        logging.info(u'Successfully processed request.')
    except:
        ALERT()
        logging.error(u"Couldn't get data from sqlite.")
        return HttpResponseRedirect('/')
    links = Query.objects.filter(status='done').values_list('query', flat=True)
    return render(request, 'result.html', {'links': links, 'pic': pic, 'form': form})
