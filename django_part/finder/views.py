from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Query, Result
from .forms import QueryForm
from .errors import RunSpiderError
import logging
from .send_email import send_email as ALERT


logger = logging.getLogger(__name__)


def main(request):
    form = QueryForm()
    return render(request, 'index.html', {'form': form})

#
# def start(request):
#     """
#
#     Just show all old query for client.
#
#     """
#     form = QueryForm()
#     return render(request, 'base.html', {'form': form})
#
#
# def find(request):
#     """
#
#     Gets a word-query and runs skrapyd or redirect on url which shows images.
#
#     """
#     links = Query.objects.filter(status='done').values_list('query', flat=True)
#     if request.method == "POST":
#         form = QueryForm(request.POST)
#         if form.is_valid():
#             query = request.POST.get('query')
#             logger.info(u'Entered query is OK.')
#
#             if query in links:
#                 return HttpResponseRedirect('/' + query.replace(' ', '_') + '/')
#
#             try:
#                 new_query = Query(query=query, status='create')
#                 new_query.save()
#             except RunSpiderError:
#                 return render(request, 'error.html', {'form': form})
#         return render(request, 'client.html', {'form': form, 'query': query})
#
#
# def show(request, query):
#     """
#     Just shows the images at the word-query.
#
#     :param:
#         query: query-word from client (position);
#
#     """
#     form = QueryForm()
#     try:
#         pic = Result.objects.select_related('query').filter(query__query=query.replace('_', ' '),
#                                                             query__status='done').order_by('rang')
#         logger.info(u'Successfully processed request.')
#     except ConnectionRefusedError:
#         ALERT()
#         logger.error(u"Couldn't get data from postgresql.")
#         return render(request, 'error.html', {'form': form})
#
#     paginator = Paginator(pic, 24)  # Show 24 contacts per page
#     page = request.GET.get('page')
#     try:
#         pic = paginator.page(page)
#     except PageNotAnInteger:
#         pic = paginator.page(1)
#     except EmptyPage:
#         pic = paginator.page(paginator.num_pages)
#
#     return render(request, 'result.html', {'pic': pic, 'form': form})
