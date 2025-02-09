
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from channel.models import Channel
from videos.models import Video, Comment
from django.db.models import Count
from django.db.models import Q
from taggit.models import Tag
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Comment, Video
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect


# urls.py

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Comment, Video
from django.contrib.auth.decorators import login_required




# @login_required
# def add_comment(request, video_id):
#     if request.method == "POST":
#         video = get_object_or_404(Video, id=video_id)
#         comment_text = request.POST.get("comment")
#         parent_id = request.POST.get("parent_id", None)
        
#         parent_comment = None
#         if parent_id:
#             parent_comment = get_object_or_404(Comment, id=parent_id)

#         comment = Comment.objects.create(
#             video=video, channel=request.user.channel, comment=comment_text, parent=parent_comment
#         )

#         return JsonResponse({
#             "id": comment.id,
#             "comment": comment.comment,
#             "channel_name": comment.channel.channel_name,
#             "date_added": comment.date_added.strftime("%Y-%m-%d %H:%M"),
#             "parent_id": parent_id,
#         })

#     return JsonResponse({"error": "Invalid request"}, status=400)
@login_required
def add_comment(request, video_id):
    if request.method == "POST":
        video = get_object_or_404(Video, id=video_id)
        comment_text = request.POST.get("comment")
        parent_id = request.POST.get("parent_id", None)
        
        parent_comment = None
        if parent_id:
            parent_comment = get_object_or_404(Comment, id=parent_id)

        # Create the new comment
        comment = Comment.objects.create(
            video=video, channel=request.user.channel, comment=comment_text, parent=parent_comment
        )

        # Fetch all replies if this comment has a parent
        replies = []
        if parent_comment:
            replies = list(parent_comment.children.values(
                "id", "comment", "channel__channel_name", "date_added"
            ).order_by("-date_added"))

        return JsonResponse({
            "id": comment.id,
            "comment": comment.comment,
            "channel_name": comment.channel.channel_name,
            "date_added": comment.date_added.strftime("%Y-%m-%d %H:%M"),
            "parent_id": parent_id,
            "replies": replies,  # Include replies if it's a reply
        })

    return JsonResponse({"error": "Invalid request"}, status=400)


def get_comments(request, video_id):
    """Fetch all comments and replies for a video"""
    video = get_object_or_404(Video, id=video_id)
    comments = Comment.objects.filter(video=video, parent=None).prefetch_related('replies')
    
    comment_data = [
        {
            "id": comment.id,
            "channel_name": comment.channel.channel_name,
            "comment": comment.comment,
            "date_added": comment.date_added.strftime("%Y-%m-%d %H:%M"),
            "replies": [
                {
                    "id": reply.id,
                    "channel_name": reply.channel.channel_name,
                    "comment": reply.comment,
                    "date_added": reply.date_added.strftime("%Y-%m-%d %H:%M"),
                }
                for reply in comment.replies.all()
            ],
        }
        for comment in comments
    ]
    return JsonResponse({"comments": comment_data})


def post_comment(request):
    """Post a new comment or reply"""
    if request.method == "POST":
        video_id = request.POST.get("video_id")
        channel_id = request.POST.get("channel_id")
        comment_text = request.POST.get("comment")
        parent_id = request.POST.get("parent_id", None)

        video = get_object_or_404(Video, id=video_id)
        channel = get_object_or_404(Channel, id=channel_id)
        parent_comment = Comment.objects.filter(id=parent_id).first() if parent_id else None

        new_comment = Comment.objects.create(
            video=video,
            channel=channel,
            comment=comment_text,
            parent=parent_comment
        )

        return JsonResponse({"message": "Comment added", "comment_id": new_comment.id})

    return JsonResponse({"error": "Invalid request"}, status=400)

def index(request):
    video = Video.objects.filter(visibility="public").order_by("-date")
    context = {
        "video":video
    }
    return render(request, "index.html", context)
    

def videoDetail(request, pk):
    video = Video.objects.get(id=pk)
    channel = Channel.objects.get(user=video.user)
    
    channel.total_views = channel.total_views + 1
    channel.save()

    video.views = video.views + 1
    video.save()

    # Suggesting Video
    video_tags_id = video.tags.values_list("id", flat=True)
    similar_videos = Video.objects.filter(tags__in=video_tags_id).exclude(id=video.id)
    similar_videos = similar_videos.annotate(same_tags=Count("tags")).order_by("-same_tags", "-date")[:25]

    # Getting all comment related to a video
    comment = Comment.objects.filter(video=video).order_by("-date_added")

    context = {
        "video":video,
        "channel":channel,
        "comment":comment,
        "similar_videos":similar_videos,
    }
    return render(request, "video-detail.html", context)

