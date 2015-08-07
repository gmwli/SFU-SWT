"""
Django settings for swt project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '&rg$=_ux_ire6qp2+%vzin028kif#p6hq!ube4eirfj$!y$#da'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []
#added this to allow t
TEMPLATE_DIRS= (
	'/home/phoenix470/swt/templates/',
)
#dajax related

DAJAXICE_MEDIA_PREFIX='/swt/dajaxice'
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'auth',
    'profiles',
    'workouts', 
    'chartit',
    'bookings',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #CAS related
    'django_cas.middleware.CASMiddleware',
    'django.middleware.doc.XViewMiddleware',
)
#CAS relate
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'django_cas.backends.CASBackend',
)
#CAS related
#CAS_SERVER_URL='http://lefty.cmpt.sfu.ca/fake-cas/'
CAS_SERVER_URL='https://cas.sfu.ca/cgi-bin/WebObjects/cas.woa/wa/'
#CAS_REDIRECT_URL='https://connect.sfu.ca/'
CAS_REDIRECT_URL='/swt/home/'
CAS_LOGOUT_COMPLETELY='True'
#CAS_IGNORE_REFERER='True'
#This should timeout session after browser closes
SESSION_EXPIRE_AT_BROWSER_CLOSE='True'


ROOT_URLCONF = 'swt.urls'

#Handling user-uploaded media
MEDIA_ROOT = '/home/phoenix470/swt/media/static/assets/uploaded_files'
MEDIA_URL = '/media/'

WSGI_APPLICATION = 'swt.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'swt_db',
	'USER': 'admin',
	'PASSWORD': 'secretpassword',
	'HOST': '',
	'PORT': '',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Canada/Pacific'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_ROOT = '/home/phoenix470/swt/media/static/'
STATIC_URL = '/static/'
STATICFILES_DIRS = (
	('assets', '/home/phoenix470/swt/static'),
)

# Enable collectstatic to check for updated files, not just new
AWS_PRELOAD_METADATA = True

TEMPLATE_CONTEXT_PROCESSORS = ("django.contrib.auth.context_processors.auth",
"django.core.context_processors.debug",
"django.core.context_processors.i18n",
"django.core.context_processors.media",
"django.core.context_processors.static",
"django.core.context_processors.request",
"django.contrib.messages.context_processors.messages",)


STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
    'dajaxice.finders.DajaxiceFinder',
)
