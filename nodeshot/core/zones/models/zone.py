from django.db import models
from django.utils.translation import ugettext_lazy as _
from nodeshot.core.base.models import BaseDate
from nodeshot.core.base.choices import TIME_ZONES

class Zone(BaseDate):
    name = models.CharField(_('name'), max_length=50, unique=True)
    parent = models.ForeignKey('Zone', blank=True, null=True)
    time_zone = models.CharField(_('time zone'), max_length=8, choices=TIME_ZONES)
    description = models.CharField(_('description'), max_length=250, blank=True, null=True)
    slug = models.SlugField(max_length=50, db_index=True, unique=True)
    lat = models.FloatField(_('center latitude'))
    lng = models.FloatField(_('center longitude'))
    is_external = models.BooleanField()
    
    class Meta:
        db_table = 'zones_zone'
        app_label= 'zones'