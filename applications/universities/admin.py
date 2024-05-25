from django.contrib import admin
from applications.universities.models import University, Faculty


class UniversityAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']
    

admin.site.register(University, UniversityAdmin)
admin.site.register(Faculty)
