from django.urls import path
from . import views

app_name ='blog'

urlpatterns = [
    path('', views.post_list, name="Post"),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_details , name = "Post_Details"),
    path('<int:post_id>/share', views.post_share , name = "Share"),
    path('tag/<slug:tag_slug>', views.post_list , name = "Tag_Post_List"),
    
]

