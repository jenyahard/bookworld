from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count

from book.models import Book, Author

admin.site.site_title = 'Администрирование блога'
admin.site.site_header = 'Администрирование блога'


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title',
                    'display_authors',
                    'text',
                    'display_image',
                    'is_archived'
                    ]

    def display_image(self, obj):
        if obj.image:
            image_html = format_html(f'<img src="{obj.image.url}" width="50" height="50" alt="{obj.image}">')
            return image_html
        else:
            return None

    display_image.short_description = 'Изображение'
    display_image.allow_tags = True

    def display_authors(self, obj):
        authors = obj.author.all()
        return ', '.join(str(author) for author in authors)

    display_authors.short_description = 'Авторы'


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['author_name', 'book_count', 'comment_count', 'userdata']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(book_count=Count('author'),
                                     comment_count=Count('author__comment')
                                     )
        return queryset

    def book_count(self, obj):
        return obj.book_count
    
    def comment_count(self, obj):
        return obj.comment_count

    comment_count.admin_order_field = 'comment_count'
    comment_count.short_description = 'Количество комментариев у автора'

    book_count.admin_order_field = 'book_count'
    book_count.short_description = 'Количество книг у автора'
