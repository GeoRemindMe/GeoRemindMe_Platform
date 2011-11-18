#coding=utf-8


from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from timezones.fields import LocalizedDateTimeField
from webapp.site.fields import AutoSlugField

from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^timezones.fields.LocalizedDateTimeField"])


class Country(models.Model):
	name = models.CharField(_(u"Nombre"), max_length = 200)
	code = models.CharField(_(u"Codigo"), max_length = 2, db_index=True)
	population = models.IntegerField(_(u"Habitantes"))
	continent = models.CharField(_(u"Continente"), max_length = 2)
	tld = models.CharField(max_length = 5, unique=True)

	objects = models.GeoManager()

	def __unicode__(self):
		return unicode(self.name)

	@property
	def hierarchy(self):
		return [self]

	class Meta:
		ordering = ['name']
		verbose_name = _(u"País")
		verbose_name_plural = _(u"Países")


#------------------------------------------------------------------------------ 
class Region(models.Model):
	name = models.CharField(_(u"Nombre"), max_length = 200)
	slug = models.SlugField(max_length = 150)
	code = models.CharField(_(u"Codigo"), max_length = 10, db_index=True)
	country = models.ForeignKey(Country, verbose_name=_(u"País"),
							related_name='regions')
	objects = models.GeoManager()

	def __unicode__(self):
		return u"%s, %s" % (self.name, self.country)

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


#------------------------------------------------------------------------------ 
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
	slug = AutoSlugField(populate_from=['name', 'region'], max_length = 50)
	region = models.ForeignKey(Region, verbose_name=_(u"Región"),
							related_name="cities")
	location = models.PointField(_(u"Localización"), blank=True, null=True)
	population = models.IntegerField(_(u"Habitantes"), blank=True, null=True)

	objects = CityManager()

	def __unicode__(self):
		return u"%s, %s" % (self.name, self.region)

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
		


#------------------------------------------------------------------------------ 
class PlaceManager(models.GeoManager):
	def nearest_to(self, lat, lon):
		p = Point(float(lon), float(lat))
		return self.nearest_to_point(p)
	
	def create_from_google(self, **kwargs):
		if 'google_places_id' in kwargs:
			place = Place.objects.filter(google_places_id = kwargs['google_places_id'])
			if place is not None:
				return place
		from webapp.site.libs.mapsService.places import GPRequest, GPAPIError
		client = GPRequest()
		search = client.retrieve_reference(kwargs['google_places_reference'])
		place = Place.objects.filter(google_places_id = search['result']['id'])
		location= Point(search['result']['geometry']['location']['lng'],
						search['result']['geometry']['location']['lat'])
		try:
			city = client._get_city(search['result'].get('address_components'))
			city_obj = City.objects.filter(name__iexact = city)
		except City.DoesNotExist:
			try:
				region = client._get_region(search['result'].get('address_components'))
				region_obj = Region.objects.filter(name__iexact = region)
				city_obj = City.objects.create(name=city, 
											region=region_obj)
			except Region.DoesNotExist:
				try: 
					country = client._get_country(search['result'].get('address_components'))
					country_obj = Country.objects.filter(name__iexact = country)
					region_obj = Region.objects.create(name = region, 
													country = country_obj)
					city_obj = City.objects.create(name=city, region=region_obj)
				except Country.DoesNotExist:
					country_obj = Country.objects.create(name=country)
					region_obj = Region.objects.create(name = region, 
													country = country_obj)
					city_obj = City.objects.create(name=city, region=region_obj)
		Place.objects.create(name=search['result']['name'],
							location=location,
                            street=search['result'].get('formatted_address'),
                            city= city_obj,
                            google_places_reference=search['result']['reference'],
                            google_places_id=search['result']['id'],
                            user = kwargs['user']
                            )

		
class Place(models.Model):
	name = models.CharField(_(u"Nombre"), max_length = 200, blank=False)
	slug = AutoSlugField(populate_from=['name', 'city'], max_length = 50, db_index=True)
	location = models.PointField(_(u"location"), blank=False)
	city = models.ForeignKey(City, verbose_name=_(u"Ciudad"),
							related_name="places")
	street = models.CharField(_(u"Calle"), max_length=512, blank=True)
	phone = models.CharField(_(u"Teléfono"), max_length=32, blank=True)
	user = models.ForeignKey(User, verbose_name=_(u"Usuario"),
							related_name = "places")
	google_places_reference = models.CharField(_(u"Referencia de Google Places"),
											 max_length=232, 
											 blank=True,
											 db_index=True)
	google_places_id = models.CharField(_(u"ID de Google Places"), 
											max_length=232, 
											blank=True,
											db_index = True,
											unique = True)
	url = models.URLField(_(u"Web"), blank=True)
	_short_url = models.URLField(_(u"Atajo en vavag"), blank=True)
	created = LocalizedDateTimeField(_(u"Creado"), auto_now_add=True)
	modified = LocalizedDateTimeField(_(u"Modificado"), auto_now=True)
	
	objects = models.GeoManager()
	
	class Meta:
		ordering = ['name']
		order_with_respect_to = 'city'
		verbose_name = _(u'Sitio')
		verbose_name_plural = _(u'Sitios')
		
	def __unicode__(self):
		return unicode(self.name)
	
	@models.permalink
	def get_absolute_url(self):
		return ('places_place_detail', (), { 'slug': self.slug })
	
	@property
	def short_url(self):
		if self._short_url is None:
			from django.contrib.sites.models import Site
			from libs.vavag import VavagRequest
			from django.conf import settings        
			try:
				current_site = Site.objects.get_current()
				client = VavagRequest(settings.VAVAG_ACCESS['user'], settings.VAVAG_ACCESS['key'])
				
				response = client.set_pack('http://%s%s' % (current_site.domain, self.get_absolute_url()))
				self._short_url = response['packUrl']
				self.save()
			except Exception:
				self._short_url = None
				return 'http://%s%s' % (current_site.domain, self.get_absolute_url())
		return self._short_url

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
