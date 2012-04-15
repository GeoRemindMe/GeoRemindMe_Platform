#coding=utf-8


from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.db.models import F
from django.db import transaction
from userena.models import UserenaLanguageBaseProfile
from userena.managers import UserenaBaseProfileManager
from userena.utils import get_gravatar
from socialregistration.contrib.facebook.models import FacebookProfile
from socialregistration.contrib.twitter.models import TwitterProfile

from libs.fields import PositiveCounterField


class UserProfileManager(UserenaBaseProfileManager):
    def set_suggested(self, user, value=1):
        return self._set_counter(user=user, counter='counter_suggested', value=value)
    
    def set_followers(self, user, value=1):
        return self._set_counter(user=user, counter='counter_followers', value=value)
    
    def set_followings(self, user, value=1):
        return self._set_counter(user=user, counter='counter_followings', value=value)
    
    def set_supported(self, user, value=1):
        return self._set_counter(user=user, counter='counter_supported', value=value)
    
    @transaction.commit_manually
    def set_notifications(self, user, value=1):
        if value > 0:
            return self._set_counter(user=user, counter='counter_notifications', value=value)
        try:
            obj = self.get(user=user)
            obj.counter_notifications += value
            obj.save()
        except:
            transaction.rollback()
        else:
            transaction.commit()
        return obj.counter_notifications
    
    def _set_counter(self, user, counter, value=1):
        return self.filter(
                            user = user
                           ).update(
                                    **{counter: F(counter) + value}
                                    )

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
    timezone = models.CharField(_(u"Zona horaria"), default='Europe/Madrid', max_length=256)
    
    objects = UserProfileManager()
    
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
