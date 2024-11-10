from django.db import models
from django.db.models import Count

from wagtail_design_system.wagtail_design_system_blog.blocks import *


class TagManager(models.Manager):
    def tags_with_usecount(self, min_count=0):
        return self.annotate(usecount=Count("contentpage")).filter(usecount__gte=min_count)
