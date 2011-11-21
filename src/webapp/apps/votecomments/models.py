#coding=utf-8


from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _


class VoteManager(models.Manager):
    pass


class Vote(models.Model):
    user = models.ForeignKey(User,
                             verbose_name=_(u"User")
                             )
    instance_c_type = models.ForeignKey(ContentType,
                                        verbose_name = _(u"Tipo de objeto seguidor"),
                                        )
    instance_id = models.PositiveIntegerField(_(u"Identificador del seguidor"))
    instance = generic.GenericForeignKey('instance_c_type', 'instance_id',) # clave generica para cualquier modelo
    created = models.DateTimeField(auto_now_add=True)
    objects = VoteManager()
    
    
#------------------------------------------------------------------------------ 
class CommentManager(models.Manager):
    pass


class Comment(models.Model):
    user_c_type = models.ForeignKey(ContentType,
                                        verbose_name = _(u"Tipo de objeto creador"),
                                        related_name = "comments_done")
    user_id = models.PositiveIntegerField(_(u"Identificador del creador"))
    user = generic.GenericForeignKey('user_c_type', 'user_id',) # clave generica para cualquier modelo
    
    instance_c_type = models.ForeignKey(ContentType,
                                        verbose_name = _(u"Tipo de objeto comentado"),
                                        )
    instance_id = models.PositiveIntegerField(_(u"Identificador del creador"))
    instance = generic.GenericForeignKey('instance_c_type', 'instance_id',) # clave generica para cualquier modelo
    
    comment = models.TextField(_(u'Comentario'), blank=False)
    created = models.DateTimeField(_(u"Creado"), auto_now_add=True)
    deleted = models.BooleanField(_(u"Borrado"), default=False)
    
    objects = CommentManager()
    
    def __unicode__(self):
        return unicode('%s - %s: %s' % (self.user_id, self.instance_id, self.comment[:50]))
    
    def delete(self, *args, **kwargs):
        if not self.deleted:
            self.deleted = True
            return self.save()
        super(self.__class__, self).delete(*args, **kwargs)