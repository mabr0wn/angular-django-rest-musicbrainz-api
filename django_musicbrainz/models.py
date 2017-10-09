from __future__ unicdoe_literals
# can use python 2 with python 3 unicode operators such as ''u you do not have to write the u() function.

from django.db import models # import the models functions to add to our models below.

import musicbrainzngs as mb # import the full mb DB from ngs

CHARACTER_VARYING_MAX_LENGTH = 10000 # Defining the max characters we can have in our strings, max is 1 GB.

# make new a model called Album to represent the artist's Album
class Album(models.Model):
  name = models.CharField(max_length=255)
  artist = models.CharField(max_length=255)
  slug = models.SlugField() #instead of having /1 we will see /album
  
  class Meta:
    ordering = ['name']
    
  def __str__(self):
    return self.name
  
  # will sort later.
  
class Artist(models.Model):
  id = models.IntegerField(primary_key=True)
  gid = models.IntegerField()
  track = models.ForeignKey('Track') # may implement blank, null
  name = models.CharField(max_length=255, blank=True, null=True)
  instrument = models.CharField(max_length=255, blank=True, null=True)
  start_time = models.CharField(max_length=20, blank=True, null=True)
  end_time = models.CharField(max_length=20, blank=True, null=True)
  begin_date_year = models.SmallIntegerField(blank=True, null=True)
  begin_date_month = models.SmallIntegerField(blank=True, null=True)
  begin_date_day = models.SmallIntegerField(blank=True, null=True)
  end_date_year = models.SmallIntegerField(blank=True, null=True)
  end_date_month = models.SmallIntegerField(blank=True, null=True)
  end_date_day = models.SmallIntegerField(blank=True, null=True)
  ended = models.DateTimeField(blank=True, null=True)
  type = models.ForeignKey(Type, db_column='type', blank=True, null=True)
  gender = models.ForeignKey('Gender', blank=True, null=True)
  area = models.ForeignKey(Area, blank=True, null=True)
  begin_area = models.CharField(max_length=255, blank=True, null=True)
  ended_area = models.CharField(max_length=255, blank=True, null=True)
  comment = models.TextField(blank=True, null=True)
  edits_pending = models.IntegerField(blank=true, null=True)
  last_update = models.DateTimeField(blank=True, null=True)
  slug = models.SlugField()
  
  class Meta:
    managed = True
    db_table = 'artist'
    ordering = ['track', 'start-time'] # order by track start time.
    
  def get_absolute_url(self): # add the reverse lookup for the url will add to the urls.py soon.
    return reverse('artist_detail_view', kwargs={'album': self.track.album.slug, 'track': self.track.slug,
                                                 'artist': self.slug})
  

# they are text fields acting as Minature wikis.
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
 
# alternate names or mispellings.
class AreaAlias(models.Model):
    id = models.IntegerField(primary_key=True)
    area = models.ForeignKey(Area, db_column='area')
    name = models.CharField(max_length=CHARACTER_VARYING_MAX_LENGTH)
    locale = models.TextField(blank=True)
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(blank=True, null=True)
    # for type possible values are Country, Subdivision, Country, Municipality, City, District, Island
    type = models.ForeignKey(
          'AreaAliasType', db_column='type', blank=True, null=True)
    sort_name = models.CharField(max_length=CHARACTER_VARYING_MAX_LENGTH)
    begin_date_year = models.SmallIntegerField(blank=True, null=True)
    begin_date_month = models.SmallIntegerField(blank=True, null=True)
    begin_date_day = models.SmallIntegerField(blank=True, null=True)
    end_date_year = models.SmallIntegerField(blank=True, null=True)
    end_date_month = models.SmallIntegerField(blank=True, null=True)
    end_date_day = models.SmallIntegerField(blank=True, null=True)
    primary_for_locale = models.BooleanField()
    ended = models.BooleanField()
    
    class Meta:
      managed = False
      db_table = 'area_alias'
# defining the possible values for ForeignKey 'type'
class AreaAliasType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    parent = models.ForeignKey(
        'self', db_column='parent', blank=True, null=True)
    child_order = models.IntegerField()
    description = models.TextField(blank=True)
    
    class Meta:
        managed = False
        db_table = 'area_alias_type'
