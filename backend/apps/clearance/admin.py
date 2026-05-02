from django.contrib import admin
admin.site.register(__import__('apps.clearance.models', fromlist=['*']).__dict__[list(filter(lambda x: x[0].isupper() and not x.startswith('_'), dir()))[0]])
