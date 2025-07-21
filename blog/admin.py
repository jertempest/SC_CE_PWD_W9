from django.contrib import admin

# Register your models here.
from . import models

class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'created',
        'updated',
    )
    search_fields = (
        'title',
        'author__username',
        'author__first_name',
        'author__last_name',
    )
    
    prepopulated_fields = {
        'slug' : ('title',)
    }
    
    list_filter = (
        'status',
        'topics',
    )

admin.site.register(models.Post, PostAdmin)

@admin.register(models.Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    prepopulated_fields = {'slug': ('name',)}