# describing the middle table between annotation and Area.  which allows them to communicate to each other.        
class AreaAnnotation(models.Model):
  area = models.ForeignKey(Area, db_column='area', primary_key=True)
  annotation = models.ForeignKey(Annotation, db_column='annotation')
  
  # unique together allows a set of fields names to be take togther, but they must be unique.
  class Meta:
    managed = False
    db_tabel = 'area_annotation'
    unique_together = ('area', 'annotation')

class AreaGidRedirect(models.Model):
  gid = models.TextField(primary_key=True)
  new = models.ForeignKey(Area)
  created = models.DateTimeField(blank=True, null=True)
  
  class Meta:
    managed = False
    db_table = 'area_gid_redirect'
  
    
class AreaType(models.Model):
    id = models.IntegerField()
    name = models.TextField()
    parent = models.ForeignKey(
         'self', db_column='parent', blank=True, null=True)
    child_order = models.IntegerField()
    description = models.TextField(blank=True)
    
    class Meta:
      managed = False
      db_table = 'area_type'
      

      
# Alias to Artist, would define a nickname or mispelling of some sort.      
class ArtistAlias(models.Model):
    id = models.IntegerField(primary_key=True)
    artist = models.ForeignKey(Artist, db_column=True, blank=True, null=True)
    sort_name = models.CharField(max_length=255, blank=True, null=True)
    locale = models.TextField()
    edits_pending = IntegerField(blank=True, null=True) # how many edits are pending for artist alias
    last_updated = DateTimeField()
    type = models.ForeignKey(
           'ArtistAliasType', db_column='type', blank=true, null=True)
    begin_date_year = models.SmallIntegerField(blank=True, null=True)
    begin_date_month = models.SmallIntegerField(blank=True, null=True)
    begin_date_day = models.SmallIntegerField(blank=True, null=True)
    ended_date_year = models.SmallIntegerField(blank=True, null=True)
    ended_date_month = models.SmallIntegerField(blank=True, null=True)
    ended_date_day = models.SmallIntegerField(blank=True, null=True)
    ended = models.DateTimeField(blank=True, null=True)
    primary_for_locale = models.BooleanField()
    
    class Meta:
      managed = False
      db_table = 'artistalias'
    
# This is the Alias type for Artist basically we will need to use this to define the type of artist.
class ArtistAliasType(models.Model):
    id = models.IntegerField()
    name = models.TextField()
    parent = models.ForeignKey(
              'self', db_columm='parent', blank=True, null=True)
    child_order = models.IntegerField()
    description = models.TextField(blank=True)
    
    class Meta:
      managed = False
      db_table = 'artist_alias_type'

class ArtistAnnonation(models.Model):
  artist = models.ForeignKey(Artist, db_column='artist', primary_key=True)
  annotation = models.ForeignKey(Annotation, db_column='annotation')
  
  class Meta:
    managed = False
    db_table = 'artist_annotation'
    unique_together = ('artist', 'annotation')

class ArtistCredit(models.Model):
  id = models.IntegerField(primary_key=True)
  name = models.Charfield(max_length=CHARACTER_VARYING_MAX_LENGTH)
  artist_count = models.smallIntegerField()
  ref_count = models.IntegerField(blank=True, null=True)
  created = models.DateTimeField(blank=True, null=True)
  
  artists = model.ManyToManyField(
      'Artist', through='ArtistCreditName')
  
  class Meta:
    managed = False
    db_table = 'artist_credit'

class ArtistCreditName(models.model):
  artist_credit = models.ForeignKey(
      ArtistCredit, db_column='artist_credit', primary_key=True)
  position = models.SmallIntegerField()
  artist = models.ForeignKey(Artist, db_column='artist')
  name = models.CharField(max_length=CHARACTER_VARYING_MAX_LENGTH)
  join_phase = models.TextField()
  
  class Meta:
    managed = False
    db_table = 'aritst_credit_name'
    unique_together = ('artist_credit', 'position') # position the artist will be in

class ArtistDeletion(models.Model):
    gid = models.TextField(primary_key=True)
    last_known_name = models.CharField(max_length=CHARACTER_VARYING_MAX_LENGTH)
    last_known_comment = models.TextField()
    deleted_at = models.DateTimeField()
    
    class Meta:
      managed = False
      db_table = 'artist_deletion'

