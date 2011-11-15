#coding=utf-8


from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.auth.models import User

from django.utils.translation import ugettext_lazy as _
from fields import AutoSlugField

class Country(models.Model):
	name = models.CharField(_(u"Nombre"), max_length = 200)
	code = models.CharField(_(u"Codigo"), max_length = 2, db_index=True)
	population = models.IntegerField(_(u"Habitantes"))
	continent = models.CharField(_(u"Continente"), max_length = 2)
	tld = models.CharField(max_length = 5, unique=True)

	objects = models.GeoManager()

	def __unicode__(self):
		return self.name

	@property
	def hierarchy(self):
		return [self]

	class Meta:
		ordering = ['name']
		verbose_name = _(u"País")
		verbose_name_plural = _(u"Países")

class Region(models.Model):
	name = models.CharField(_(u"Nombre"), max_length = 200)
	slug = models.SlugField(max_length = 150, unique=True, blank=True)
	code = models.CharField(_(u"Codigo"), max_length = 10, db_index=True)
	country = models.ForeignKey(Country, verbose_name=_(u"País"),
							related_name='regions')
	objects = models.GeoManager()

	def __unicode__(self):
		return "%s, %s" % (self.name, self.country)

	@property
	def hierarchy(self):
		list = self.country.hierarchy
		list.append(self)
		return list
	
	class Meta:
		ordering = ['name']
		order_with_respect_to = 'country'
		verbose_name = _(u'Región')
		verbose_name_plural = _(u'Regiones')

class CityManager(models.GeoManager):
	def nearest_to(self, lat, lon):
		#Wrong x y order
		#p = Point(float(lat), float(lon))
		p = Point(float(lon), float(lat))
		return self.nearest_to_point(p)

	def nearest_to_point(self, point):
		return self.distance(point).order_by('distance')[0]

class City(models.Model):
	name = models.CharField(_(u"Nombre"), max_length = 200)
	slug = models.SlugField(max_length = 150, unique=True, blank=True)
	region = models.ForeignKey(Region, verbose_name=_(u"Región"),
							related_name="cities")
	location = models.PointField(_(u"Localización"))
	population = models.IntegerField(_(u"Habitantes"))

	objects = CityManager()

	def __unicode__(self):
		return "%s, %s" % (self.name, self.region)

	@property
	def hierarchy(self):
		list = self.region.hierarchy
		list.append(self)
		return list
	
	class Meta:
		ordering = ['name']
		order_with_respect_to = 'region'
		verbose_name = _(u'Ciudad')
		verbose_name_plural = _(u'Ciudades')
		

class Place(models.Model):
	name = models.CharField(_(u"Nombre"), max_length = 200, db_index=True, blank=False)
	slug = AutoSlugField(populate_from=['name', 'city'], max_length = 50, unique=True)
	location = models.PointField(_(u"location"), blank=False)
	city = models.ForeignKey(City, verbose_name=_(u"Ciudad"),
							related_name="places")
	street = models.CharField(_(u"Calle"), max_length=256)
	num = models.IntegerField(_(u"Número"))
	phone = models.CharField(_(u"Teléfono"), max_length=32)
	user = models.ForeignKey(User, verbose_name=_(u"Usuario"),
							related_name = "places")
	google_places_reference = models.CharField(_(u"Referencia de Google Places"),
											 max_length=232, 
											 blank=True,
											 db_index=True)
	google_places_id = models.CharField(_(u"ID de Google Places"), max_length=232, blank=True)
	
	objects = models.GeoManager()
	
	class Meta:
		ordering = ['name']
		order_with_respect_to = 'city'
		verbose_name = _(u'Sitio')
		verbose_name_plural = _(u'Sitios')
		
	def __unicode__(self):
		return self.name

#===========================================================================
# Traduccion de modelos
#===========================================================================
from datatrans.utils import register
class RegionTranslation(object):
	fields = ('name')


class CountryTranslation(object):
	fields = ('name')


register(Country, CountryTranslation)
register(Region, RegionTranslation)

#class District(models.Model):
#	name = models.CharField(max_length = 200)
#	slug = models.CharField(max_length = 200, db_index=True)
#	city = models.ForeignKey(City)
#	location = models.PointField()
#	population = models.IntegerField()
#
#	objects = models.GeoManager()
#
#	def __unicode__(self):
#		return u"%s, %s" % (self.name, self.city)
#
#	@property
#	def hierarchy(self):
#		list = self.city.hierarchy
#		list.append(self)
#		return list
#	
#	class Meta:
#		ordering = ['name']
#		order_with_respect_to = 'city'
#		verbose_name = _(u'Distrito')
#		verbose_name_plural = _(u'Distritos')
