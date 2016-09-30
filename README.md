Install two virtualenv via command `virtualenv -p `pythonversion` .name`:
```
1. python2 for scrapy_part;
2. python3 for django_part.
```
Make scrapyd-deploy when you in 'links_finder' folder using `scrapyd-deploy links_finder`.
<br>
For running:
```
1. Enter to virtual environment for django_part and type: `python manage.py runserver`(run django server);
2. Open another terminal, enter in the same directory as first one and type: `python manage.py run_all` (run autobahn server);
2. Enter to virtual environment for scrapy_part and type: `scrapyd` (run scrapyd);
```