class ArtistGidRedirect(models.Model):
  gid = models.TextField(primary_key=True)
  new = models.ForeignKey(Artist)
  created = models.DateTimeField(blank=True, null=True)
  
  class Meta:
    managed = False
    db_table = 'artist_gid_redirect'
    
"""
The Interested Parties Information Code (IPI) is an identifying number assigned in 
the CISAC database to each Interested Party in musical rights management.
"""

class ArtistIpi(models.Model):
  artist = models.ForeignKey(
      Artist, db_column='artist', primary_key=True)
  ipi = models.CharField(max_length=11)
  edits_pending = models.IntegerField()
  created = models.DateTimeField(blank=True, null=True)
  
  class Meta:
    managed = False
    db_table = 'artist_ipi'
    unique_together = ('artist', 'ipi')
    
# Identifies an Artist
class ArtistIsni(models.Model):
  artist = models.ForeignKey(
      Artist, db_column='artist', primary_key=True)
  isni = models.CharField(max_length=16)
  edits_pending = models.IntegerField()
  create = models.DateTimeField(blank=True, null=True)
  
  class Meta:
    managed = False
    db_table = 'artist_isni'
    unique_together = ('artist', 'isni')

# Meta data for the artist
class ArtistMeta(models.Model):
  id = models.ForeignKey(Artist, db_column='id', primary_key=True)
  rating = models.SmallIntegerField(blank=True, null=True)
  rating_count = models.IntegerField(blank=True, null=True)
  
  class Meta:
    managed = False
    db_table = 'artist_meta'

# allows to rate an artist    
class ArtistRatingRaw(models.Model):
  artist = models.ForeignKey(Artist, db_column='artist', primary_key=True)
  editor = models.ForeignKey('Editor', db_column='editor')
  rating = models.SmallIntegerField()
  
  class Meta:
    managed = False
    db_table = 'artist_rating_raw'
    unique_together = ('artist', 'editor')
 
# Tag a artist such as a comment
class ArtistTag(models.Model):
  artist = models.ForeignKey(Artist, db_column='artist', primary_key=True)
  tag = models.ForeignKey('Tag', db_column='tag')
  count = models.IntegerField()
  last_updated = models.DateTimeField(blank=True, null=True)
  
  class Meta:
    managed = False
    db_table = 'artist_tag'
    unique_together = ('artist', 'tag')
    
class ArtistTagRaw(models.Model):
  artist = models.ForeignKey(Artist, db_column='artist', primary_key=True)
  editor = models.ForeignKey('Editor', db_column='editor')
  tag = models.ForeignKey('Tag', db_column='tag')
  
  class Meta:
    managed = False
    db_table = 'artist_tag_raw'
    unique_together = 'artist', 'editor', 'tag'

class ArtistType(models.Model):
  id = models.IntegerField(primary_key=True)
  name = models.CharField(max_length=255)
  parent = models.ForeignKey(
    'self', db_column='parent', blank=True, null=True)
  child_order = models.IntegerField()
  description = models.Textfield(blank=True)
  
  class Meta:
    managed = False
    db_table = 'artist_type'

    
class AutoeditorElection(models.Model):
  id = models.IntegerField(primary_key=True)
  # who the honor is
  candidtate = models.ForeignKey(
    'Editor', db_column='canditate',
    related_name='candiate_autoeditorelection_set')
  proposer = models.ForeignKey(
    'Editor', db_column='proposer',
    related_name='proposer_autoeditorelection_set')
  seconder_1 = models.ForeignKey(
    'Editor', db_column='seconder_1',
    related_name='seconder_1_autoeditorelection_set',
    blank=True, null=True)
  seconder_2 = models.ForeignKey(
    'Editor', db_column='seconder_2',
    related_column='seconder_2_autoeditorelection_set',
    blank=True, null=True)
  status = models.IntegerField()
  yes_votes = models.IntgerField()
  no_votes = models.IntegerField()
  proposed_time = models.DateTimeField()
  open_time = models.DateTimeField(blank=True, null=True)
  close_time = models.DateTimeField(blank=True, null=True)
  
  class Meta:
    managed = False
    db_table = 'autoeditor_election'

class AutoeditorElectionVote(models.Model):
  id = models.IntegerField(primary_key=True)
  autoeditor_election = models.ForeignKey(
      AutoeditorElection, db _column='autoeditor_election')
  voter = models.ForeignKey('Editor', db_column='voter')
  vote = models.IntegerField()
  vote_time = models.DateTimeField()
  
  class Meta:
    managed = False
    db_table = 'autoeditor_election_vote'
 
