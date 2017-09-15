from __future__ unicdoe_literals
# can use python 2 with python 3 unicode operators such as ''u you do not have to write the u() function.

from django.db import models # import the models functions to add to our models below.

CHARACTER_VARYING_MAX_LENGTH = 10000 # Defining the max characters we can have in our strings, max is 1 GB.
# this links area, artist, label, place, recording, release, release_group, and work
# They all have a corresponding _annotation table that links entities of that type of entry to the main Annotation below.
# The main annotation table which contains the actual text of the annotation, along with the changelog and the
# identity of the editor who created it.
class Annotation(models.Model):
  id = models.IntergerField(primary_key=True)
  editor = models.ForeignKey('Editor', do_column='editor')
  text = models.TextField(blank=True)
  changelog = models.CharField(max_length=225, blank=True)
  created = models.DateTimeField(blank=True, null=True)
  
  # no DB table creation or deletion operations will be preformed for this model.
  # the name of the database table is db_table.
  class Meta:
      managed = False
      db_table = 'annotation'

