from django.contrib import admin
from .models import Artist, Album, Song, SongChangeLog, Tabber


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ("name", "num_tabs")
    search_fields = ("name",)
    readonly_fields = ("name_cleaned", "path", "artist_img", "num_tabs")
    fieldsets = (
        (None, {"fields": ("name",)}),
        (
            "Auto-generated Fields",
            {
                "fields": ("name_cleaned", "path", "artist_img"),
                "classes": ("collapse",),
            },
        ),
        (
            "Stats",
            {"fields": ("num_tabs",)},
        ),
    )


class SongInline(admin.TabularInline):
    model = Song
    extra = 0
    fields = (
        "title",
        "track_num",
        "duration",
        "riffs",
        "is_filler",
        "difficulty",
        "was_request",
        "artist_verified",
        "tuning",
        "tabber",
        "tab_description",
        "cover_video",
    )
    filter_horizontal = ("tabber",)



@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ("title", "artist", "release_year", "is_complete", "num_tabs", "has_filler")
    list_filter = ("is_complete", "has_filler", "release_year")
    search_fields = ("title", "artist__name")
    readonly_fields = ("title_cleaned", "album_img", "path", "num_tabs")
    inlines = [SongInline]

    fieldsets = (
        (None, {"fields": ("title", "artist", "release_year")}),
        (
            "Auto-generated Fields",
            {
                "fields": ("title_cleaned", "album_img", "path"),
                "classes": ("collapse",),
            },
        ),
        (
            "Additional Info",
            {"fields": ("is_complete", "has_filler", "tuning", "cover_playlist")},
        ),
        (
            "Stats",
            {"fields": ("num_tabs",)},
        ),
    )


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "album",
        "artist",
        "track_num",
        "duration",
        "riffs",
        "is_filler",
        "difficulty",
        "was_request",
        "artist_verified",
    )
    list_filter = (
        "artist",
        "album",
        "difficulty",
        "was_request",
        "artist_verified",
        "is_filler",
    )
    search_fields = ("title", "album__title", "artist__name")
    filter_horizontal = ("tabber",)
    readonly_fields = (
        "title_cleaned",
        "path",
        "tab_files",
        "date_added",
        "date_last_edited",
    )

    fieldsets = (
        (None, {"fields": ("title", "album", "artist")}),
        (
            "Details",
            {
                "fields": (
                    "track_num",
                    "duration",
                    "riffs",
                    "tuning",
                    "difficulty",
                    "was_request",
                    "artist_verified",
                    "is_filler",
                ),
            },
        ),
        (
            "Tab Info",
            {"fields": ("tabber", "tab_description", "cover_video")},
        ),
        (
            "Auto-generated Fields",
            {
                "fields": ("title_cleaned", "tab_files", "path"),
                "classes": ("collapse",),
            },
        ),
        (
            "Timestamps",
            {"fields": ("date_added", "date_last_edited")},
        ),
    )


@admin.register(SongChangeLog)
class SongChangeLogAdmin(admin.ModelAdmin):
    list_display = ("song", "change_date", "change_summary")
    list_filter = ("change_date",)
    search_fields = ("song__title", "change_summary")
    date_hierarchy = "change_date"


@admin.register(Tabber)
class TabberAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    readonly_fields = ("name_cleaned", "tabber_img")
    fieldsets = (
        (None, {"fields": ("name", "youtube")}),
        (
            "Auto-generated",
            {"fields": ("name_cleaned", "tabber_img"), "classes": ("collapse",)},
        ),
    )