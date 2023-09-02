"""
    This is a Blender project developed by B-MH and WannaR. Please do not reprint, copy, or resell without permission.
    This project, written in Python, designed in English (though both of us are Chinese) aims to provide Blender users with the most scientific and 
precision simulation of celestial objects as possible.
    It has been made possible through published resources like the SAO Star Catalog, Planetary and Lunar 3d-model from NASA, as well as open-source Python 
package "pyephem" and algorithms. We have noticed that there are already excellent astronomical computing and simulating programs such as Stellarium, 
but it seems that no one has ported them to Blender, making it difficult to meet the need to obtain real sky backgrounds. We believe that such needs are 
always existing, for instance, the movie special effect of Titanic has been pointed out by astronomer Neil deGrasse Tyson for applying wrong background 
starry sky; moreover, for users performing some night scenes, aviation, and Low Earth Orbit projects, using correct and accurate star background is always 
the icing on the cake.
    This project is planned to be released in an open-source format, and the code structure and implementation methods of the project may be explained 
in the form of documents or videos later. We sincerely appreciate every user of the add-on, and developer who has proposed optimization ideas for the code 
of this add-on.
    This is the first version of the add-on, we believe its functionality and inclusion of celestial bodies are limited, there are also some possibilities 
for code optimization. So in the future, we are continually developing this project according to the increasing needs and release new versions. Stay tuned!
    Copyright B-MH and Wannar, all rights reserved.
"""
# -*- coding: UTF-8 -*-
import os
import sys
import bpy

# 逐个导入子模块
from . import A_Generate_UI

bl_info = {
    "name" : "Scientific and Precision Astronomical System", 
    "author" : "B-MH & WannaR",
    "description" : "To provide Blender users with the most scientific and presicion simulation of celestial objects as possible.",
    "blender" : (3, 2, 0),
    "version" : (0, 1, 0),
    "location" : "",
    "warning" : "Please ensure that you have thoroughly read the document's \"Usage Guidelines\" section before using the add-on",
    "category" : "Generic",
    "doc_url" : "https://github.com/Yuxiza/Blender-CelestialSimulator", # 文档链接
    "traker_url" : "https://github.com/Yuxiza/Blender-CelestialSimulator/issues", #  反馈问题链接
}

# 除了A因为有参数的读入读出需要在此注册，其他类没这个必要
def register():
    print("SPAS started successfully.")
    currentPyFilePath = os.path.abspath(__file__) # 当前.py文件的路径
    parentPyFilePath = os.path.dirname(currentPyFilePath) # 当前.py文件所在的文件夹（整个插件所有文件都在这）
    sys.path.append(parentPyFilePath) # 当前文件夹添加入Blender Python的系统路径

    print(f'Current absolute path is: {os.path.abspath(__file__)}') # 检查当前路径，后续用作路径绝对化
    # print(f'sys.path is: {sys.path}') # 检查Blender Python的系统路径
    print('Parent path has been appended to sys.path\n')
    A_Generate_UI.register()
    ...

def unregister():
    A_Generate_UI.unregister()
    print("SPAS terminated successfully.")
    ...

# 在调试时激活
if __name__ == "__main__":
    register()