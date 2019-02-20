from rest_framework import serializers
from .models import *


class FaceSerializer(serializers.ModelSerializer):
    hairstyle = serializers.SerializerMethodField()

    class Meta:
        model = Face
        fields = ('id', 'faceType', 'hairstyle')

    def get_hairstyle(self, obj):
        return [(hairstyle.id, hairstyle.hairstyle) for hairstyle in obj.hairstyles.all()]


class HairstyleSerializer(serializers.ModelSerializer):
    faceType = serializers.SerializerMethodField()

    class Meta:
        model = Hairstyle
        fields = ('id', 'hairstyle', 'curlDegree', 'heatDegree', 'faceType')

    def get_faceType(self, obj):
        return [(face.id, face.faceType) for face in obj.faceType.all()]


class HairSerializer(serializers.ModelSerializer):
    pictureURL = serializers.SerializerMethodField()

    class Meta:
        model = Hair
        fields = ('id', 'hairstyle', 'length', 'gender', 'heatCount', 'pictureURL')

    def get_pictureURL(self, obj):
        return settings.PIC_URL + obj.filename
