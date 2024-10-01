from django.contrib import admin

from .models import Tweet, Like

@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = (
        "payload",
        "user",
        "created_at",
        "updated_at",
    )
    list_search = (
        "payload",
        "user__username",
    )
    list__filter= (
        "created_at",
    )


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = (
        "tweet",
        "user",
        "created_at",
        "updated_at",
    )
    list_search = (
        "user__username",
    )
    list_filter= (
        "created_at",
    )