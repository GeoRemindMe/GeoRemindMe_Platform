# coding=utf-8

from django.db import models
from django.contrib.contenttypes.models import ContentType



class VoteManager(models.Manager):
    def has_voted(self, user, target):
        target_ct = ContentType.objects.get_for_model(target)
        return self.get_query_set().filter(user = user,
                                           target_c_type = target_ct,
                                           target_id=target.id, 
                                           ).exists()
    
    def toggle_vote(self, user, target, ip_address):
        target_ct = ContentType.objects.get_for_model(target)
        q = self.get_query_set().filter(user = user,
                                        target_c_type = target_ct,
                                        target_id=target.id, 
                                        )
        if q.exists():
            q.delete()
            return False
        else:
            self.create(user = user, target=target, ip_address=ip_address)
            return True


