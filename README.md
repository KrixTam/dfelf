# dfelf

由于日常工作需要（有时候还有写blog的需要），总是要处理一些数据文件，很多繁琐的工作希望可以有一个文件精灵来帮我处理，所以就把过去写的小工具重新整理下，形成“数据文件精灵”（“dfelf”）。

“dfelf”为“Data File Elf”的缩写。

因为日常总是需要处理如下文件：
* CVS
* PDF
* 图片

所以数据文件精灵初步设计可以支持以上三类文件的日常处理需要。

## PDFFileElf

PDF文件精灵用于日常对PDF的处理应用。

配置文件设定如下：

> {
> 
>     'name': 'PDFFileElf',
> 
>     'default': {
> 
>         'input': 'input_filename',
> 
>         'output': 'output_filename',
> 
>         'concat': []
> 
>     },
> 
>     'schema': {
> 
>         'type': 'object',
> 
>         'properties': {
> 
>             'input': {'type': 'string'},
> 
>             'output': {'type': 'string'},
> 
>             'concat': {
> 
>                 'type': 'array',
> 
>                 'items': {'type': 'number'}
>             }
> 
>         }
> 
>     }
> 
> }

