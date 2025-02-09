from django.contrib import admin
from django.contrib import admin
from .models import Comment
# Register your models here.
from videos.models import Video, Comment
from import_export.admin import ImportExportModelAdmin

class VideoAdmin(ImportExportModelAdmin):
    pass

class CommentAdmin(admin.ModelAdmin):
    list_display = ('channel', 'comment', 'date_added', 'is_parent')  # 'user' & 'active' removed
    search_fields = ('channel__channel_name', 'comment')  # Searchable fields

admin.site.register(Comment, CommentAdmin)

admin.site.register(Video, VideoAdmin)




