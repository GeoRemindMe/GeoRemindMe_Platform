from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from guardian.admin import GuardedModelAdmin

from userena.models import UserenaSignup
from userena.utils import get_profile_model
from apps.profiles.models import UserProfile

class UserenaSignupInline(admin.StackedInline):
    model = UserenaSignup
    max_num = 1
    
class UserProfileAdmin(admin.StackedInline):
    model = UserProfile
#    readonly_fields = ('_get_counter_preinscripciones',)
#    list_filter = ('estado', 'ciudad')
    extra = 0
#    list_display = ('id','format_date','user','_get_nombre','_get_email','telefono',)
#    
#    def _get_nombre(self,obj):
#        return u"%s %s" % (obj.user.first_name, obj.user.last_name)
#    _get_nombre.short_description = "Nombre"
#    
#    def _get_email(self,obj):
#        return obj.user.email
#    _get_email.short_description = "Email"
#    
#    def format_date(self, obj):
#        return obj.user.date_joined.strftime('%d/%m/%y %H:%M')
#    format_date.short_description = u'Fecha'

class UserenaAdmin(UserAdmin, GuardedModelAdmin):
    inlines = [UserenaSignupInline, UserProfileAdmin]
    list_display = ('username', 'email', 'first_name', 'last_name',
                    'is_staff', 'date_joined')

admin.site.unregister(User)
admin.site.register(User, UserenaAdmin)
