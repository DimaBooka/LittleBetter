from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Query, Result
from .forms import QueryForm
from .scrapyd_file import RunSpider
import logging
from.send_email import send_email as ALERT


logger = logging.getLogger(__name__)


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
    form = QueryForm()
    links = Query.objects.values_list('query', flat=True)
    urls = [q.replace(' ', '_') for q in links]
    if request.method == "POST":
        form = QueryForm(request.POST)
        if form.is_valid():
            try:
                query = request.POST.get('query')
                logger.info(u'Entered query is OK.')
            except:
                ALERT()
                logger.warning(u'Entered query is incorrect.')
                return render(request, 'error.html', {'links': links, 'form': form})

            if query.replace(' ', '_') in urls:
                return HttpResponseRedirect('/' + query.replace(' ', '_') + '/')
            ret = RunSpider(query)
            response = ret.run()
            if isinstance(response, HttpResponseRedirect):
                return render(request, 'error.html', {'links': links, 'form': form})
            Query.objects.create(query=query, status='create')
    return render(request, 'client.html', {'links': links, 'form': form, 'query': query})


def show(request, query):
    """
    Just shows the images at the word-query.

    :param:
        query: query-word from client (position);

    """
    links = Query.objects.filter(status='done').values_list('query', flat=True)
    form = QueryForm()
    try:
        pic = Result.objects.select_related('query').filter(query__query=query.replace('_', ' '),
                                                            query__status='done').order_by('rang')
        logger.info(u'Successfully processed request.')
    except:
        ALERT()
        logger.error(u"Couldn't get data from sqlite.")
        return render(request, 'error.html', {'links': links, 'form': form})

    paginator = Paginator(pic, 24)  # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        pic = paginator.page(page)
    except PageNotAnInteger:
        pic = paginator.page(1)
    except EmptyPage:
        pic = paginator.page(paginator.num_pages)


    return render(request, 'result.html', {'links': links, 'pic': pic, 'form': form})
