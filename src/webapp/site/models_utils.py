#coding=utf-8

from django.db import models
from django.utils.translation import ugettext_lazy as _


VISIBILITY_CHOICES = (
          ('public', _('Pública')),
          ('private', _('Privada')),
          ('shared', _('Compartida')),
                      )
class Visibility(models.Model):
    """Metodos comunes heredados por todas las Clases que necesiten visibilidad"""
    _vis = models.CharField(_(u"Visibilidad"), 
                            choices = VISIBILITY_CHOICES, 
                            default = 'private', 
                            max_length=10)
    
    class Meta:
        abstract = True
        
    @property
    def visibility(self):
        return self.get__vis_display()
    
    def _is_public(self):
        if self._vis == 'public':
            return True
        return False
    
    def _is_private(self):
        if self._vis == 'private':
            return True
        return False
    
    def _is_shared(self):
        if self._vis == 'shared':
            return True
        return False
