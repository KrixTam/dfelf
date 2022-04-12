# dfelf

由于日常工作需要（有时候还有写blog的需要），总是要处理一些数据文件，很多繁琐的工作希望可以有一个文件精灵来帮我处理，所以就把过去写的小工具重新整理下，形成“数据文件精灵”（“dfelf”）。

“dfelf”为“Data File Elf”的缩写。

因为日常总是需要处理如下文件：
* PDF
* CSV
* 图片

所以数据文件精灵初步设计可以支持以上三类文件的日常处理需要。

## 安装

> pip install --upgrade dfelf

在macOS下，如果要pdf2image运行正常，需要安装Poppler

> conda install -c conda-forge poppler

## PDFFileElf

PDF文件精灵用于日常对*pdf*文件的处理应用。相关方法如下：

* **reorganize**：抽取PDF文件中相关页重新排列组合成一个新的PDF文件；对应的配置设定为*reorganize*。
* **image2pdf**：将图片文件拼接成一个PDF文件，每个图片为一页；对应的配置设定为*image2pdf*。
* **to_image**：将PDF文件相关页输出成图片，每一页为一个图片，以页码为文件后续；对应的配置设定为*2image*。

配置文件设定如下：

```json
{
    'reorganize': {
        'input': 'input_filename',
        'output': 'output_filename',
        'pages': [1]
    },
    'image2pdf': {
        'images': [],
        'output': 'output_filename'
    },
    '2image': {
        'input': 'input_filename',
        'output': 'output_filename_prefix',
        'format': 'png',
        'dpi': 200,
        'pages': [1]
    }
}
```

## CSVFileElf

CSV文件精灵用于日常对*csv*文件的处理应用。相关方法如下：

* **add**：将*tags*下定义的*csv*文件，按照*key*进行匹配，补充相关字段到*base*的*csv*文件中；对应的配置设定为*add*。
* **join**：将*files*下定义的*csv*文件，拼接到*base*的*csv*文件中；对应的配置设定为*join*。
* **exclude**：根据*exclusion*下定义的条件（*op*支持的操作有：'=', '!=', '>', '>=', '<=', '<'），对*input*的*csv*文件内容进行剔除处理；对应的配置设定为*exclude*。
* **filter**：根据*filters*下定义的条件（*op*支持的操作有：'=', '!=', '>', '>=', '<=', '<'），对*input*的*csv*文件内容进行筛选处理；对应的配置设定为*filter*。
* **split**：根据*key*对*input*的*csv*文件进行拆解处理；对应的配置设定为*split*。

配置文件设定如下：

```json
{
    'add': {
        'base': {
            'name': 'base_filename',
            'key': 'key_field',
            'drop_duplicates': False,
        },
        'output': {
            'name': 'output_filename',
            'BOM': False,
            'non-numeric': []
        },
        'tags': [
            {
                'name': 'base_filename',
                'key': 'key_field',
                'fields': ['field A', 'field B'],
                'defaults': ['default value of field A', 'default value of field B']
            }
        ]
    },
    'join': {
        'base': 'base_filename',
        'output': {
            'name': 'output_filename',
            'BOM': False,
            'non-numeric': []
        },
        'files': [
            {
                'name': 'filename',
                'mappings': {}
            }
        ]
    },
    'exclude': {
        'input': 'input_filename',
        'exclusion': [
            {
                'key': 'field',
                'op': '=',
                'value': 123
            }
        ],
        'output': {
            'name': 'output_filename',
            'BOM': False,
            'non-numeric': []
        }
    },
    'filter': {
        'input': 'input_filename',
        'filters': [
            {
                'key': 'field',
                'op': '=',
                'value': 123
            }
        ],
        'output': {
            'name': 'output_filename',
            'BOM': False,
            'non-numeric': []
        }
    },
    'split': {
        'input': 'input_filename',
        'output': {
            'prefix': 'output_filename_prefix',
            'BOM': False,
            'non-numeric': []
        },
        'key': 'key_field'
    }
}
```

对于输出*output*配置，如果需要输出*BOM*格式，请把*BOM*设置为*True*；若有一些字段需要表达为非数字类字段，以便于在Excel中打开处理的话，请在*non-numeric*中设置需要处理的相关字段。

