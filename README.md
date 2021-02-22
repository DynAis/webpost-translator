# Typora - Hexo文章转换器

用于在向个人网站上传md文件时, 将个人使用的Typora编辑器中和Hexo不兼容的部分互相转换, 节省人工修改的力气



## Usage

1. 待转换的Markdown文件命名格式必须遵守`{类型标识符}-{内容标识符}-{文章标题}.md`的格式规范书写

2. 放置所有待转换文件至脚本`normalize.py`根目录下
3. 双击运行脚本`normalize.py`
4. 输出文件将以`{文章标题.md}`的格式输出



## To Do List

- 制作GUI界面

- 根据文章内容完成元数据中`tags` `categories` `keywords`的自动填充

- 加入快速选择文章缩略图功能

- 加入LaTex公式帮助功能

  