from django import template
from ..models import Post
from django.db.models import Count
import markdown
from django.utils.safestring import mark_safe


register = template.Library()


@register.simple_tag
def total_posts():
    """Returns the total count of published posts."""
    return Post.published.count()


@register.inclusion_tag("blog/post/latest_posts.html")
def show_latest_posts(count=5):
    """
    Renders the latest published posts using latest_posts.html template.

    Args:
        count (int): Number of latest posts to display. Defaults to 5.

    Returns:
        dict: Context containing latest posts for the template.
    """
    latest_posts = Post.published.order_by("-publish")[:count]
    return {"latest_posts": latest_posts}


@register.simple_tag
def get_most_commented_posts(count=3):
    """
    Returns the most commented published posts.

    This template tag retrieves published blog posts ordered by their comment count.
    It uses Django's annotation and aggregation features to:
    1. Count comments for each post using the 'comments' related name
    2. Filter out posts with no comments (total_comments > 0)
    3. Order posts by comment count in descending order
    4. Limit results to specified count

    Args:
        count (int): Number of posts to return. Defaults to 3.

    Returns:
        QuerySet: Posts ordered by comment count in descending order, limited to 'count' results.
                 Each post object includes a 'total_comments' annotation.
    """
    return (
        Post.published.annotate(total_comments=Count("comments"))
        .filter(total_comments__gt=0)
        .order_by("-total_comments")[:count]
    )

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))