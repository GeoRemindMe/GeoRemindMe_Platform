#coding=utf-8

from django.db import models
from django.contrib.contenttypes.models import ContentType

from models import Vote


class VotableManager(models.Manager):
    def has_voted(self, user):
        if not user.is_authenticated():
            return self.get_query_set()
        target_ct = ContentType.objects.get_for_model(self.model).pk
        table = Vote._meta.db_table
        table2 = self.model._meta.db_table
        select = 'SELECT True FROM %s' % table
        where1 = 'WHERE ' + table + '.user_id = %s'
        where2 = 'AND ' + table + '.target_id = ' + table2 + '.id'
        where3 = 'AND ' + table + '.target_c_type_id = %s'
        return self.get_query_set().extra(
                                          select={'has_voted':" ".join((select, where1, where2, where3))},
                                          select_params=(user.id, target_ct)
                                          )
        
