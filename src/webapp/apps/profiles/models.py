#coding=utf-8


from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from timezones.fields import TimeZoneField
from userena.models import UserenaLanguageBaseProfile
from userena.utils import get_gravatar
from socialregistration.contrib.facebook.models import FacebookProfile
from socialregistration.contrib.twitter.models import TwitterProfile

from webapp.site.fields import PositiveCounterField

from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^timezones.fields.TimeZoneField",])

class UserProfile(UserenaLanguageBaseProfile):
    AVATAR_CHOICES = (
                #(0, _(u'Avatar subido')),
                (1, _(u'Gravatar')),
                (2, _(u'Facebook')),
                (3, _(u'Twitter')),
    )
    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name=_(u"usuario"),
                                related_name='profile')
    
    description = models.CharField(_(u"Descripción"), max_length=100, blank=True)
    
    show_followers = models.BooleanField(_(u"Mostrar quien te sigue"),
                                         default=True, 
                                         )
    show_followings = models.BooleanField(_(u"Mostrar a quien sigues"),
                                         default=True, 
                                         )
    sync_avatar_with = models.PositiveSmallIntegerField(choices=AVATAR_CHOICES,
                                           default=1,
                                           verbose_name=_(u"Sincronizar tu avatar con")
                                          )
    counter_suggested =PositiveCounterField(_(u"Contador de sugerencias creadas"),
                                                    default=0,
                                                    )
    counter_followers = PositiveCounterField(_(u"Contador de seguidores"),
                                                    default=0,
                                                    )
    counter_followings = PositiveCounterField(_(u"Contador de seguidos"),
                                                     default=0,
                                                     )
    counter_notifications = PositiveCounterField(_(u"Contador de notificaciones pendientes"),
                                                        default=0,
                                                        )
    counter_supported = PositiveCounterField(_(u"Contador de votadas"),
                                                    default=0,
                                                    )
    last_location = models.PointField(_(u"Ultima localización usada"), blank=True, null=True)
    favorite_location = models.PointField(_(u"Localización favorita"), blank=True, null=True)
    timezone = TimeZoneField(_(u"Zona horaria"))
    
    class Meta:
        verbose_name = _(u"Perfil de usuario")
        verbose_name_plural = _(u"Perfiles de usuario")
    
    
    @models.permalink
    def get_absolute_url(self):
        return ('profiles_profile_public', (), { 'username': self.user.username })
    
    
    def get_mugshot_url(self):
        """
            (Basada en la funcion de userena)
            Devuelve la url donde esta la imagen que tenga seleccionada el usuario
            
            El usuario puede subir imagenes, usar gravatar, facebook o twitter
        """
        # First check for a mugshot and if any return that.
        if self.sync_avatar_with == 0 and self.mugshot:
            return self.mugshot.url
        elif self.sync_avatar_with == 1:
            return get_gravatar(self.user.email,
                                settings.USERENA_MUGSHOT_SIZE,
                                settings.USERENA_MUGSHOT_DEFAULT)
        elif self.sync_avatar_with == 2:
            facebook = FacebookProfile.objects.get(user=self.user)
            if facebook is not None:
                return facebook.get_avatar_url()
        elif self.sync_avatar_with == 3:
            twitter = TwitterProfile.objects.get(user=self.user)
            if twitter is not None:
                return twitter.get_avatar_url()
        return #settings.DEFAULT_AVATAR
