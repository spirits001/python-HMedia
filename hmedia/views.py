# encoding: utf-8
"""
@author: hofeng
@license: (C) Copyright 2024.
@contact: hofeng@aqifun.com
@software: Python 3
@file: hmedia
@time: 2024-08-13 13:28
@desc: 参考oss的本地化缩略图
"""
import io
import os
from PIL import Image
from PIL.ImageFile import ImageFile
from django.conf import settings
from django.http import Http404, HttpResponse


class _Hmedia:
    def __init__(self, params: list, file: bytes, ext: str):
        data = dict()
        for item in params:
            i = 0
            data[item[0]] = None
            if '_' not in item[1]:
                value = item[1]
                try:
                    value = int(item[1])
                except:
                    pass
                data[item[0]] = value
                continue
            else:
                data[item[0]] = dict()
            while i < len(item):
                if i:
                    arr = item[i].split('_')
                    value = arr[1]
                    try:
                        value = int(arr[1])
                    except:
                        pass
                    data[item[0]][arr[0]] = value
                i += 1
        self.params = data
        self.file = file
        self.ext = ext

    @staticmethod
    def _resize(file: ImageFile, resize: dict) -> ImageFile or Image:
        # 图片原始宽高
        width, height = file.size
        # 图片原始比例
        radio = width / height
        if resize['m'] == 'lfit':
            # 宽度固定，高度自适应
            if 'w' in resize and 'h' not in resize and width > resize['w']:
                width = resize['w']
                height = int(width / radio)
                return file.resize((width, height), Image.Resampling.LANCZOS)
            # 高度固定，宽度自适应
            if 'h' in resize and 'w' not in resize and height > resize['h']:
                height = resize['h']
                width = int(height * radio)
                return file.resize((width, height), Image.Resampling.LANCZOS)
            # 固定宽高，长边缩放
            if 'w' in resize and 'h' in resize:
                if width > resize['w'] or height > resize['h']:
                    if width / resize['w'] > height / resize['h']:
                        width = resize['w']
                        height = int(width / radio)
                    else:
                        height = resize['h']
                        width = int(height * radio)
                    return file.resize((width, height), Image.Resampling.LANCZOS)
        # 固定宽高，短边缩放
        if resize['m'] == 'mfit' and 'w' in resize and 'h' in resize:
            if width / resize['w'] < height / resize['h']:
                width = resize['w']
                height = int(width / radio)
            else:
                height = resize['h']
                width = int(height * radio)
            return file.resize((width, height), Image.Resampling.LANCZOS)
        # 固定宽高，缩略填充
        if resize['m'] == 'pad' and 'w' in resize and 'h' in resize and 'color' in resize:
            color = f"#{resize['color']}"
            if width / resize['w'] > height / resize['h']:
                width = resize['w']
                height = int(width / radio)
            else:
                height = resize['h']
                width = int(height * radio)
            file = file.resize((width, height), Image.Resampling.LANCZOS)
            imgFIle = Image.new('RGBA', (resize['w'], resize['h']), color)
            imgFIle.paste(file, (int((resize['w'] - width) / 2), int((resize['h'] - height) / 2)))
            return imgFIle
        # 固定宽高，居中裁切
        if resize['m'] == 'fill' and 'w' in resize and 'h' in resize:
            if width / resize['w'] < height / resize['h']:
                width = resize['w']
                height = int(width / radio)
            else:
                height = resize['h']
                width = int(height * radio)
            file = file.resize((width, height), Image.Resampling.LANCZOS)
            imgFIle = Image.new('RGBA', (resize['w'], resize['h']))
            imgFIle.paste(file, (int((resize['w'] - width) / 2), int((resize['h'] - height) / 2)))
            return imgFIle
        return file

    def build(self):
        ret = io.BytesIO()
        with Image.open(io.BytesIO(self.file)) as imgFIle:
            if "resize" in self.params:
                imgFIle = self._resize(imgFIle, self.params["resize"])
            kwargs = {
                'format': self.ext,
                'quality': 90
            }
            if 'format' in self.params:
                kwargs['format'] = self.params['format']
            if 'quality' in self.params:
                kwargs['quality'] = self.params['quality']['q']
            imgFIle.save(ret, **kwargs)
        return HttpResponse(ret.getvalue(), f'image/{kwargs["format"]}')


def hmedia(request, path):
    path = f"{settings.MEDIA_ROOT}{path}"
    if not os.path.exists(path):
        raise Http404('')
    file = open(path, 'rb')
    ext = path.split('.')[-1]
    if "x-oss-process" not in request.GET:
        return HttpResponse(file.read(), f'image/{ext}')
    arr = request.GET["x-oss-process"].split('/')
    if len(arr) and arr[0] == 'image':
        params = list()
        for item in arr:
            if ',' in item:
                params.append(item.split(','))
        h = _Hmedia(params, file.read(), ext)
        return h.build()
    raise Http404('')
