import os
import sys
import django
from django.conf import settings
#from django.core.management import execute_from_command_line
from django.http import HttpResponse
from django.urls import path
from django.db import models



fname = os.path.splitext(os.path.basename(__file__))[0]
urlpatterns = [path(r'', lambda r: HttpResponse('Hello, world!'))]


settings.configure(
	SECRET_KEY = 'ty&9(v*hengug!*7$6=7l5!xv_v-i5&%1g*4m&9uy-a5-wcody',
	DEBUG = True,
	INSTALLED_APPS = ['django.contrib.sites'],
	MIDDLEWARE_CLASSES = ('django.middleware.common.CommonMiddleware',
						'django.middleware.csrf.CsrfViewMiddleware',
						'django.middleware.clickjacking.XFrameOptionsMiddleware'),
	ROOT_URLCONF=__name__,
	DATABASES = {
		'default': {
			'ENGINE': 'django.db.backends.mysql',
			'NAME': 'stocksvision',
			'USER': 'crawler',
			'PASSWORD': 'pass',
			'HOST': 'db',
			'PORT': '3306'
		}
	},
	PRODUCT_MODEL = 'database.Example',
	SITE_ID = 1
)

django.setup()

from database import Example


if __name__ == "__main__":
	#settings.configure(DEBUG=True, MIDDLEWARE_CLASSES=[], ROOT_URLCONF=fname)

	#django.setup()
	from django.core.management import execute_from_command_line
	execute_from_command_line(sys.argv)