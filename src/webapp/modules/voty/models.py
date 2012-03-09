#coding=utf-8


from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from managers import VoteManager


class Vote(models.Model):
    user = models.ForeignKey(User,
                             verbose_name=_(u"User"),
                             db_index = True
                             )
    target_c_type = models.ForeignKey(ContentType,
                                        verbose_name = _(u"Tipo de objeto seguidor"),
                                        related_name='+',
                                        )
    target_id = models.IntegerField(_(u"Identificador del seguidor"))
    target = generic.GenericForeignKey('target_c_type', 'target_id',) # clave generica para cualquier modelo
    ip_address = models.IPAddressField()
    created = models.DateTimeField(auto_now_add=True)
    objects = VoteManager()
    
    class Meta:
        unique_together = ['user', 'target_c_type', 'target_id']
        verbose_name = _(u"Voto")
        verbose_name_plural = _(u"Votos")
        
    def __unicode__(self):
        return u'%s - %s - %s' % (self.user.username, self.target, self.created)
    
    def __str__(self):
        return unicode(self.__unicode__())
        
        
try:
    # south fails migrating with this code :)
    GenericModels = ['events.Suggestion', 'places.Place',]
    # from django-activity-stream
    from django.db.models import get_model
    for model in GenericModels:
        model = get_model(*model.split('.'))
        opts = model._meta
        generic.GenericRelation(Vote, content_type_field="target_c_type",
                                    object_id_field='target_id',
                                    related_name='votes_with_%s_as_target' % opts.module_name,
                                    ).contribute_to_class(model, 'target_in_votes')
        setattr(Vote, 'votes_with_target', None)
except:
    pass
        