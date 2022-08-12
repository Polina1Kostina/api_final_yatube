from django.urls import include, path
from rest_framework import routers
from api.views import (
    PostViewSet, UserViewSet, CommentViewSet, FollowViewSet, GroupViewSet)

app_name = 'api'

v1_router = routers.DefaultRouter()
v1_router.register(r'users', UserViewSet)
v1_router.register(r'posts', PostViewSet)
v1_router.register(r'users', UserViewSet)
v1_router.register(r'groups', GroupViewSet)
v1_router.register(r'follow', FollowViewSet, basename='follow')
v1_router.register(
    r'^posts/(?P<post_id>\d+)/comments', CommentViewSet, basename='comments')


urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]
