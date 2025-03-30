from django.conf import settings
from django.db import models
from django.db.models.functions import Now
from django.urls import reverse


class PublishedManager(models.Manager):
    """
    Le PublishedManager est un gestionnaire personnalisé pour le modèle Post.
    Il est utilisé pour récupérer uniquement les articles qui ont le statut "PUBLISHED".
    
    La méthode get_queryset() surcharge la méthode par défaut pour filtrer les articles
    et ne retourner que ceux dont le statut est égal à Post.Status.PUBLISHED.
    """
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"

    title = models.CharField(max_length=250)
    # Ce champ est utilisé pour stocker la représentation URL-friendly du titre.
    # Il est généralement utilisé dans l'URL de l'article.
    # Le paramètre unique_for_date="publish" garantit que la valeur du slug est unique pour une date donnée.
    # Cela signifie qu'il ne peut pas y avoir deux articles avec le même slug publiés le même jour.
    # Cette contrainte permet d'éviter les conflits d'URL et assure que chaque article a une URL unique.
    slug = models.SlugField(max_length=250, unique_for_date="publish")
    
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

    objects = models.Manager()
    published = PublishedManager()

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
    
    def get_absolute_url(self):
        """
        Cette méthode retourne l'URL absolue pour un article de blog spécifique.
        Elle est utilisée pour générer des liens vers les détails d'un article de blog.

        L'importance de cette méthode réside dans sa capacité à fournir une URL unique et permanente pour chaque article de blog.
        Cela permet de référencer facilement un article spécifique, que ce soit dans les templates, les vues ou même à l'extérieur du site web.

        En utilisant cette méthode, nous assurons que les liens vers les articles de blog sont générés de manière cohérente et centralisée.
        Cela facilite la maintenance du code, car toute modification de la structure des URL peut être effectuée en un seul endroit.

        De plus, cette méthode est essentielle pour le bon fonctionnement des fonctionnalités de navigation et de référencement.
        Les moteurs de recherche peuvent indexer les articles de blog plus efficacement grâce à des URL claires et descriptives.
        """
        return reverse(
            "blog:post_detail", 
            args=[
                self.publish.year,
                self.publish.month,
                self.publish.day,
                self.slug
            ]
        )

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["created"]
        indexes = [
            models.Index(fields=["created"]),
        ]

    def __str__(self):
        return f"Comment by {self.name} on {self.post}"