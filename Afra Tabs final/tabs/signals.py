from django.db.models.signals import post_save, post_delete, pre_delete
from django.db.models import F
from django.db import transaction
from django.dispatch import receiver
from .models import Song, Artist, Album  # type: ignore


# -------------------------------
# SONG SIGNALS
# -------------------------------

@receiver(post_save, sender=Song)
def update_tab_counts_on_save(sender, instance, created, **kwargs):
    """
    Update artist and album num_tabs after a song is saved.
    Works for both creation and update.
    """
    with transaction.atomic():  # type: ignore
        # Recalculate album's tab count
        Album.objects.filter(id=instance.album_id).update(  # type: ignore
            num_tabs=Song.objects.filter(album_id=instance.album_id).count()  # type: ignore
        )
        # Recalculate artist's tab count
        Artist.objects.filter(id=instance.artist_id).update(  # type: ignore
            num_tabs=Song.objects.filter(artist_id=instance.artist_id).count()  # type: ignore
        )


@receiver(post_delete, sender=Song)
def update_tab_counts_on_delete(sender, instance, **kwargs):
    """
    Update artist and album num_tabs after a song is deleted.
    Bulk-safe: always recalculates counts.
    """
    with transaction.atomic():  # type: ignore
        Album.objects.filter(id=instance.album_id).update(  # type: ignore
            num_tabs=Song.objects.filter(album_id=instance.album_id).count()  # type: ignore
        )
        Artist.objects.filter(id=instance.artist_id).update(  # type: ignore
            num_tabs=Song.objects.filter(artist_id=instance.artist_id).count()  # type: ignore
        )


# -------------------------------
# ALBUM SIGNALS
# -------------------------------

@receiver(pre_delete, sender=Album)
def update_artist_on_album_delete(sender, instance, **kwargs):
    """
    When an album is deleted, recalc the artist's num_tabs.
    All songs in this album will be deleted automatically because of CASCADE.
    """
    with transaction.atomic():  # type: ignore
        Artist.objects.filter(id=instance.artist_id).update(  # type: ignore
            num_tabs=Song.objects.filter(artist_id=instance.artist_id).count()  # type: ignore
        )