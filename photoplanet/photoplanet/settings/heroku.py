import os

import dj_database_url

from base import *

#DEBUG = False
# https://devcenter.heroku.com/articles/django#django-settings

# Parse database configuration from $DATABASE_URL
DATABASES['default'] = dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# To set environment variables see config_heroku_sample.sh in project's root

INSTAGRAM_CLIENT_ID = os.environ['INSTAGRAM_CLIENT_ID']
INSTAGRAM_CLIENT_SECRET = os.environ['INSTAGRAM_CLIENT_SECRET']

GOOGLE_OAUTH2_CLIENT_ID = os.environ['GOOGLE_OAUTH2_CLIENT_ID']
GOOGLE_OAUTH2_CLIENT_SECRET = os.environ['GOOGLE_OAUTH2_CLIENT_SECRET']

TWITTER_CONSUMER_KEY = os.environ['TWITTER_CLIENT_ID']
TWITTER_CONSUMER_SECRET = os.environ['TWITTER_CLIENT_SECRET']

GITHUB_API_ID=os.environ['GITHUB_API_ID']
GITHUB_API_SECRET=os.environ['GITHUB_API_ID']
