from django.contrib import admin
from .models import *


class FaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'faceType', 'hairstyle')

    def hairstyle(self, obj):
        return [hairstyle.hairstyle for hairstyle in obj.hairstyles.all()]

    hairstyle.short_description = '适合发型'


class HairstyleAdmin(admin.ModelAdmin):
    list_display = ('id', 'hairstyle', 'curlDegree', 'heatDegree', 'get_faceType')

    def get_faceType(self, obj):
        return [face.faceType for face in obj.faceType.all()]

    get_faceType.short_description = '适合脸型'


class HairAdmin(admin.ModelAdmin):
    list_display = ('id', 'hairstyle', 'length', 'gender', 'heatDegree', 'heatCount', 'pictureURL')

    def pictureURL(self, obj):
        return settings.PIC_URL + obj.filename

    def heatDegree(self, obj):
        return obj.hairstyle.heatDegree

    pictureURL.short_description = '图片URL'
    heatDegree.short_description = '热度'


admin.site.register(Face, FaceAdmin)
admin.site.register(Hairstyle, HairstyleAdmin)
admin.site.register(Hair, HairAdmin)
