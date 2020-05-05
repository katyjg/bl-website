# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_()v3e49-sg5vt(#x7lnftjp^rs5t#5^or$8#o)h0obi*3@i@y'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*'] 

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'website',
        'USER': 'website',
        'PASSWORD': 'Zoeshah6fiuzeeCeed5ahGau',
        'HOST': '172.17.0.1',
        'PORT': '',
    }
}
