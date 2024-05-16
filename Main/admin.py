from django.contrib import admin
from .models import Memebers

# Register your models here.

class MemberAdmin(admin.ModelAdmin):
    list_display = ('shopname', 'ownersname', 'phone', 'joined_date', 'bio')


admin.site.register(Memebers, MemberAdmin)