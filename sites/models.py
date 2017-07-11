from django.db import models

# Create your models here.


class Site(models.Model):

    name = models.CharField(u'Name', max_length=50)


    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class SiteData(models.Model):
    site = models.ForeignKey(Site, related_name='sitedata')
    date = models.DateField(u'Date')
    a_value = models.FloatField(u'A value')
    b_value = models.FloatField(u'B value')