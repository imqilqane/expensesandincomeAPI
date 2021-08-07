from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination

class PostLimitOfPage(PageNumberPagination):
    page_size = 10