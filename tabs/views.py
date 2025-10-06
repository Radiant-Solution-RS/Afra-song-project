# type: ignore
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import JsonResponse
from .models import Artist, Album, Song, Tabber  # type: ignore


def index(request):
    """Home page view with latest tabs and statistics"""
    # Get latest 4 songs for the home page
    latest_songs = Song.objects.filter(is_filler=False).select_related('artist', 'album').order_by('-date_added')[:4]
    
    # Get statistics
    stats = {
        'total_tabs': Song.objects.filter(is_filler=False).count(),
        'total_albums': Album.objects.count(),
        'total_artists': Artist.objects.count(),
        'verified_tabs': Song.objects.filter(artist_verified=True, is_filler=False).count(),
        'total_riffs': Song.objects.aggregate(total_riffs=Count('riffs'))['total_riffs'] or 0,
        'total_hours': 200,  # You can calculate this based on song durations if needed
    }
    
    context = {
        'latest_songs': latest_songs,
        'stats': stats,
    }
    return render(request, 'tabs/index.html', context)


def tabs_list(request):
    """Songs/tabs listing page with filtering"""
    songs = Song.objects.filter(is_filler=False).select_related('artist', 'album').order_by('-date_added')
    
    # Apply search filter
    search_query = request.GET.get('search')
    if search_query:
        songs = songs.filter(
            Q(title__icontains=search_query) |
            Q(artist__name__icontains=search_query) |
            Q(album__title__icontains=search_query)
        )
    
    # Apply tuning filter
    tuning_filter = request.GET.get('tuning')
    if tuning_filter and tuning_filter != 'All Tunings':
        songs = songs.filter(tuning=tuning_filter)
    
    # Apply difficulty filter
    min_difficulty = request.GET.get('min_difficulty')
    max_difficulty = request.GET.get('max_difficulty')
    if min_difficulty:
        songs = songs.filter(difficulty__gte=int(min_difficulty))
    if max_difficulty:
        songs = songs.filter(difficulty__lte=int(max_difficulty))
    
    # Apply sorting
    sort_by = request.GET.get('sort', 'A to Z')
    if sort_by == 'Z to A':
        songs = songs.order_by('-title')
    elif sort_by == 'Recently Added':
        songs = songs.order_by('-date_added')
    elif sort_by == 'Most Popular':
        # You can implement popularity logic here
        songs = songs.order_by('-date_added')
    else:  # A to Z
        songs = songs.order_by('title')
    
    # Pagination
    paginator = Paginator(songs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get counts for categories
    counts = {
        'songs': Song.objects.filter(is_filler=False).count(),
        'albums': Album.objects.count(),
        'artists': Artist.objects.count(),
    }
    
    context = {
        'page_obj': page_obj,
        'counts': counts,
        'search_query': search_query,
        'tuning_filter': tuning_filter,
        'sort_by': sort_by,
        'min_difficulty': min_difficulty,
        'max_difficulty': max_difficulty,
    }
    return render(request, 'tabs/tabs_list.html', context)


def albums_list(request):
    """Albums listing page"""
    albums = Album.objects.select_related('artist').annotate(
        song_count=Count('songs', filter=Q(songs__is_filler=False))
    ).order_by('title')
    
    # Apply search filter
    search_query = request.GET.get('search')
    if search_query:
        albums = albums.filter(
            Q(title__icontains=search_query) |
            Q(artist__name__icontains=search_query)
        )
    
    # Apply sorting
    sort_by = request.GET.get('sort', 'A to Z')
    if sort_by == 'Z to A':
        albums = albums.order_by('-title')
    elif sort_by == 'Recently Added':
        albums = albums.order_by('-id')  # or by a date field if you add one
    else:  # A to Z
        albums = albums.order_by('title')
    
    # Pagination
    paginator = Paginator(albums, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get counts for categories
    counts = {
        'songs': Song.objects.filter(is_filler=False).count(),
        'albums': Album.objects.count(),
        'artists': Artist.objects.count(),
    }
    
    context = {
        'page_obj': page_obj,
        'counts': counts,
        'search_query': search_query,
        'sort_by': sort_by,
    }
    return render(request, 'tabs/albums_list.html', context)


def artists_list(request):
    """Artists listing page"""
    artists = Artist.objects.annotate(
        song_count=Count('songs', filter=Q(songs__is_filler=False))
    ).order_by('name')
    
    # Apply search filter
    search_query = request.GET.get('search')
    if search_query:
        artists = artists.filter(name__icontains=search_query)
    
    # Apply sorting
    sort_by = request.GET.get('sort', 'A to Z')
    if sort_by == 'Z to A':
        artists = artists.order_by('-name')
    elif sort_by == 'Recently Added':
        artists = artists.order_by('-id')
    else:  # A to Z
        artists = artists.order_by('name')
    
    # Pagination
    paginator = Paginator(artists, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get counts for categories
    counts = {
        'songs': Song.objects.filter(is_filler=False).count(),
        'albums': Album.objects.count(),
        'artists': Artist.objects.count(),
    }
    
    context = {
        'page_obj': page_obj,
        'counts': counts,
        'search_query': search_query,
        'sort_by': sort_by,
    }
    return render(request, 'tabs/artists_list.html', context)


def about(request):
    """About page view"""
    return render(request, 'tabs/about.html')


def song_detail(request, artist_slug, album_slug, song_slug):
    """Individual song detail page"""
    song = get_object_or_404(
        Song.objects.select_related('artist', 'album').prefetch_related('tabber'),
        artist__name_cleaned=artist_slug,
        album__title_cleaned=album_slug,
        title_cleaned=song_slug,
        is_filler=False
    )
    
    # Get related songs from the same album
    related_songs = Song.objects.filter(
        album=song.album,
        is_filler=False
    ).exclude(id=song.id).select_related('artist', 'album')[:4]
    
    context = {
        'song': song,
        'related_songs': related_songs,
    }
    return render(request, 'tabs/song_detail.html', context)


def artist_detail(request, artist_slug):
    """Individual artist detail page"""
    artist = get_object_or_404(Artist, name_cleaned=artist_slug)
    
    # Get artist's albums and songs
    albums = Album.objects.filter(artist=artist).annotate(
        song_count=Count('songs', filter=Q(songs__is_filler=False))
    ).order_by('release_year')
    
    # Get all of the artist's songs, not just recent ones
    songs = Song.objects.filter(
        artist=artist,
        is_filler=False
    ).select_related('album').order_by('-date_added')
    
    context = {
        'artist': artist,
        'albums': albums,
        'songs': songs,  # Changed from recent_songs to songs
    }
    return render(request, 'tabs/artist_detail.html', context)


def album_detail(request, artist_slug, album_slug):
    """Individual album detail page"""
    album = get_object_or_404(
        Album.objects.select_related('artist'),
        artist__name_cleaned=artist_slug,
        title_cleaned=album_slug
    )
    
    # Get all songs in the album
    songs = Song.objects.filter(
        album=album
    ).select_related('artist').order_by('track_num', 'title')
    
    context = {
        'album': album,
        'songs': songs,
    }
    return render(request, 'tabs/album_detail.html', context)


def search_api(request):
    """API endpoint for search dropdown"""
    query = request.GET.get('q', '').strip()
    
    if len(query) < 2:
        return JsonResponse({'results': []})
    
    results = []
    
    # Search songs (limit to 2)
    songs = Song.objects.filter(
        Q(title__icontains=query),
        is_filler=False
    ).select_related('artist', 'album')[:2]
    
    for song in songs:
        results.append({
            'type': 'song',
            'title': song.title,
            'subtitle': f"{song.artist.name} - {song.album.title}",
            'url': song.get_absolute_url(),
            'verified': song.artist_verified
        })
    
    # Search albums (limit to 2)
    albums = Album.objects.filter(
        Q(title__icontains=query)
    ).select_related('artist')[:2]
    
    for album in albums:
        results.append({
            'type': 'album',
            'title': album.title,
            'subtitle': f"{album.artist.name} ({album.release_year})",
            'url': f"/tabs/artist/{album.artist.name_cleaned}/album/{album.title_cleaned}/",
            'verified': False
        })
    
    # Search artists (limit to 1)
    artists = Artist.objects.filter(
        Q(name__icontains=query)
    )[:1]
    
    for artist in artists:
        results.append({
            'type': 'artist',
            'title': artist.name,
            'subtitle': f"{artist.num_tabs} tab{'s' if artist.num_tabs != 1 else ''}",
            'url': artist.get_absolute_url(),
            'verified': False
        })
    
    return JsonResponse({'results': results[:5]})