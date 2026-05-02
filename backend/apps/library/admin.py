from django.contrib import admin
admin.site.register(__import__('apps.library.models', fromlist=['*']).__dict__[list(filter(lambda x: x[0].isupper() and not x.startswith('_'), __import__(f'apps.library.models', fromlist=['*']).__dict__.keys()))[0]])
