#coding=utf-8

from django.db import models
from django.utils.translation import ugettext_lazy as _


VISIBILITY_CHOICES = (
          ('public', _('Publica')),
          ('private', _('Privada')),
          ('shared', _('Compartida')),
                      )
class Visibility(models.Model):
    """Metodos comunes heredados por todas las Clases que necesiten visibilidad"""
    _vis = models.CharField(choices = VISIBILITY_CHOICES, default = 'public', max_length=10)
    
    class Meta:
        abstract = True

    def _get_visibility(self):
        return self._vis
    
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
