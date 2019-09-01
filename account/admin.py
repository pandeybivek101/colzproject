from django.contrib import admin
from .models import *
# Register your models here.

class UserHistoryAdmin(admin.ModelAdmin):
	list_display = ['user', 'duration', 'destination_type', 'accomodation_type']
admin.site.register(UserHistory, UserHistoryAdmin)
