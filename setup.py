# -*- coding: utf8 -*-
from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setup(
    name='dfelf',
    version='0.2.1',
    packages=['dfelf', 'dfelf.res', 'dfelf.res.Noto_Sans_SC'],
    package_data={
        'dfelf': [
            'LICENSE',
            './dfelf/res/Noto_Sans_SC/NotoSansSC-Regular.otf',
            './dfelf/res/Noto_Sans_SC/OFL.txt'
        ]
    },
    include_package_data=True,
    url='https://github.com/KrixTam/dfelf',
    license='MIT',
    author='Krix Tam',
    author_email='krix.tam@qq.com',
    description='Data File Elf',
    long_description=long_description,
    long_description_content_type="text/markdown",
    project_urls={
        "Bug Tracker": "https://github.com/KrixTam/dfelf/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    py_modules=["dfelf"],
    python_requires=">=3.6",
    install_requires=[
        'pymoment>=0.0.6',
        'ni-config>=0.0.15',
        'pandas>=2.2.2',
        'Pillow>=10.3.0',
        'qrcode>=7.4.2',
        'opencv-python>=4.10.0.84',
        'scikit-image>=0.23.2',
        'PyMuPDF>=1.24.6'
    ]
)
