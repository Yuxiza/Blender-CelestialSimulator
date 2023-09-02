# -*- coding: UTF-8 -*-
import math
import csv
import os

# 这里声明囊括一切的 calssC 和 mainC 纯属只是为了套用register_class函数格式，没啥其他用处
class classC():
    def mainC():
        # 从“003_Sorted SAO Star Catalog (sort accroding to the star's visual magnitude).txt” 中提取恒星参数：赤经赤纬、视星等、光谱类型，分别映射成Blender参数：直角坐标、scale因子、材质名称

        # Blender默认运行路径是blender.exe所在的路径，在其下无法使用这些相对路径，在Blender中读取会报错
        # 路径绝对化
        currentPyFilePath = os.path.abspath(__file__) # 当前.py文件的路径
        parentPyFilePath = os.path.dirname(currentPyFilePath) # 当前.py文件所在的文件夹（整个插件所有文件都在这里）
        file003 = os.path.join(parentPyFilePath,'Database','003_Sorted SAO Star Catalog (sort accroding to the star\'s visual magnitude).txt')
        file004 = os.path.join(parentPyFilePath,'Database','004_Parameters obtained from UI panel.csv')
        file005 = os.path.join(parentPyFilePath,'Database','005_Pre-Operated index to generate code for Blender.csv')
        findex=open(file004,"r") # 打开存储用户输入的csv
        fr=open(file003,"r") # 打开排序后的星表
        fw=open(file005,"w",newline='') # 打开存储恒星参数映射的csv
        
        r=0 # 天球半径初始化为0
        amount = 1 # 所需星数初始化为1
        row=0 # 在第row行进行的操作
        for line in csv.reader(findex):
            if row == 2: # csv里第第二行
                r = int(line[0])         # 第2行第0位为天球半径
                amount = int(line[1])    # 第2行第1位位所需星数
                break
            row += 1
        findex.close # 完成参数读取
        
        count = 0 # 计数已转换完成多少星的参数
        for line in fr:

            # 获取SAO编号
            SAO=line[0:6].strip(" ")

            # 赤道坐标系转直角坐标系
            # 规定Blender中，xoy为地平面，+x所指为正北方，+y所指为正西方，+z所指为正上方的天顶

            # 关于赤纬
            # 假设r是天球半径，真实情况中，在地理坐标系纬度0°（即地球赤道上）观察时，北天极在地平线正北方位置(r,0,0)，天赤道平面yoz垂直于地平面xoy
            # 如果直接把赤经赤纬做球坐标的方位角、仰角，计算直角坐标的xyz，就相当于默认xoy为天赤道平面（这个“默认”体现在球坐标转直角坐标的数学公式中，z=r*cos(theta)这个方程就在表明z是竖直轴，即极轴）
            # 这样的话，赤纬+90°的北天极在天顶(0,0,r)，这不符合真实情况，所以需要让这样的产生天球绕y轴，从+z向+x方向转九十度，把北天极从(0,0,r)转到(r,0,0)去

            # 关于赤经
            # 本来想规定赤经，但是生成结果和我规定的不一样......我也懒得推算了，无所谓最初子午圈在哪个平面，反正最终会根据 最初生成的天狼星坐标 → 某时某地的天狼星坐标 这个变化反推天球旋转
            # 啊当然了，让它自由发挥后，0h子午圈会经过 +x半轴 -z半轴 -x半轴
            # 如果你没看懂上面我在说什么，这里列几个特殊点，以(x,y,z)坐标表示：(r,0,0)处为天球北天极，(0,0,-r)处为春分点，(0,0,r)处为秋分点

            # 观察SAO星表可以发现，表中的弧度制赤经赤纬实际上记载的是方位角和俯仰角，然而球坐标(r,θ,φ)的φ指方位角，θ指“原点指向目标的矢径”和“垂直轴正半轴”的夹角
            # 所以，赤经取值范围[0,2π]，这很好，可以直接作为方位角φ；赤纬取值范围[-π/2,π/2]，需要 π/2-赤纬 才得到夹角θ

            phi=float(line[7:16].strip(" "))            # 从弧度制赤经直接得到方位角φ
            theta=math.pi/2-float(line[18:28].strip(" ")) # π/2-赤纬 得到夹角θ

            # 依照公式换系
            x = r * math.sin(theta) * math.cos(phi)
            y = r * math.sin(theta) * math.sin(phi)
            z = r * math.cos(theta)

            # 按上述分析，需要让坐标系绕y轴，从+z向+x方向转九十度，所以原本的点 D(x0,y0,z0) 会变成新的点 D'(x,y,z)=(z0,y0,-x0)
            temp=x
            x=z
            y=y
            z=-temp
            # 坐标系旋转完成

            # 建立scale因子映射
            # 我去blender里试了一下，在天空纹理黄昏的情况下，在1000m远的地方放置一颗大小1m的棱角球，自发光强度5，白色
            # 大概缩放=5倍的相当于-2等星，缩放=0.1倍相当于12等星（大气纯净时勉强还能看见），这样才能看出一些差异，不然大家都一样大
            # 所以把-2等到12等映射到5到0.1，但是并非线性映射，因为星等到亮度是个指数函数,底数约为2.512
            # 所以取指数函数在y轴缩放并且平移，设缩放因子a，平移因子b，则应该有方程 scale=a*2.512**(12-VMag)+b

            ### 不过取2.512做为指数函数底数，一些极亮的星星如天狼星，角面积会比一般的亮星大数十倍上百倍
            ### 为了不让它这么突兀，这里把底数改成1.5，即scale=a*1.5**(12-VMag)+b

            # 所以取指数函数在y轴缩放并且平移，设缩放因子a，平移因子b，则应该有方程 scale=a*1.5**(12-VMag)+b
            # 当视星等VMag取12，方程得0.1；当VMag=-2，方程得5
            # 解得
            a=(5-0.1)/(1.5**14-1.5**0)
            b=0.1-a
            VMag=float(line[30:34].strip(" "))
            scale=a*1.5**(12-VMag)+b


            # 建立光谱类型到实例子级的映射, 从1~9对应颜色蓝-白-红的变化
            # 一共有9种情况，本可以用switch case语句，但是这个语句知道Python 3.10才出现，为了兼容低版本，还是用 if elif else 了
            if line[35]=="w":
                material=1
            elif line[35]=="O":
                material=2
            elif line[35]=="B":
                material=3
            elif line[35]=="A":
                material=4
            elif line[35]=="F":
                material=5
            elif line[35]=="G":
                material=6
            elif line[35]=="K":
                material=7
            elif line[35]=="S":
                material=8
            elif line[35]=="M":
                material=9
            else:
                material=5 # 避免星表里有我没发现的特殊情况，默认为F类白色恒星

            # 合并结果,格式化输出，其中xyz坐标右对齐宽度15，保留10位小数，中间空格；scale右对齐宽度12，保留10位小数，空一格输出material
            csv.writer(fw).writerow ([SAO,x,y,z,scale,material])

            count += 1
            if count >= amount+10: #如果已经转换完了所需数量的恒星的参数，+10是怕哪里数量没考虑周到出错
                break # 就停止再算，不必每次都通篇计算全部26万颗星的数据

        
        fr.close
        fw.close

        print('Finished the converting.\n')
        return None

# def register():
#     from bpy.utils import register_class
#     register_class(classC)

# def unregister():
#     from bpy.utils import unregister_class
#     unregister_class(classC)