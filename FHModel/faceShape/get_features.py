# coding: utf-8

# In[1]:


# ----------------------------------拟合圆，得到圆心和半径------------------------------------------#
from numpy import *  # 导入numpy的库函数



def circleLeastFit(points):
    center_x = 0.0
    center_y = 0.0
    radius = 0.0

    sum_x = sum_y = 0.0
    sum_x2 = sum_y2 = 0.0
    sum_x3 = sum_y3 = 0.0
    sum_xy = sum_x1y2 = sum_x2y1 = 0.0
    N = len(points)
    for i in range(1, N):
        x = points[i][0]
        y = points[i][1]
        x2 = x * x
        y2 = y * y
        sum_x += x
        sum_y += y
        sum_x2 += x2
        sum_y2 += y2
        sum_x3 += x2 * x
        sum_y3 += y2 * y
        sum_xy += x * y
        sum_x1y2 += x * y2
        sum_x2y1 += x2 * y

    C = D = E = G = H = 0.0
    a = b = c = 0.0
    C = N * sum_x2 - sum_x * sum_x
    D = N * sum_xy - sum_x * sum_y
    E = N * sum_x3 + N * sum_x1y2 - (sum_x2 + sum_y2) * sum_x
    G = N * sum_y2 - sum_y * sum_y
    H = N * sum_x2y1 + N * sum_y3 - (sum_x2 + sum_y2) * sum_y
    a = (H * D - E * G) / (C * G - D * D)
    b = (H * C - E * D) / (D * D - G * C)
    c = -(a * sum_x + b * sum_y + sum_x2 + sum_y2) / N

    center_x = a / (-2)
    center_y = b / (-2)
    radius = sqrt(a * a + b * b - 4 * c) / 2

    return center_x, center_y, round(radius, 2)


# In[2]:


# ----------------------------------分析图片，得到响应json--------------------------------------#
# -*- coding: utf-8 -*-
import urllib.request
import urllib.error
import time
import json


def faceIdentify(fr):
    http_url = 'https://api-cn.faceplusplus.com/facepp/v3/detect'
    key = "enFC8NNZcf19CNRZGhGMvGKPHtMgVkfB"
    secret = "kIV15LIXTSX0gKflGEYHXekj8-mgEuHE"
    # filepath = r"gg.jpg"

    boundary = '----------%s' % hex(int(time.time() * 1000))
    data = []
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_key')
    data.append(key)

    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_secret')
    data.append(secret)

    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"; filename=" "' % 'image_file')
    data.append('Content-Type: %s\r\n' % 'application/octet-stream')
    data.append(fr.read())
    fr.close()
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'return_landmark')
    data.append('2')
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'return_attributes')
    data.append(
        "gender,age,smiling,headpose,facequality,blur,eyestatus,emotion,ethnicity,beauty,mouthstatus,eyegaze,skinstatus")
    data.append('--%s--\r\n' % boundary)

    for i, d in enumerate(data):
        if isinstance(d, str):
            data[i] = d.encode('utf-8')

    http_body = b'\r\n'.join(data)

    # build http request
    req = urllib.request.Request(url=http_url, data=http_body)

    # header
    req.add_header('Content-Type', 'multipart/form-data; boundary=%s' % boundary)

    try:
        # post data to server
        resp = urllib.request.urlopen(req, timeout=5)
        # get response
        qrcont = resp.read()
        # if you want to load as json, you should decode first,
        # for example: json.loads(qrcont.decode('utf-8'))
        text = json.loads(qrcont.decode('utf-8'))
        tt = text.get('faces')[0].get('landmark')
        return tt
    except urllib.error.HTTPError as e:
        print(e.read().decode('utf-8'))
        return 'wrong'


# In[3]:


# ---------------------------------------特征点分析----------------------------------------------#
import math


def qradium(a, b, t):
    list1 = []
    for i in range(a, b):
        tt = t.get('contour_left' + str(i))
        list1.append([tt.get('x'), tt.get('y')])
    x, y, r = circleLeastFit(list1)
    return r


def chinhu(t):
    list2 = []
    for i in range(14, 17):
        text2 = t.get('contour_left' + str(i))
        list2.append([text2.get('x'), text2.get('y')])
        text3 = t.get('contour_right' + str(i))
        list2.append([text3.get('x'), text3.get('y')])
    text4 = t.get('contour_chin')
    list2.append([text4.get('x'), text4.get('y')])
    x, y, r = circleLeastFit(list2);
    return r


# -----------------------------调用这个方法得到七个特征---------------------------------#
def handle_features(text1):
    w1 = round(math.sqrt((text1.get('contour_right1').get('x') - text1.get('contour_left1').get('x')) ** 2 + (
            text1.get('contour_right1').get('y') - text1.get('contour_left1').get('y')) ** 2), 2)
    w2 = round(math.sqrt((text1.get('contour_right3').get('x') - text1.get('contour_left3').get('x')) ** 2 + (
            text1.get('contour_right3').get('y') - text1.get('contour_left3').get('y')) ** 2), 2)
    w3 = round(math.sqrt((text1.get('contour_right9').get('x') - text1.get('contour_left9').get('x')) ** 2 + (
            text1.get('contour_right9').get('y') - text1.get('contour_left9').get('y')) ** 2), 2)
    h = round(math.sqrt((text1.get('contour_chin').get('x') - text1.get('nose_bridge1').get('x')) ** 2 + (
            text1.get('contour_chin').get('y') - text1.get('nose_bridge1').get('y')) ** 2), 2)
    r1 = qradium(1, 7, text1)
    r2 = qradium(7, 14, text1)
    r3 = chinhu(text1)

    return w1 / h, w2 / h, w3 / h, h / h, r1 / h, r2 / h, r3 / h


from sklearn.externals import joblib
clf = joblib.load('./FHModel/faceShape/clf.pkl')


def get_face(img):
    x = []
    text = faceIdentify(img)
    w1, w2, w3, h, r1, r2, r3 = handle_features(text)
    x = [[w1 / h, w2 / h, w3 / h, h / h, r1 / h, r2 / h, r3 / h]]
    y = clf.predict(x)
    # print(y)
    return y
