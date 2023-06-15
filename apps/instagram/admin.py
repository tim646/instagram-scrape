from django.contrib import admin
from django.forms import ModelForm, PasswordInput

from .models import InstagramPost, InstagramScrape


class InstagramScrapeModelAdmin(ModelForm):
    """InstagramScrapeModelAdmin is a ModelForm for InstagramScrape that hides the password field."""

    class Meta:
        model = InstagramScrape
        fields = "__all__"
        widgets = {
            "password": PasswordInput(render_value=True),
        }


class MyScrapeInfoAdmin(admin.ModelAdmin):
    """with this class we are overriding the default ModelAdmin form for InstagramScrape"""

    form = InstagramScrapeModelAdmin


@admin.register(InstagramScrape)
class InstagramScrapeAdmin(MyScrapeInfoAdmin):
    list_display = ("username", "target_username", "created_at")
    readonly_fields = ("created_at", "updated_at")

    def has_add_permission(self, request):
        if self.model.objects.count() > 0:
            return False
        return True


@admin.register(InstagramPost)
class InstagramPostAdmin(admin.ModelAdmin):
    list_display = ("id", "link", "likes", "created_day", "created_at")
    list_filter = ("created_at",)
    readonly_fields = ("created_at", "updated_at")
