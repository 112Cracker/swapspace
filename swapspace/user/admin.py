from django.contrib import admin
from user.models import UserProfile, UserLocation

# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    pass

admin.site.register(UserProfile, UserProfileAdmin)


class UserLocationAdmin(admin.ModelAdmin):
    pass

admin.site.register(UserLocation, UserLocationAdmin)