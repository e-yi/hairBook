from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

import logging
import face_recognition
import io
import base64


logger = logging.getLogger('faceLandmarkView')

@api_view(['POST'])
def getFaceLandmarks(request):
    """
    获取脸部特征点
    :param request:
    :return:
    """
    if request.method == 'POST':
        try:
            img64 = request.data['face']
            img = base64.b64decode(img64)
            imageBytes = io.BytesIO(img)
            imageArr = face_recognition.load_image_file(imageBytes)
        except Exception as e:
            logger.debug(str(e))
            return Response(status=status.HTTP_400_BAD_REQUEST)
        face_landmarks_list = face_recognition.face_landmarks(imageArr)
        return Response(data={"face_landmarks_list": face_landmarks_list})