## ImageFileElf

Image文件精灵用于日常对图片类文件的处理应用。相关方法如下：

* **to_favicon**：把图片转化为favicon；对应的配置设定为*favicon*。
* **splice**：将*images*中的文件拼接为一张图片；对应的配置设定为*splice*。
* **watermark**：在指定的*x*、*y*坐标中增加水印文字；对应的配置设定为*watermark*。
* **qrcode**：将*input*的字符串生成二维码；对应的配置设定为*qrcode*。
* **decode_qrcode**：将*input*的二维码图片解析成字符串，并返回；对应的配置设定为*dqrcode*。
* **to_base64**：将*input*的图片转化为base64字符串，并返回；对应的配置设定为*2base64*。
* **from_base64**：将*input*的base64字符串转化为图片；对应的配置设定为*base64*。
* **resize**：将*input*的图片调整尺寸后输出到*output*；对应的配置设定为*resize*。
* **crop**：将*input*的图片按照*loaction*裁剪后输出到*output*；对应的配置设定为*crop*。当*mode*为**0**时，*location*为**left, top, right, bottom**构成的数组；当*mode*为**1**时，*location*为**left, top, width, right**构成的数组。

> 注：ImageFileElf.crop自v0.1.4版本开始支持

配置文件设定如下：

```json
{
    'favicon': {
        'size': -1,
        'input': 'input_filename'
    },
    'splice': {
        'output': 'output_filename',
        'images': [],
        'width': 700,
        'gap': 5,
        'mode': 'v'
    },
    'watermark': {
        'input': 'input_filename',
        'output': 'output_filename',
        'text': 'Krix.Tam',
        'color': 'FFFFFF',
        'font': 'arial.ttf',
        'font_size': 24,
        'x': 5,
        'y': 5,
        'alpha': 50
    },
    '2base64': {
        'input': 'input_filename',
        'css_format': False
    },
    'base64': {
        'input': 'base64 string',
        'output': 'output_filename'
    },
    'qrcode': {
        'input': 'string',
        'output': 'output_filename',
        'border': 2,
        'fill_color': "#000000",
        'back_color': "#FFFFFF"
    },
    'dqrcode': {
        'input': 'input_filename'
    },
    'resize': {
        'input': 'input_filename',
        'output': 'output_filename',
        'scale': False,
        'width': 28,
        'height': 28,
        'quality': 100,
        'dpi': 1200
    },
    'crop': {
        'input': 'input_filename',
        'output': 'output_filename',
        'mode': 0,
        'location': [0, 0, 5, 5]
    }
}
```

## 示例

```python
import os
from dfelf import CSVFileElf

df_elf = CSVFileElf()
config = {
    'base': {
        'name': os.path.join('sources', 'df1.csv'),
        'key': 'key'
    },
    'output': {
        'name': 'test_add.csv'
    },
    'tags': [
        {
            'name': os.path.join('sources', 'df3.csv'),
            'key': 'key',
            'fields': ['new_value'],
            'defaults': ['0.0']
        }
    ]
}
df_elf.add(**config)
```

下面的代码在v0.1.0版本开始，可以获得与上面代码同样的结果：

```python
import os
import pandas as pd
from dfelf import CSVFileElf

df_elf = CSVFileElf()
config = {
    'base': {
        'key': 'key'
    },
    'output': {
        'name': 'test_add.csv'
    },
    'tags': [
        {
            'name': os.path.join('sources', 'df3.csv'),
            'key': 'key',
            'fields': ['new_value'],
            'defaults': ['0.0']
        }
    ]
}
input_df = pd.read_csv(os.path.join('sources', 'df1.csv'), dtype=str)
df_elf.add(input_df, **config)
```

ImageFileElf.watermark在v0.1.3版本中，对*color*参数支持值为"**auto**"的设定，表示由程序自动选择水印颜色；颜色选择方法为水印所在位置(*x, y*)区域高频使用颜色的反转颜色。

ImageFileElf.splice自v0.1.3版本开始，支持水平拼接（设置*mode*参数为"**H**"或"**h**"，默认为垂直拼接，即*mode*参数为"**v**"或"**V**"）。
