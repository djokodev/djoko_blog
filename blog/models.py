from django.conf import settings
from django.db import models
from django.db.models.functions import Now


class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"

    title = models.CharField(max_length=250)
    # This field is used to store the URL-friendly representation of the title.
    # It is typically used in the URL of the post.
    slug = models.SlugField(max_length=250)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="blog_posts"
    )
    body = models.TextField()
    publish = models.DateTimeField(db_default=Now())
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status, default=Status.DRAFT)

    class Meta:
        # This specifies the default ordering for the Post objects.
        # The "-" before "publish" means that the posts will be ordered in descending order by the publish date.
        ordering = ["-publish"]

        # This creates a database index on the "publish" field in descending order.
        # Indexes improve the speed of database operations on the specified fields.
        indexes = [
            models.Index(fields=["-publish"]),
        ]

    def __str__(self):
        return self.title
