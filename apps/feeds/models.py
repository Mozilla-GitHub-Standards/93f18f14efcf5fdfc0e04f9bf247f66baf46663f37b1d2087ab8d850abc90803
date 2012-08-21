import datetime

from django.contrib import admin
from django.db import models
from django.db.models.signals import post_save

from innovate.models import BaseModel
from activity.models import broadcast


class Entry(BaseModel):
    title = models.CharField(max_length=100)
    published = models.DateTimeField(default=datetime.datetime.utcnow())
    url = models.URLField()
    body = models.TextField()
    link = models.ForeignKey('projects.Link')

    class Meta:
        verbose_name_plural = u'entries'

    def __unicode__(self):
        return u'%s -> %s' % (self.title, self.url)

    @property
    def project(self):
        return self.link.project or None
admin.site.register(Entry)


def entry_save_handler(sender, instance, **kwargs):
    broadcast(instance)
post_save.connect(entry_save_handler, sender=Entry)
