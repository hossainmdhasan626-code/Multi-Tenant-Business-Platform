from rest_framework.pagination import PageNumberPagination


def reusable_custom_pagination(
    queryset, request, serializer_class, view_instance, page_size=10
):

    paginator = PageNumberPagination()
    paginator.page_size = page_size

    paginated_data = paginator.paginate_queryset(queryset, request, view=view_instance)

    serializer = serializer_class(
        instance=paginated_data, many=True, context={"request": request}
    )

    return paginator.get_paginated_response(serializer.data).data