# Cd table of contents
class Cdtoc(models.Model):
  id = models.IntegerField(primary_key=True)
  discid = models.CharField(unique=True, max_length=28)
  # another DB with music meta data
  freedb_id = models.CharField(max_length=8)
  track_count = models.IntegerField()
  track_offset = models.BooleanField()
  degraded = models.BooleanField()
  created = models.DateTimeField(blank=True, null=True)
  
  class Meta:
    managed = False
    db_table = 'cdtoc'
 
class CdtocRaw(models.Model):
  id = models.InteferField(primary_key=True)
  release = models.ForeignKey('ReleaseRaw', db_column='release')
  # discid is a small Program, written in C++
  discid = models.CharField(max_length=28)
  track_count = models.integerField()
  # this follows the data area on the CD.
  leadout_offset = models.IntegerField()
  # this must follow the data area after each track.
  track_offset = models.TextField()
  degraded = models.BooleanField()
  created = models.DateTimeField(blank=True, null=True)
  
  class Meta:
    managed = False
    db_table = 'cdtoc'

class CountryArea(models.Model):
  area = models.ForeignKey(Area, db_column='area', primary_key=True)
  
  class Meta:
    manged = False
    db_table = 'country_area'

class Edit(models.Model):
  id = models.IntegerField(primary_key=True)
  editor = models.ForeignKey('Editor', db_column='editor')
  type = models.SmallIntegerField()
  # to modify what you need to edit.
  data = models.TextField()
  yes_votes = models.IntegerField()
  no_votes = models.IntegerField()
  autoedit = models.SmallIntegerField()
  open_time = models.DateTimeField(blank=True, null=True)
  close_time = models.DateTimeField(blank=True, null=True)
  expired_time = models.DateTimeField()
  language = models.ForeignKey(
      'Language', db_column='language', blank=True, null=True)
  quality = models.SmallIntegerField()
  
  class Meta:
    managed = False
    db_table = 'Edit'
    
class EditArea(models.Model):
  edit = models.ForeignKey(Edit, db_column='edit', primary_key=True)
  area = models.ForeignKey(Area, db_column='area')
  
  class Meta:
    managed = False
    db_table = 'edit_area'
    unique_together = ('edit', 'area')
   
class EditArtist(models.Model):
  edit = models.ForeignKey(Edit, db_column='edit', primary_key=True)
  artist = models.ForeignKey(Artist, db_column='artist')
  status = models.SmallIntegerField()
  
  class Meta:
    managed = False
    db_table = 'edit_artist'
    unique_together = ('edit', 'artist')
    
class EditInstrument(models.Model):
  edit = models.ForeignKey(Edit, db_column='edit', primary_key=True)
  instrument = models.ForeignKey('Instrument', db_colunmn='instrument')
  
  class Meta:
    managed = False
    db_table = 'edit_instrument'
    unique_together = ('edit', 'instrument')

class EditLabel(models.Model):
  edit = models.ForeignKey(Edit, db_column='edit', primary_key=True)
  label = models.ForeignKey('Label', db_column='label')
  status = models.SmallIntegerField()
  
  class Meta:
    managed = False
    db_table = 'edit_label'
    unique_together = ('edit', 'label')
    
class EditNote(models.Model):
  id = models.IntegerField(primary_key=True)
  editor = models.ForeignKey('Editor', db_column='editor')
  edit = models.ForeignKey(Edit, db_column='edit')
  text = models.TextField()
  post_time = models.DateTimeField(blank=True, null=True)
  
  class Meta:
    managed = False
    db_table = 'edit_note'
 
class EditPlace(models.Model):
  edit = models.ForeignKey(Edit, db_column='edit', primary_key=True)
  place = models.ForeignKey('Place', db_column='place')
  
  class Meta:
    managed = False
    db_table = 'edit_place'
    unique_together = ('edit', 'place')

class EditRecording(models.Model):
  edit = models.ForeignKey(Edit, db_column='edit', primary_key=True)
  recording = models.ForeignKey('Recording', db_column='recording')
  
  class Meta:
    managed = False
    db_table = 'edit_release'
    unique_together = ('edit', 'recording')
    
