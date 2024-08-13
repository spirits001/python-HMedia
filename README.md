# HMedia实现对本地化图片的丝滑般生成缩略图

我经常使用阿里云的oss服务，我最喜欢oss的功能就是通过简单的参数，就能实现图片的缩略图与格式转换。

但是，如果图片使用本地存储时候，就没办法使用oss的生成缩略图和格式转换功能了。

所以，借着一个项目必须本地化部署的背景，我写了一个模块，让前端方便进行对应渲染。

# 快速开始

## 安装

```bash
pip install hmedia
```

在url.py中增加以下代码

```python
from django.urls import re_path
from hmedia.views import hmedia

urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', hmedia),
]
```

注意，示例中urlpatterns的内容，是增加在您原有内容里，不是覆盖。

另外，media目录是在settings里配置的静态文件目录。如果你不一样，请修改，我的settings内容如下：

```python
MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
```

所以是media。

## 使用方式

前端调用时候，参考阿里云的oss语法规范，目前仅支持图片缩放、格式转换功能。

传送门：[阿里云oss图片处理](https://help.aliyun.com/zh/oss/user-guide/resize-images-4?spm=a2c4g.11186623.0.i1)

也可以在oss管理中的数据处理里，配置图片处理规则，参考其设定的前端调用代码。

# 版本历史

1.0.0 首次发布

