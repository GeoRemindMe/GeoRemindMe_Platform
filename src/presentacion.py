from geouser.models import *

#u1 = User.register(email='test@test.com', password='123456', username='usertest')
#u2 = User.register(email='test2@test.com', password='123456', username='usertest2')
u1 = User.objects.get_by_email('test@test.com')
u2 = User.objects.get_by_email('test2@test.com')

print u1.get_timelinesystem()
print '===='
print u2.get_timelineALL()

print u1.add_following(followname=u2.username)
print u1.counters().followings
print u2.counters().followers
print '====FOLLOWS==='
print u1.get_followings()
print u2.get_followers()
print '====TIMELINE==='
print u1.get_timeline()
print u1.get_timelinesystem()
print u2.get_timelineALL()

u1.del_following(followid=u2.id)
print u1.counters().followings
print u2.counters().followers
print '====FOLLOWS==='
print u1.get_followings()
print u2.get_followers()
print '====TIMELINE==='
print u1.get_timelinesystem()
print u2.get_timelineALL()

print u1.add_following(followname=u2.username)

print u1.counters().followings
print u2.counters().followers

u2.write_timeline(msg='mensaje')
print u2.get_timeline()
print u1.get_chronology()

#===============================================================================
# LISTAS DE USUARIOS
#===============================================================================
from geolist.models import *

l = ListUser.insert_list(u1, 'usuarios', instances=[u2])
print l
print l.keys
print l.to_dict()

l2 = ListUser.insert_list(u1, 'blabal', instances=[u2])
print l2
print l2.keys
print l2.to_dict()

print u1.listuser_set.count()

#===============================================================================
# ALERTAS
#===============================================================================
from geoalert.models import *
poi = PrivatePlace.get_or_insert(id = None, name=None, bookmark=False, address = None, business = None, location = '1,2', user = u1)
poi2 = PrivatePlace.get_or_insert(id = None, name=None, bookmark=False, address = None, business = None, location = '1,2', user = u2)
a = Alert.update_or_insert(name='prueba', description='asdf', poi=poi, user=u1)
a = Alert.update_or_insert(name='prueba', description='asdf', poi=poi, user=u1)

from geolist.models import *
l = ListAlert.insert_list(u1, 'alertas', instances=[a,a2])
print l
print l.keys
print l.to_dict()

#===============================================================================
# SUGERENCIAS
#===============================================================================
from geoalert.views import search_place
a = search_place(db.GeoPt(37.20631,-3.595849))
print a

from geoalert.models import *
p = Place.objects.get_by_id(11)
a = Suggestion.update_or_insert(name='prueba', description='asdf', poi=p, user=u)
a = Suggestion.update_or_insert(name='prueba', description='asdf', poi=p, user=u, vis='private')

a.del_follower(u2)
a.add_follower(u2)