from django.urls import path
from . import views

app_name = 'tabs'

urlpatterns = [
    path('', views.index, name='index'),
    path('tabs/', views.tabs_list, name='tabs_list'),
    path('albums/', views.albums_list, name='albums_list'),
    path('artists/', views.artists_list, name='artists_list'),
    path('about/', views.about, name='about'),
    path('api/search/', views.search_api, name='search_api'),
    path('tabs/<slug:artist_slug>/<slug:album_slug>/<slug:song_slug>/', views.song_detail, name='song_detail'),
    path('tabs/<slug:artist_slug>/', views.artist_detail, name='artist_detail'),
    path('tabs/<slug:artist_slug>/<slug:album_slug>/', views.album_detail, name='album_detail'),
]