class EditRelease(models.Model):
  edit = models.ForeignKey(Edit, db_column='edit', primary_key=True)
  release = models.ForeignKey('Release', db_column='release')
  
  class Meta:
    managed = False
    db_table = 'edit_release'
    unique_together = ('edit', 'release')

class EditReleaseGroup(models.Model):
    edit = models.ForeignKey(Edit, db_column='edit', primary_key=True)
    release_group = models.ForeignKey(
        'ReleaseGroup', db_column='release_group')

    class Meta:
        managed = False
        db_table = 'edit_release_group'
        unique_together = ('edit', 'release_group')    
  
class EditSeries(models.Model):
    edit = models.ForeignKey(Edit, db_column='edit', primary_key=True)
    series = models.ForeignKey('Series', db_column='series')

    class Meta:
        managed = False
        db_table = 'edit_series'
        unique_together = ('edit', 'series')

class EditUrl(models.Model):
    edit = models.ForeignKey(Edit, db_column='edit', primary_key=True)
    url = models.ForeignKey('Url', db_column='url')

    class Meta:
        managed = False
        db_table = 'edit_url'
        unique_together = ('edit', 'url')        
  
class EditWork(models.Model):
    edit = models.ForeignKey(Edit, db_column='edit', primary_key=True)
    work = models.ForeignKey('Work', db_column='work')

    class Meta:
        managed = False
        db_table = 'edit_work'
        unique_together = ('edit', 'work')
class Editor(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=64)
    privs = models.IntegerField(blank=True, null=True)
    email = models.CharField(max_length=64, blank=True)
    website = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)
    member_since = models.DateTimeField(blank=True, null=True)
    email_confirm_date = models.DateTimeField(blank=True, null=True)
    last_login_date = models.DateTimeField(blank=True, null=True)
    edits_accepted = models.IntegerField(blank=True, null=True)
    edits_rejected = models.IntegerField(blank=True, null=True)
    auto_edits_accepted = models.IntegerField(blank=True, null=True)
    edits_failed = models.IntegerField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    gender = models.ForeignKey(
        'Gender', db_column='gender', blank=True, null=True)
    area = models.ForeignKey(Area, db_column='area', blank=True, null=True)
    password = models.CharField(max_length=128)
    ha1 = models.CharField(max_length=32)
    deleted = models.BooleanField()

    artists_subscribed = models.ManyToManyField(
        'Artist', through='EditorSubscribeArtist')
    artists_watched = models.ManyToManyField(
        'Artist', through='EditorWatchArtist')
    artists_deleted = models.ManyToManyField(
        'ArtistDeletion', through='EditorSubscribeArtistDeleted')
    labels_deleted = models.ManyToManyField(
        'LabelDeletion', through='EditorSubscribeLabelDeleted')
    languages = models.ManyToManyField('Language', through='EditorLanguage')
    release_group_types_watched = models.ManyToManyField(
        'ReleaseGroupPrimaryType', through='EditorWatchReleaseGroupType')
    release_status_watched = models.ManyToManyField(
        'ReleaseStatus', through='EditorWatchReleaseStatus')
    series_deleted = models.ManyToManyField(
        'SeriesDeletion', through='EditorSubscribeSeriesDeleted')

    class Meta:
        managed = False
        db_table = 'editor'
class EditorCollection(models.Model):
    id = models.IntegerField(primary_key=True)
    gid = models.TextField(unique=True)
    editor = models.ForeignKey(Editor, db_column='editor')
    name = models.CharField(max_length=CHARACTER_VARYING_MAX_LENGTH)
    public = models.BooleanField()
    description = models.TextField()

    releases = models.ManyToManyField(
        'Release', through='EditorCollectionRelease')

    class Meta:
        managed = False
        db_table = 'editor_collection'

class EditorCollectionRelease(models.Model):
    collection = models.ForeignKey(
        EditorCollection, db_column='collection', primary_key=True)
    release = models.ForeignKey('Release', db_column='release')

    class Meta:
        managed = False
        db_table = 'editor_collection_release'
        unique_together = ('collection', 'release')       
class EditorLanguage(models.Model):
    editor = models.ForeignKey(Editor, db_column='editor', primary_key=True)
    language = models.ForeignKey('Language', db_column='language')
    fluency = models.TextField()

    class Meta:
        managed = False
        db_table = 'editor_language'
        unique_together = ('editor', 'language')