def ajax_save_comment(request):
    if request.method == "POST":
        pk = request.POST.get("id")

        comment = request.POST.get("comment")
        video = Video.objects.get(id=pk)
        user = request.user

        new_comment = Comment.objects.create(comment=comment, user=user, video=video)
        new_comment.save()

        response = "Comment Posted"
        return HttpResponse(response)


@csrf_exempt
def ajax_delete_comment(request):
    if request.method == "POST":
        id = request.POST.get("cid")
        comment = Comment.objects.get(id=id)
        comment.delete()
        return JsonResponse({"status":1})
    else:
        return JsonResponse({"status":2})

# Subscribe Functions
def add_new_subscribers(request, id):
    subscribers = Channel.objects.get(id=(id))
    user = request.user

    # if Destiny > [Desphixs Subscribers]
    if user in subscribers.subscribers.all():
        subscribers.subscribers.remove(user)
        response = "Subscribe"
        return JsonResponse(response, safe=False, status=200)
    else:
        subscribers.subscribers.add(user)
        response = "Unsubscribe"
        return JsonResponse(response, safe=False, status=200)

# Load channel subs
def load_channel_subs(request, id):
    subscribers = Channel.objects.get(id=id)
    sub_lists = list(subscribers.subscribers.values())
    return JsonResponse(sub_lists, safe=False, status=200)

def add_new_like(request, id):
    video = Video.objects.get(id=id)
    user = request.user

    # if Destiny > [Desphixs Subscribers]
    if user in video.likes.all():
        video.likes.remove(user)
        like_response = '<i class="fa fa-thumbs-up"></i>'
        return JsonResponse(like_response, safe=False, status=200)
    else:
        video.likes.add(user)
        like_response = '<i class="fa fa-thumbs-up"></i>'
        return JsonResponse(like_response, safe=False, status=200)
    



def load_video_likes(request, id):
    video = Video.objects.get(id=id)
    likes_lists = list(video.likes.values())
    return JsonResponse(likes_lists, safe=False, status=200)


def searchView(request):
    video = Video.objects.filter(visibility="public").order_by("-date")
    query = request.GET.get("q")
    if query:
        video = video.filter(
            Q(title__icontains=query)|
            Q(description__icontains=query)
        ).distinct()
    
    context = {
        "video":video,
        "query":query,

    }
    return render(request, "search.html", context)

    
def tag_list(request, tag_slug=None):
    video = Video.objects.filter(visibility="public").order_by("-date")

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        video = video.filter(tags__in=[tag])

    context = {
    "video":video,
    "tag":tag,

    }
    return render(request, "tags.html", context)


def trending(request):
    video = Video.objects.filter(visibility="public").order_by("-views")
    context = {
        "video":video
    }
    return render(request, "trending.html", context)
    

def savedVideos(request):
    try:
        video = request.user.profile.saved_videos.all()
    except:
        video = None
    context = {
        "video":video
    }
    return render(request, "saved-video.html", context)
    






















# def homepage(request):
#     return render(request, "test_temp/index.html")

# def aboutpage(request):
#     return render(request, "test_temp/about.html")
    
# def contactpage(request):
#     return render(request, "test_temp/contact.html")


@login_required
def add_comment(request, video_id):
    """Handles adding a new comment."""
    if request.method == "POST":
        video = get_object_or_404(Video, id=video_id)
        comment_text = request.POST.get("comment")

        if comment_text:
            comment = Comment.objects.create(
                video=video,
                channel=request.user.channel,  # Assuming a user has a related Channel
                comment=comment_text
            )
            return JsonResponse({"message": "Comment added!", "comment_id": comment.id}, status=201)

    return JsonResponse({"error": "Invalid request"}, status=400)

@login_required
def add_reply(request, comment_id):
    """Handles adding a reply to an existing comment."""
    if request.method == "POST":
        parent_comment = get_object_or_404(Comment, id=comment_id)
        reply_text = request.POST.get("comment")

        if reply_text:
            reply = Comment.objects.create(
                video=parent_comment.video,
                channel=request.user.channel,  # Assuming a user has a related Channel
                comment=reply_text,
                parent=parent_comment  # Setting parent to make it a reply
            )
            return JsonResponse({"message": "Reply added!", "reply_id": reply.id}, status=201)

    return JsonResponse({"error": "Invalid request"}, status=400)

    