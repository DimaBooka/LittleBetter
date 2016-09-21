from django.db import models


class Query(models.Model):
    query = models.CharField(max_length=150, unique=True)
    status = models.CharField(max_length=50)

    def __str__(self):
        return "{0} | {1}".format(self.query, self.status)


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
                                                      self.image_url,
                                                      self.spider,
                                                      self.date,
                                                      self.rang)
