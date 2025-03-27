from django.urls import path
from  blog.views import post_list, post_detail


# La ligne suivante définit le nom de l'application pour l'espace de noms des URL.
# Cela permet de faire référence aux URL de cette application de manière unique,
# même si d'autres applications ont des noms de vues similaires.
# Par exemple, si vous avez une autre application avec une vue nommée 'post_list',
# vous pouvez toujours faire référence à la vue 'post_list' de l'application 'blog'
# en utilisant 'blog:post_list'.
app_name = 'blog'

urlpatterns = [
    path('', post_list, name='post_list'),
    path('<int:id>/', post_detail, name='post_detail'),
 ]