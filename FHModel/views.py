import base64
import io
import logging
import random

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from .faceShape.get_features import get_face
from .models import *
from .serializers import *

logger = logging.getLogger('FHModel')

@api_view(['POST'])
def faceShape(request):
    try:
        img64 = request.data['face']
        img = base64.b64decode(img64)
        imageBytes = io.BytesIO(img)
        shape = get_face(imageBytes)
        assert len(shape) == 1
    except Exception as e:
        logger.debug(str(e))
        return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)
    return Response(data={"shape": shape[0]})


class FaceListView(ListAPIView):
    queryset = Face.objects.all()
    serializer_class = FaceSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('id', 'faceType', 'hairstyles')


class HairstyleListView(ListAPIView):
    queryset = Hairstyle.objects.all()
    serializer_class = HairstyleSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_fields = ('id', 'hairstyle', 'curlDegree', 'faceType')
    ordering_fields = ('heatDegree',)


class HairListView(ListAPIView):
    queryset = Hair.objects.all()
    serializer_class = HairSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_fields = ('id', 'hairstyle', 'length', 'gender')
    ordering_fields = ('heatCount',)
