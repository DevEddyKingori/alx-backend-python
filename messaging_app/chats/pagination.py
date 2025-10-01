from rest_framework.pagination import PageNumberPagination
from reste_framework.response import Response

class MessagePagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response(
            'count': self.page.paginator.count,   # total records
            'total_pages': self.page.paginator.num_pages,  # total pages
            'current_page': self.page.number,    # current page number
            'next': self.get_next_link(),        # next page link
            'previous': self.get_previous_link(),# prev page link
            'results': data                      # paginated results
        )
