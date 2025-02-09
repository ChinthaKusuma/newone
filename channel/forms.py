from django import forms
from channel.models import Community
from videos.models import Video

from django import forms
from .models import Channel  # Import your Channel model

class ChannelForm(forms.ModelForm):
    channel_name = forms.CharField(widget=forms.TextInput(attrs={'id': "channel_name", 'onkeyup': "validateChannelName()"}))
    full_name = forms.CharField(widget=forms.TextInput(attrs={'id': "full_name"}))
    description = forms.CharField(widget=forms.Textarea(attrs={'id': "description", 'onkeyup': "validateDescription()"}), required=False)
    channel_art = forms.ImageField(widget=forms.FileInput(attrs={'class': "file"}), required=False)
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': "file"}), required=False)
    
    class Meta:
        model = Channel
        fields = [
            "channel_art", "image", "full_name", "channel_name",
            "description", 
        ]



class VideoForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'id':"title", 'onkeyup':"titleValidate()"}))
    description = forms.CharField(widget=forms.Textarea(attrs={'id':"description", 'onkeyup':"desc_validate()"}))
    image = forms.ImageField(widget=forms.FileInput(attrs={'class':"file"}))
    video = forms.FileField(widget=forms.FileInput(attrs={'class':"file"}))

    class Meta:
        model = Video
        fields = ['video', 'image', 'title', 'description', 'tags', 'visibility']


class CommunityForm(forms.ModelForm):

    class Meta:
        model = Community
        fields = ['content', 'image']