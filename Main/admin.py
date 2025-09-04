from django.contrib import admin
from .models import Members, Price

# Register your models here.

class MemberAdmin(admin.ModelAdmin):
    list_display = ('shopname', 'ownersname', 'phone', 'joined_date', 'bio')
    
class PriceAdmin(admin.ModelAdmin):
    list_display = ('foodstuff', 'price', 'description', 'author', 'market_store_name', 'state', 'lga')

admin.site.register(Members, MemberAdmin)
admin.site.register(Price, PriceAdmin)