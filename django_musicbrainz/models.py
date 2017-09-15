from __future__ unicdoe_literals
# can use python 2 with python 3 unicode operators such as ''u you do not have to write the u() function.

from django.db import models # import the models functions to add to our models below.

CHARACTER_VARYING_MAX_LENGTH = 10000 # Defining the max characters we can have in our strings, max is 1 GB.
# this links area, artist, label, place, recording, release, release_group, and work
# They all have a corresponding _annotation table that links entities of that type of entry to the main Annotation below.
# The main annotation table which contains the actual text of the annotation, along with the changelog and the
# identity of the editor who created it.
class Annotation(models.Model):
  id = models.IntegerField(primary_key=True)
  editor = models.ForeignKey('Editor', do_column='editor')
  text = models.TextField(blank=True)
  changelog = models.CharField(max_length=225, blank=True)
  created = models.DateTimeField(blank=True, null=True)
  
  # no DB table creation or deletion operations will be preformed for this model.
  # the name of the database table is db_table.
  class Meta:
      managed = False
      db_table = 'annotation'
      
# used for external application, we have a id for identitfy this table,
# we may not need this since we will not implement any 3rd party applications.
class Application(models.Model):
    id = models.IntegerField(primary_key=True)
    owner = models.ForeignKey('Editor', db_column='owner')
    name = models.TextField()
    oauth_id = models.TextField(unique=True)
    oauth_secret = models.TextField()
    oauth_redirect_uri = models.TextField(blank=True)
    
    class Meta:
      managed = False
      db_table = 'application'

# A country, region, city or the like.
class Area(models.Model):
    id = models.IntegerField(primary_key=True)
    gid = models.TextField(unique=True)
    name = models.CharField(max_length=CHARACTER_VARYING_MAX_LENGTH)
    type = models.ForeignKey(
          'AreaType', db_column='type', blank=True, null=True)
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    begin_date_year = models.SmallIntegerField(blank=True, null=True)
    begin_date_month = models.SmallIntegerField(blank=True, null=True)
    begin_date_day = models.SmallIntegerField(blank=True, null=True)
    end_date_year = models.SmallIntegerField(blank=True, null=True)
    end_date_month = models.SmallIntegerField(blank=True, null=True)
    end_date_day = models.SmallIntegerField(blank=True, null=True)
    ended = models.BooleanField()
    comment = models.CharField(max_length=225)
    
    # defing the annotation database table with area, to link to the main annotation table above.
    
    # manually specifiy the middle table, using through can allow django model to specify the middle table you want to use 
    # allowing annotation model to commuicate to areaAnnotation model.
    annotation = models.ManyToManyField(
         'Annotation', through='AreaAnnotation')
    areas = models.ManyToManyField('Area', through='LAreaArea')
    edits = models.ManyToManyField('Edit', through='EditArea')
    urls = models.ManyToManyField('Url', through='LAreaUrl')
    
    class Meta:
        managed = False
        db_table = 'area'

