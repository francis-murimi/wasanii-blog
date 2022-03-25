from django.conf.urls import url
from django.urls import path
from . import views
from blog.views import blog_add

app_name = 'blog'
urlpatterns = [
    path('blog/add-blog/',views.add_blog,name='add_blog'),
    path('blog/add-topic/',views.add_topic,name='add_topic'),
    path('blog/topic/<int:id>/',views.topic_detail,name='topic_detail'),
    path('add-blog/',views.blog_add.as_view(),name='blog_add'),
    path('blog/<int:blogid>/preference/<int:userpreference>/',views.blogpreference,name='blogpreference'),
    path('blog/vote/<int:topicid>/preference/<int:userpreference>/',views.topicpreference,name='topicpreference'),
    path('blog/blog_list/',views.blog_list,name='blog_list'),
    path('blog/<category_slug>/',views.blog_list,name='blog_list_by_category'),
    path('blog/<int:id>/<slug>/',views.blog_detail,name='blog_detail'),
    path('my-blogs/',views.edit_list,name='edit_list'),
    path('archive-blog/<int:id>/',views.archive_blog, name='archive_blog'),
    path('publish-blog/<int:id>/',views.publish_blog, name='publish_blog'),
    path('edit-blog/<int:id>/',views.edit_blog, name='edit_blog'),
    path('create-category-blog/',views.create_category, name='create_category'),
]