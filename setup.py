import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="hmedia",  # 模块名称
    version="1.0.0",  # 当前版本
    author="代码厨子",  # 作者
    author_email="15755153@qq.com",  # 作者邮箱
    description="Django本地存储的图片，前端调用通过参数生成缩略图与格式转换",  # 模块简介
    long_description=long_description,  # 模块详细介绍
    long_description_content_type="text/markdown",  # 模块详细介绍格式
    url="https://github.com/spirits001/python-HMedia",  # 模块github地址
    packages=setuptools.find_packages(),  # 自动找到项目中导入的模块
    # 模块相关的元数据
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # 依赖模块
    install_requires=[
        'django',
        'pillow'
    ],
    python_requires='>=3',
)