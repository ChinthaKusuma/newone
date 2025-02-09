from django.urls import path
from videos import views
from .views import add_comment

app_name="videos"


urlpatterns = [
    
    path("", views.index, name="index"),
    path("trending/", views.trending, name="trending"),
    path("saved-videos/", views.savedVideos, name="saved-videos"),


    path("watch/<int:pk>/", views.videoDetail, name="video-detail"),

    # Saving Comment to db
    

    # Subscribe Function
    # path("add-sub/<int:id>/", views.add_new_subscribers, name="add_new_subscribers"),
    # path("sub-load/<int:id>/", views.load_channel_subs, name="load_channel_subs"),

    # Like Function
    path("add-like/<int:id>/", views.add_new_like, name="add_new_like"),
    
    path("likes-load/<int:id>/", views.load_video_likes, name="load_video_likes"),

    # Saving Video TO Profile
    
    # path("video/search/", views.searchView, name="search"),

     # Tag URL
    path("tags/video/<slug:tag_slug>", views.tag_list, name="tags"),
    
    path('comment/add/<int:video_id>/', views.add_comment, name='add_comment'),
    path('comment/reply/<int:comment_id>/', views.add_reply, name='add_reply'),
    path("subscribe/<int:channel_id>/", views.subscribe_channel, name="subscribe-channel"),

   
]






# urlpatterns = [
    # path("", views.homepage, name="home"),
    # path("about/", views.aboutpage, name="daosjdasjdijaspodjoaspjdoasdjajsodjaosjd"),
    # path("contact/", views.contactpage, name="contact"),
    
# ]