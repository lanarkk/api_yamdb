from rest_framework import filters, mixins, viewsets

from api.permissions import IsAdminUserOrReadOnly


class ViewsetsGenericsMixin(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin
):
    """Создает класс (миксин) обобщенного вьюсета.

    Он допускает только выдачу списка объектов, создание и удаление объкета.
    В нем настроено:
        - поле 'slug' используется в качестве pk;
        - права доступа;
        - поиск по полю 'name'
    """

    lookup_field = 'slug'
    permission_classes = (IsAdminUserOrReadOnly, )
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class AllowedMethodsMixin(viewsets.ModelViewSet):
    """Создает миксин с настроенными допустимыми методами (все, кроме PUT)."""

    http_method_names = [
        'get', 'post', 'patch', 'delete', 'head', 'options', 'trace'
    ]
