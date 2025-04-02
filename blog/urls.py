from django.urls import path
from blog.views import post_list, post_detail, PostListView, post_share, post_comment


# La ligne suivante définit le nom de l'application pour l'espace de noms des URL.
# Cela permet de faire référence aux URL de cette application de manière unique,
# même si d'autres applications ont des noms de vues similaires.
# Par exemple, si vous avez une autre application avec une vue nommée 'post_list',
# vous pouvez toujours faire référence à la vue 'post_list' de l'application 'blog'
# en utilisant 'blog:post_list'.
app_name = "blog"

urlpatterns = [
    path("", post_list, name="post_list"),
    path("tag/<slug:tag_slug>", post_list, name="post_list_by_tag"),
    # path("", PostListView.as_view(), name="post_list"),
    path(
        "<int:year>/<int:month>/<int:day>/<slug:post>/", 
        post_detail, 
        name="post_detail"
    ),
    path('<int:post_id>/share/', post_share, name='post_share'),
    path('<int:post_id>/comment/', post_comment, name='post_comment'),
]
