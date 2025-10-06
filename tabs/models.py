# type: ignore
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from django.urls import reverse


class Artist(models.Model):
    name = models.CharField(db_column="artistName", max_length=100)
    name_cleaned = models.CharField(db_column="artistNameCleaned", max_length=100)

    num_tabs = models.IntegerField(db_column="numTabs", default=0)
    artist_img = models.URLField(db_column="artistImage")
    path = models.CharField(db_column="path", max_length=200, blank=True, default="")

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('tabs:artist_detail', kwargs={'artist_slug': self.name_cleaned})
    
    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        self.name_cleaned = slugify(self.name)
        self.path = "/tabs/" + self.name_cleaned
        self.artist_img = (
            "https://f005.backblazeb2.com/file/afras-tabs-artist-images/"
            + self.name_cleaned
            + ".jpg"
        )
        super().save(*args, **kwargs)


class Album(models.Model):
    title = models.CharField(db_column="albumTitle", max_length=100)
    title_cleaned = models.CharField(db_column="albumTitleCleaned", max_length=100)

    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name="albums")
    release_year = models.CharField(db_column="releaseYear", max_length=4)
    album_img = models.URLField(db_column="albumImage")
    num_tabs = models.IntegerField(db_column="numTabs", default=0)
    tuning = models.CharField(db_column="tuning", max_length=100, blank=True, null=True)

    # These will create elements
    is_complete = models.BooleanField(db_column="isComplete", default=False)
    has_filler = models.BooleanField(db_column="hasFiller", default=False)
    cover_playlist = models.URLField(db_column="coverPlaylist", blank=True)

    path = models.CharField(db_column="path", max_length=200, blank=True, default="")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.title_cleaned = slugify(self.title)
        self.album_img = (
            "https://f005.backblazeb2.com/file/afras-tabs-album-arts/"
            + self.title_cleaned
            + ".jpg"
        )
        self.path = "/tabs/" + self.artist.name_cleaned + "/" + self.title_cleaned
        super().save(*args, **kwargs)


class Song(models.Model):
    title = models.CharField(db_column="songTitle", max_length=100)
    title_cleaned = models.CharField(
        db_column="songTitleCleaned", max_length=100, blank=True
    )
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name="songs")
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name="songs")
    duration = models.DurationField(db_column="duration", blank=True, null=True)
    track_num = models.IntegerField(db_column="trackNum", blank=True, null=True)

    tuning = models.CharField(db_column="tuning", max_length=100, blank=True, null=True)
    difficulty = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(4)],
        default=1,
        blank=True,
        null=True,
    )
    riffs = models.IntegerField(db_column="riffs", default=0)
    tabber = models.ManyToManyField("Tabber", blank=True)

    # These will create elements
    artist_verified = models.BooleanField(db_column="artistVerified", default=False)
    cover_video = models.URLField(db_column="coverVideo", blank=True)
    was_request = models.BooleanField(db_column="wasRequest", default=False)
    is_filler = models.BooleanField(default=False)

    date_added = models.DateTimeField(db_column="dateAdded", auto_now_add=True)
    date_last_edited = models.DateTimeField(db_column="dateLastEdited", auto_now=True)

    tab_files = models.URLField(db_column="tabFiles", blank=True, null=True)
    tab_description = models.TextField(
        db_column="tabDescription",
        default="Description not provided",
        blank=True,
        null=True,
    )
    path = models.CharField(db_column="path", max_length=200, blank=True, default="")

    def __str__(self):
        return f"{self.title} - {self.artist.name}"
    
    def get_absolute_url(self):
        return reverse('tabs:song_detail', kwargs={
            'artist_slug': self.artist.name_cleaned,
            'album_slug': self.album.title_cleaned,
            'song_slug': self.title_cleaned
        })
    
    class Meta:
        ordering = ['artist__name', 'album__title', 'track_num', 'title']

    def save(self, *args, **kwargs):
        self.title_cleaned = slugify(self.title)

        if not self.is_filler:
            # Normal song: require an artist and build path/files
            if not self.artist_id:
                if self.album and self.album.artist_id:
                    self.artist = self.album.artist
                else:
                    raise ValueError("Song must have an associated artist.")

            artist_cleaned = getattr(self.artist, "name_cleaned", "").lower()
            album_cleaned = (
                getattr(self.album, "title_cleaned", "").lower() if self.album else ""
            )

            self.tab_files = (
                f"https://f005.backblazeb2.com/file/afras-tabs-tab-files/"
                f"{artist_cleaned}/{album_cleaned}/{self.title_cleaned}"
            )
            self.path = f"/tabs/{artist_cleaned}/{album_cleaned}/{self.title_cleaned}"
        else:
            # Filler: no tab files, no path
            self.tab_files = None
            self.path = ""

        super().save(*args, **kwargs)


class SongChangeLog(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name="changelog")
    change_date = models.DateTimeField(auto_now_add=True)
    change_summary = models.CharField(max_length=500)

    class Meta:
        ordering = ["-change_date"]

    def __str__(self):
        return f"{self.song.title} - {self.change_date.date()}"


class Tabber(models.Model):
    name = models.CharField(db_column="tabberName", max_length=100)
    tabber_img = models.URLField(db_column="tabberImage")
    name_cleaned = models.CharField(db_column="tabberNameCleaned", max_length=100)
    youtube = models.URLField(db_column="youtube", blank=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        self.name_cleaned = slugify(self.name)
        self.tabber_img = (
            "https://f005.backblazeb2.com/file/afras-tabs-tabber-pictures/"
            + self.name_cleaned
            + ".jpg"
        )

        super().save(*args, **kwargs)
