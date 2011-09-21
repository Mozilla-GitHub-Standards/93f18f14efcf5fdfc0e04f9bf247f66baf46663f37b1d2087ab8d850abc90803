from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, pre_delete

from django_push.subscriber.models import Subscription
from django_push.subscriber.signals import updated

from tower import ugettext_lazy as _
from taggit.managers import TaggableManager

from innovate.models import BaseModel
from projects import tasks
from users.models import Profile


class Project(BaseModel):
    name = models.CharField(verbose_name=_(u'Name'), max_length=100)
    slug = models.SlugField(verbose_name=_(u'Slug'), unique=True,
                            max_length=100)
    description = models.CharField(verbose_name=_(u'Description'),
                                   max_length=200)
    long_description = models.TextField(verbose_name=_(u'Long Description'))
    image = models.ImageField(verbose_name=_(u'Image'), blank=True,
                              upload_to=settings.PROJECT_IMAGE_PATH,
                              null=True)
    featured_image = models.ImageField(verbose_name=_(u'Featured Image'),
                                       blank=True, null=True,
                                       upload_to=settings.PROJECT_IMAGE_PATH)
    team_members = models.ManyToManyField(Profile,
                                          verbose_name=_(u'Team Members'))
    topics = models.ManyToManyField('topics.Topic', verbose_name=_(u'Topics'))
    featured = models.BooleanField(default=False)
    followers = models.ManyToManyField(Profile,
                                       verbose_name=_(u'Followers'),
                                       related_name='projects_following')
    allow_participation = models.BooleanField(default=False,
        verbose_name=_(u'Allow user participation'))
    allow_sub_projects = models.BooleanField(default=False,
        verbose_name=_(u'Allow Sub-Projects'))
    """
    Need a way to reference the parent project - ID feel about right
    """
    parent_project_id = models.IntegerField(blank=True, null=True)
    sub_project_label = models.CharField(max_length=50,
        blank=True, null=True,
        verbose_name=_(u'What would you like to label your sub-projects as to the user?'))

    tags = TaggableManager(blank=True)

    @models.permalink
    def get_absolute_url(self):
        return ('projects_show', (), {
            'slug': self.slug
        })

    @property
    def image_url(self):
        media_url = getattr(settings, 'MEDIA_URL', '')
        path = lambda f: f and '%s%s' % (media_url, f)
        return path(self.image) or path('img/project-default.gif')

    @property
    def featured_image_or_default(self):
        return self.featured_image or 'img/featured-default.gif'

    @property
    def active_topics(self):
        return self.topics.filter(draft=False)

    @property
    def is_program(self):
        return len(self.tags.filter(name='program'))

    def __unicode__(self):
        return self.name


class Link(BaseModel):
    """
    A link that can be added to a project. Links can be 'subscribed' to, in
    which case, entries from the links RSS/Atom feed will be syndicated.
    """
    name = models.CharField(verbose_name=_(u'Name'), max_length=100)
    url = models.URLField(verbose_name=_(u'URL'))
    subscribe = models.BooleanField(default=False)
    subscription = models.ForeignKey(Subscription, null=True, blank=True)
    project = models.ForeignKey(Project, null=True, blank=True)
    featured = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s -> %s' % (self.name, self.url)


def link_subscriber(sender, instance, created, **kwargs):
    """Subscribe to link RSS/Atom feed."""
    if not isinstance(instance, Link) or not instance.subscribe:
        return
    if instance.subscription:
        return
    tasks.PushSubscriber.apply_async(args=(instance,))
post_save.connect(link_subscriber, sender=Link)


def link_delete_handler(sender, instance, **kwargs):
    """Send unsubscribe request to link hub."""
    if not isinstance(instance, Link):
        return
    tasks.PushUnsubscriber.apply_async(args=(instance,))
pre_delete.connect(link_delete_handler, sender=Link)


def notification_listener(notification, **kwargs):
    """Create entries for notification."""
    sender = kwargs.get('sender', None)
    if not sender:
        return
    tasks.PushNotificationHandler.apply_async(args=(notification, sender))
updated.connect(notification_listener)
