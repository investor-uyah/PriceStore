from django.contrib import admin
from .models import Members, Price, BlogPost

# Register your models here.

@admin.register(Members)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('shopname', 'ownersname', 'phone', 'joined_date', 'bio')


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ('foodstuff', 'price', 'description', 'author', 'market_store_name', 'state', 'lga')


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at", "updated_at")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "content")
    list_filter = ("created_at",)