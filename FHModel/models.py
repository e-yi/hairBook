from django.db import models
from django.conf import settings


# Create your models here.
class Face(models.Model):
    faceType = models.CharField(max_length=20, unique=True,
                                verbose_name='脸型')

    def __str__(self):
        return self.faceType

    class Meta:
        verbose_name = '脸型'
        verbose_name_plural = verbose_name


class Hairstyle(models.Model):
    """
    todo 检查heatDegree >=0 <=5
    """
    CURL_DEGREE_CHOICE = [(0, '直'), (1, '微卷'), (2, '大卷'), (3, '内扣'), (4, '外扣')]

    hairstyle = models.CharField(max_length=50, unique=True,
                                 verbose_name='发型大类')
    curlDegree = models.IntegerField(choices=CURL_DEGREE_CHOICE,
                                     verbose_name='卷曲度')
    heatDegree = models.FloatField(verbose_name='流行程度')
    createdTime = models.DateTimeField(auto_now_add=True,
                                       editable=False,
                                       verbose_name="创建时间")
    updatedTime = models.DateTimeField(auto_now=True,
                                       verbose_name="更新时间")
    faceType = models.ManyToManyField('Face',
                                      verbose_name='适合脸型',
                                      related_name='hairstyles',
                                      blank=True)

    def __str__(self):
        return self.hairstyle

    class Meta:
        verbose_name = '发型'
        verbose_name_plural = verbose_name


class Hair(models.Model):
    """
    todo 检查 url格式（以jpg/png结尾等）
    todo 检查 heatCount >= 0
    """
    LENGTH_CHOICE = [(0, '短发'), (1, '中发'), (2, '长发')]
    GENDER_CHOICE = [(0, '男'), (1, '女'), (2, '全部')]

    hairstyle = models.ForeignKey(Hairstyle,
                                  on_delete=models.CASCADE,
                                  verbose_name='发型大类',
                                  related_name='hairs')
    length = models.IntegerField(choices=LENGTH_CHOICE,
                                 verbose_name='长度')
    gender = models.IntegerField(choices=GENDER_CHOICE,
                                 verbose_name='性别')
    heatCount = models.IntegerField(verbose_name='用户试用次数', default=0)
    filename = models.CharField(max_length=50,
                                verbose_name='图片URL（部分）')

    def __str__(self):
        return str(self.hairstyle)+":"+str(self.id)

    class Meta:
        verbose_name = '具体发型'
        verbose_name_plural = verbose_name
