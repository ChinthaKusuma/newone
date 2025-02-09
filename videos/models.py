# Django Imports
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model  # Avoids circular import
from taggit.managers import TaggableManager

# Constants
VISIBILITY = (
    ("private", "Private"),
    ("unlisted", "Unlisted"),
    ("members_only", "Members Only"),
    ("public", "Public")
)

# Function to define file upload path
def user_directory_path(instance, filename):
    return "user_{0}/{1}".format(instance.user.id, filename)

# Models
class Video(models.Model):
    video = models.FileField(upload_to=user_directory_path)
    image = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    tags = TaggableManager()
    date = models.DateTimeField(auto_now_add=True)
    visibility = models.CharField(choices=VISIBILITY, max_length=100, default="public")
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)  # Use get_user_model()
    views = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(get_user_model(), related_name="likes")
    featured = models.BooleanField(default=False)  # Featured Field

    def __str__(self):
        return self.title

class Comment(models.Model):
    video = models.ForeignKey(
        Video, related_name='comments', null=True, on_delete=models.CASCADE)
    channel = models.ForeignKey(
        'channel.Channel',  # Use string reference to prevent circular import
        verbose_name='Channel',
        related_name='comments',
        null=True,
        on_delete=models.CASCADE
        
    )
    comment = models.TextField(max_length=300)
    date_added = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, blank=True, null=True, related_name='replies')

    def __str__(self):
        return f"{self.channel.channel_name}: {self.comment[:50]}" 

    @property
    def children(self):
        return Comment.objects.filter(parent=self).order_by('-date_added').all()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False
