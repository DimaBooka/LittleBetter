from django.db import models
from django.contrib.auth.models import User


class ZipFiles(models.Model):
    way = models.CharField(max_length=1500, unique=True)
    downloaded = models.BooleanField()
    date = models.DateField(auto_now=True)

    def __str__(self):
        return "{0} | {1} | {2}".format(self.way,
                                        self.downloaded,
                                        self.date)


class Query(models.Model):
    query = models.CharField(max_length=150)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.SmallIntegerField()

    def __str__(self):
        return "{0} | {1} | {2}".format(self.query, self.status, self.author_id)


class Result(models.Model):
    query = models.ForeignKey(Query, on_delete=models.CASCADE)
    url = models.CharField(max_length=1500)
    spider = models.CharField(max_length=20)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    rang = models.PositiveIntegerField()

    def get_query(self, query):
        return Result.objects.filter(query__query=query)

    def __str__(self):
        return " {0} | {1} | {2} | {3} | {4} ".format(self.query,
                                                      self.url,
                                                      self.spider,
                                                      self.date,
                                                      self.rang)
