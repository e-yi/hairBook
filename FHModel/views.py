import base64
import io
import logging

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .faceShape.get_features import get_face

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
