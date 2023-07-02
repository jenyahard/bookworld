from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from book import views

app_name = 'book'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('profile/<int:pk>/', views.ProfileView.as_view(), name='profile'),
    path('editprofile/<int:pk>/', views.UserUpdateView.as_view(), name='edit_profile'),
    path('addbook/', views.AddBookView.as_view(), name='add_book'),
    path('editbook/<int:pk>/', views.BookUpdateView.as_view(), name='edit_book'),
    path('deletebook/<int:pk>/', views.BookDeleteView.as_view(), name='delete_book'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    path('author/<slug:author_slug>/', views.AuthorPostsView.as_view(), name='author_books'),
    path('addcomment/<int:pk>/', views.AddCommentView.as_view(), name='add_comment'),
    path('editcomment/<int:post_id>/<int:comment_id>/', views.EditCommentView.as_view(), name='edit_comment'),
    path('deletecomment/<int:post_id>/<int:comment_id>/', views.DeleteCommentView.as_view(), name='delete_comment'),
] 

urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT
                       )
