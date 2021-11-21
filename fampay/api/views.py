from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import APIKey, Video
from .serializers import APIKeySerializer, VideoSerializer


class GetVideosPagination(PageNumberPagination):
    page_size = 20
    max_page_size = 20


class APIKeyViewset(viewsets.ModelViewSet):
    """
        Viewset to add a new Youtube Data API Key in the database.
        **Context**
        :class:`results.models.APIKey` .

        **Permission** : AllowAny

        :create:
            create APIKey object for that specific Key.
    """

    serializer_class = APIKeySerializer

    def create(self, request, *args, **kwargs):
        """
        parameters:
            - name: key
              required: true
        """

        # Standard check
        if self.request.data.get('key', ''):
            serializer = self.get_serializer(data={'key': self.request.data.get('key')})
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data,
                                status=status.HTTP_201_CREATED,
                                headers=self.get_success_headers(serializer.data))
        return Response(status=status.HTTP_400_BAD_REQUEST)


class VideosViewset(viewsets.ModelViewSet):
    """
        Viewset to display all the videos, order by latest published date.
        **Context**
        :class:`results.models.Videos` .

        **Permission** : AllowAny

        :list:
            list of Videos data.
    """

    serializer_class = VideoSerializer
    pagination_class = GetVideosPagination

    def list(self, request, *args, **kwargs):
        """ return all the videos, order by latest published date. """

        # Standard check
        if not APIKey.objects.filter(is_limit_over=False).exists():
            raise ValidationError("All APIKey's Quota is over / Empty, Add a new APIKey")

        queryset = Video.objects.all().order_by('-published')
        if queryset:
            return Response(data=self.serializer_class(self.filter_queryset(queryset), many=True).data,
                            status=status.HTTP_200_OK)
        return Response(status=status.HTTP_204_NO_CONTENT)
