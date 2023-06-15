from django.db import models
from django.utils.translation import gettext_lazy as _
from django_resized import ResizedImageField


class InstagramPost(models.Model):
    image = ResizedImageField(size=[720, 400], upload_to="instagram", verbose_name=_("Image"))
    link = models.URLField(verbose_name=_("Link"))
    likes = models.PositiveIntegerField(default=0, verbose_name=_("Likes"))
    text = models.TextField(verbose_name=_("Text"), null=True, blank=True)
    created_day = models.DateField(verbose_name=_("Created day"), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    class Meta:
        verbose_name = _("Instagram post")
        verbose_name_plural = _("Instagram posts")


class InstagramScrape(models.Model):
    username = models.CharField(max_length=255, verbose_name=_("Username"))
    password = models.CharField(max_length=255, verbose_name=_("Password"))
    target_username = models.CharField(max_length=255, verbose_name=_("Target username"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    class Meta:
        verbose_name = _("Instagram scrape")
        verbose_name_plural = _("Instagram scrapes")

    def __str__(self):
        return self.username

    @staticmethod
    def get_solo():
        return InstagramScrape.objects.first()
