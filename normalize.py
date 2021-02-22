#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import time

try:
    import regex as re
except ImportError:
    os.system('pip install regex')
    import regex as re

# 读取当前根目录下正确命名的笔记文件, 生成列表
file_list = os.listdir("./")
note_list = []
for file in file_list:
    if re.match("[NTPJ]{2}-.*-.*.md$", file):
        note_list.append(file)
# print(note_list)

# 对每一个文件进行一次操作
for note in note_list:
    with open(note, "r+", encoding="utf8") as md:
        tex = md.readlines()

    # In[2]:


    # code_flag指示当前语句是否处于code block内
    code_flag = False
    # list_flag指示当前语句是否处于list内(>, -, 1.)
    list_flag = False

    for i in range(len(tex)):
        # 检测code block
        if tex[i].startswith("```"):
            code_flag = not code_flag
        # 如果是code block则不进行任何处理
        if code_flag:
            continue

        # 删除空行
        tex[i] = tex[i].lstrip()
        # 小写规范化
        str = tex[i].lower()
        # 检测list, 如果是list则不进行任何处理, 然后在推出list是加上空行
        if str.startswith(">") or str.startswith("-") or re.match("\d.", str) != None:
            list_flag = True
            continue
        elif list_flag and i - 1 > 0:
            list_flag = False
            tex[i - 1] += "\n"

        # 检测替换[toc]标签
        if str.find("[toc]") >= 0:
            tex[i] = tex[i].lower().replace("[toc]", "<!-- toc -->")
        # 自动设置空行
        br_flag = False
        if str.startswith("#####") and not br_flag:
            br_flag = True
        if str.startswith("####") and not br_flag:
            br_flag = True
        if str.startswith("###") and not br_flag and i - 1 > 0:
            tex[i - 1] += '<br>\n'
            br_flag = True
        if str.startswith("##") and not br_flag and i - 1 > 0:
            tex[i - 1] += '<br>\n<br>\n'
            br_flag = True
        if str.startswith("#") and not br_flag and i - 1 > 0:
            tex[i - 1] += '<br>\n<br>\n'
            br_flag = True
        # 转换图片至fancybox
        if re.search("<img.+/>", str):
            # 获取图片url
            img_url = re.search("(?<=src=\")(.+?)(?=\")", str).group()
            img_url = img_url + "?x-oss-process=image/resize,h_2000/quality,q_90"
            # 替换图片url
            fancybox = "{%% image fancybox center clear group:default %s " " %%}" % (img_url)
            tex[i] = re.sub("<img.+/>", fancybox, str)
        elif re.search("!\[.*\]\(.*\)", str):
            # 获取图片url
            img_url = re.search("(?<=!\[.*\]\().*(?=\))", str).group()
            img_url = img_url + "?x-oss-process=image/resize,h_2000/quality,q_90"
            # 替换图片url
            fancybox = "{%% image fancybox center clear group:default %s " " %%}" % (img_url)
            tex[i] = re.sub("!\[.*\]\(.*\)", fancybox, str)


        # In[3]:


        # 私有符号解释器


        # In[4]:


        # 根据head_config.md文件生成头部结构
        with open(".\config\head_config.md", "r", encoding="utf8") as md:
            head = md.read()
        #         print(head)
        # 生成date标签
        local_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        head = re.sub("{{ date }}", local_time, head)
        # 生成title标签
        title = re.search("(?<=[NTPJ]{2}-.*-).*(?=.md$)", note).group()
        head = re.sub("{{ title }}", title, head)
        #     print(head)


        # In[5]:


        # 自动生成archive
        # 自动生成tags
        # 自动生成keywords


        # In[6]:


        # 文件输出
        out = [head] + tex
        with open(title + ".md", "w+", encoding="utf8") as md:
            for str in out:
                md.write(str)
