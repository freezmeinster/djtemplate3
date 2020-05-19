from django.db import models
from django.db.models.query import QuerySet
from django.db.models.signals import pre_delete, post_delete
from django.utils import timezone
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

class DataQuerySet(QuerySet):
    pass


class DataManager(models.Manager):
    # use_for_related_fields = True

    def get_queryset(self):
        qs = self.get_full_queryset()
        return qs.filter(deleted__isnull=True)

    def get_full_queryset(self):
        qs = super().get_queryset()
        if not isinstance(qs, DataQuerySet):
            qs = DataQuerySet(self.model, using=self._db)
        return qs

    def get(self, *args, **kwargs):
        if "pk" in kwargs or "id" in kwargs:
            # because models are not deleted foreign keys might reference 'deleted data'
            # to not crash the admin in these cases, we let it still access this data
            # if explicitly asked for by id
            return self.get_full_queryset().get(*args, **kwargs)
        return self.get_queryset().get(*args, **kwargs)

    def filter(self, *args, **kwargs):
        if "pk" in kwargs or "id" in kwargs:
            return self.get_full_queryset().filter(*args, **kwargs)
        return self.get_queryset().filter(*args, **kwargs)

    def deleted(self):
        return self.get_full_queryset().filter(deleted__isnull=False)

    def visible(self):
        return self.filter(concealed=False)


class BaseModel(models.Model):

    created = models.DateTimeField(
        _("created"), auto_now_add=True, editable=False, db_index=True
    )
    modified = models.DateTimeField(auto_now=True, editable=False)
    deleted = models.DateTimeField(editable=False, null=True)

    objects = DataManager()

    class Meta:
        abstract = True
        ordering = ["-id"]
        get_latest_by = "id"
        base_manager_name = "objects"
        default_manager_name = "objects"
