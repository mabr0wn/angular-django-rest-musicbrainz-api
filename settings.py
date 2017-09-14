DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends,sqlite3'
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
  
    'musicbrainz': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2' # sudo pip install psycopg2
    'NAME': 'musicbrainz_db',
    'USER': 'musicbrainz',
    'PASSWORD': '',
            'HOST': '127.0.0.1',
    'PORT': '5432',
    }
}

DATABASE_ROUTERS = ['django_musicbrainz.router.MusicbrainzRouter',]
