from django.db import models


class Video(models.Model):
    title = models.TextField()
    description = models.TextField()
    video_id = models.TextField()
    channel_id = models.TextField()
    published = models.DateTimeField(auto_now=False)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name = 'Video'
        verbose_name_plural = 'Videos'

    def __str__(self):
        return self.title


class VideoThumbNail(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="thumbnail")
    screen_size = models.CharField(max_length=20)
    url = models.TextField()

    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name = 'Video ThumbNail'
        verbose_name_plural = 'Video ThumbNails'

    def __str__(self):
        return self.video.title


class APIKey(models.Model):
    key = models.TextField()
    is_limit_over = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'APIKey'
        verbose_name_plural = 'APIKeys'

    def __str__(self):
        return self.key
