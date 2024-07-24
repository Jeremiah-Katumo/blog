from django.contrib import admin

from . import models

# Customize how models are displayed
@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'published_at', 'status'] # 'author'
    list_filter = ['status', 'created_at', 'published_at'] # 'author'
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    # raw_id_fields = ['author']
    date_hierarchy = 'published_at'
    ordering = ['status', 'published_at']

# Register your models here.
# admin.site.register(models.Post, PostAdmin)

@admin.register(models.User)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['username', 'firstname', 'lastname', 'phone', 'joined_date']
    list_filter = ['lastname']
    search_fields = ['username', 'firstname', 'lastname', 'phone']
    ordering = ['lastname']
    date_hierarchy = 'joined_date'


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created_at', 'active']
    list_filter = ['active', 'created_at', 'updated_at']
    search_fields = ['name', 'email', 'body']