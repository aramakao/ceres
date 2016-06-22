from django.db import models

class Country(models.Model):
    '''This model allows create countries'''
    name=models.CharField(max_length=20)

    def __unicode__(self):
        return self.name

class Region(models.Model):
    """This model allows create regions"""
    country=models.ForeignKey(Country)
    name=models.CharField(max_length=20)

    def __unicode__(self):
        """Metodo unicode"""
        return self.name

class City(models.Model):
    '''This model allows create cities'''
    country=models.ForeignKey(Country)
    region=models.ForeignKey(Region)
    name=models.CharField(max_length=20)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __unicode__(self):
        return self.name

class Occupation(models.Model):
    '''This model allows create occupations'''
    name=models.CharField(max_length=20)

    def __unicode__(self):
        return self.name
