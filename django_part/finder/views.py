from django.shortcuts import render, render_to_response, redirect
import logging
from django.template.context_processors import csrf
from django.shortcuts import render_to_response, redirect
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm


logger = logging.getLogger(__name__)


def main(request):
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
