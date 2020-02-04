from django.urls import path, include
from . import views
from . import viewsets
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', viewsets.UserViewSet)
router.register(r'subreddits', viewsets.SubRedditViewSet)
router.register(r'posts', viewsets.PostViewSet)
router.register(r'comments', viewsets.CommentViewSet)

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    ### From the last assignment
    path('', views.post_list, name='post_list'),
    path('post/<uuid:pk>/', views.post_detail, name='post_detail'),
    path('sub/<uuid:pk>/', views.sub_detail, name='sub_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<uuid:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<uuid:pk>/comment/', views.add_comment, name='add_comment_to_post'),
    path('post/<uuid:pk>/comment/<uuid:parent_pk>/', views.add_comment, name='add_reply_to_comment'),
    path('content/<uuid:pk>/upvote/', views.vote, {'is_upvote': True}, name='upvote'),
    path('content/<uuid:pk>/downvote/', views.vote, {'is_upvote': False}, name='downvote')
]