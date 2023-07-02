from django.db.models.query import QuerySet
from django.core.paginator import Paginator
from django.db.models import Count


def paginator_custom(self, objects: QuerySet):
    '''Пагинатор:
    Вход - self, objects: QuerySet
    Возвращает - Page
    '''
    paginate_by = 2
    paginator = Paginator(objects, paginate_by)
    page_number = self.request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj
