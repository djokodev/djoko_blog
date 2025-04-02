from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    return render(
        request,
        "blog/post/comment.html",
        {"post": post, "form": form, "comment": comment},
    )


def post_share(request, post_id):
    post = get_object_or_404(Post.published, id=post_id)
    sent = False

    if request.method == "POST":
        # Création d'une instance du formulaire EmailPostForm avec les données soumises
        # request.POST contient toutes les données envoyées par l'utilisateur via le formulaire
        # Cette ligne permet de récupérer ces données pour les valider et les traiter ensuite
        form = EmailPostForm(request.POST)
        print(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            print(cd)
            # Construction de l'URL absolue pour le post (Ex Résultat: 'https://www.monblog.com/blog/mon-article/')
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n{cd['name']}'s comments: {cd['comments']}"
            send_mail(subject, message, "djoko.dev.pro@gmail.com", [cd["to"]])
            sent = True
    else:
        form = EmailPostForm()
    return render(
        request, "blog/post/share.html", {"post": post, "form": form, "sent": sent}
    )


class PostListView(ListView):
    """Alternative post_list view"""

    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = "blog/post/list.html"


def post_list(request, tag_slug=None):
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get("page", 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, "blog/post/list.html", {"posts": posts, "tag": tag})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post.published,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )

    comments = post.comments.filter(active=True)
    form = CommentForm()

    # Récupère les IDs des tags associés à l'article actuel (post)
    # La méthode `values_list("id", flat=True)` renvoie une liste simple contenant uniquement les IDs des tags, 
    # ce qui permet d'extraire uniquement les valeurs nécessaires pour les prochaines étapes.
    post_tags_ids = post.tags.values_list("id", flat=True)

    # Récupère tous les articles publiés qui partagent au moins un tag avec l'article actuel.
    # La méthode `filter(tags__in=post_tags_ids)` permet de sélectionner les articles ayant des tags en commun avec l'article actuel.
    # La méthode `exclude(id=post.id)` permet d'exclure l'article courant de la liste des articles similaires.
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)

    # Utilise la fonction `annotate()` pour ajouter un champ calculé "same_tags" à chaque article,
    # qui correspond au nombre de tags partagés avec l'article actuel.
    # `Count("tags")` est une fonction d'agrégation qui compte le nombre de tags pour chaque article dans le QuerySet.
    # Puis, trie les articles similaires :
    # 1. D'abord par `same_tags` en ordre décroissant (-same_tags), 
    #    afin que les articles ayant le plus de tags en commun apparaissent en premier.
    # 2. Ensuite, par `publish` en ordre décroissant (-publish), 
    #    pour afficher les articles les plus récents parmi ceux ayant le même nombre de tags partagés.
    # Enfin, la méthode `[:3]` limite la sélection aux trois premiers articles les plus pertinents.
    similar_posts = similar_posts.annotate(same_tags=Count("tags")).order_by("-same_tags", "-publish")[:3]

    return render(
        request,
        "blog/post/detail.html",
        {
            "post": post,
            "comments": comments,
            "form": form,
            "similar_posts": similar_posts,
        },
    )
