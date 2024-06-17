from django.contrib import admin

from applications.feedback.models import *

# Register your models here.
admin.register(Comment)
admin.register(Like)
admin.register(Favourite)
admin.site.register(Rating)


