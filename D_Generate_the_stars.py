# -*- coding: UTF-8 -*-
import bpy
import math
import csv
from . import ephem
import os


class classD():
    def mainD(): 
        # 路径绝对化，详见C文件注释
        currentPyFilePath = os.path.abspath(__file__) # 当前.py文件的路径
        parentPyFilePath = os.path.dirname(currentPyFilePath) # 当前.py文件所在的文件夹（整个插件所有文件都在这里）
        file004 = os.path.join(parentPyFilePath,'Database','004_Parameters obtained from UI panel.csv')
        file005 = os.path.join(parentPyFilePath,'Database','005_Pre-Operated index to generate code for Blender.csv')

        findex=open(file004,"r") # 打开存储用户输入的csv

        amount = 1 # 所需星数初始化为1
        row=0 # 在第row行进行的操作
        for line in csv.reader(findex):
            if row == 2: # csv里第第二行
                amount = int(line[1])    # 第2行第1位位所需星数
                break
            row += 1
        findex.close # 完成参数读取
        print(f'amount={amount}')

        count=0 # 读取行数计数
        fr=open(file005,"r") # 打开存储恒星参数映射的csv

        for starInfo in csv.reader(fr): # 对于csv文件的每一行
            if count >= amount:
                break
            if count == 0: # 第一行的数据是直接从星表生成的天狼星坐标，这里单独存起来后面使用
                beforeX=float(starInfo[1])
                beforeY=float(starInfo[2])
                beforeZ=float(starInfo[3])

            # 从表中的每一行读取参数
            x=float(starInfo[1])
            y=float(starInfo[2])
            z=float(starInfo[3])
            scale=float(starInfo[4])
            type=int(starInfo[5])

            # 在指定位置，创建指定scale的，指向某个标准星的实例集合
            bpy.ops.object.collection_instance_add(collection="starExample." + str(type), align='WORLD', location=(x,y,z))
            bpy.ops.transform.resize(value=(scale, scale, scale))
            # print(f'count={count}')
            count+=1

        ##################################
        # 此时生成的是一个(r,0,0)处为天球北天极，(0,0,-r)处为春分点，(0,0,r)处为秋分点的天球，这是某时刻某经度，在地球赤道上的观察结果
        # 要想获得用户输入的时间地点下，天球的状态，需要对现在的天球进行两次旋转

        # 读取用户输入
        findex=open(file004,"r") # 打开存储用户输入的csv
        row=0 # 在第row行进行的操作
        for line in csv.reader(findex):
            if row >= 3: # csv里第三行及以后不再读
                break
            elif row == 0: # csv第0行
                year    =int(line[0])
                month   =int(line[1])
                day     =int(line[2])
                hour    =float(line[3])
                minute  =float(line[4])
                second  =float(line[5])
            elif row == 1: # csv第1行
                lat = float(line[0])
                lon = float(line[1])
                alt = int(line[2])
            elif row == 2: # csv第2行
                r = int(line[0]) # 天球半径

            row+=1
        
        time = str(year) + '/' + str(month) + '/' + str(day) + ' ' + str(hour) + ':' + str(minute) + ':' + str(second)
        findex.close
        # 从用户输入更新本地信息
        local = ephem.Observer()
        local.lon = str(lon)
        local.lat = '0' # 这里纬度初始化为0，而不是用户的输入，见后面【2】处注释
        local.elevation = alt
        local.date = time

        # 计算从默认天球位置 转动到 某时刻某经线圈纬度0° 的真实天空 需要的旋转角度
        # 以全天第一亮星-天狼星-为计算靶标
        
        sirius = ephem.star('Sirius')           # 从ephem库内置的亮星星表创建天狼星对象，取名sirius
        # 这东西用不了，内置的Sirius赤经赤纬算出的地平坐标和方位角和真实情况对不上

        # sirius = ephem.FixedBody()
        # sirius._ra = '6:45:07'
        # sirius._dec = -16.723
        sirius.compute(local) # 基于local存储的本地位置，计算当前位置、高度、时间下的天狼星信息，主要是 sirius.az方位角，sirius.alt仰角                  
        print(f'At {local.date}, Sirius\'s azimuth and altitude at Lon.{local.lon/(2*math.pi)*360}° Lat.0° is {sirius.az},{sirius.alt}')

        theta = math.pi/2-sirius.alt            # pi/2-仰角 得到矢径和竖直轴正半轴夹角
        phi = -sirius.az                        # 方位角取相反数！！！！！！！！！！！
        ##### 因为地平坐标系方位角az正北（+x）向正东（-y）旋转为正，而球坐标系的方位角φ规定从+x轴向+y轴旋转为正，所以前者换算为后者时方位角要取反，不然生成的天体都是关于xoz平面对称后的

        # 球坐标转直角坐标
        # 通过ephem库直接计算出天狼星在此时此地的地平坐标系方位角、仰角；由于地面就是xoy平面，所以直接从球坐标转直角坐标即可

        print(f'before xyz is: ({beforeX},{beforeY},{beforeZ})')
        # 球坐标系转直角坐标系
        afterX = r * math.sin(theta) * math.cos(phi)
        afterY = r * math.sin(theta) * math.sin(phi)
        afterZ = r * math.cos(theta)
        print(f'after xyz is: ({afterX},{afterY},{afterZ})')

        # 注释【2】
        # 由于生成星星时就默认是在纬度0°的地球赤道（北天极卡在地平线正北方），此时计算坐标依然选在纬度0°，这就是开头初始化纬度为0的原因
        # 在两种状态之间，只有经度和时间发生了变化，因此天球只会产生绕极轴（即x轴）的转动，有afterX ≡ beforeX ≡ X
        # 接下来计算这个转动角度
        # Blender中，绕x轴转动的规定是：从+y转向+z方向，旋转角度为正，反之为负
        # 所以，保持视线看向-x方向，面对yoz平面，以+y为0°，逆时针转动为正，就规定了yoz平面直角坐标系下的任意角
        # 以(X,0,0)为原点，经过天狼星初始位置(X,beforeY,beforeZ)的射线，其与+y半轴的夹角 beforeDegree = arctan(beforeZ/beforeY) 
        # 以(X,0,0)为原点，经过天狼星终末位置(X,afterY,afterZ)的射线，其与+y半轴的夹角 afterDegree = arctan(afterZ/afterY) 

        beforeDegree = math.atan2(beforeZ,beforeY)
        afterDegree = math.atan2(afterZ,afterY)
        rotateXDegree = (afterDegree-beforeDegree) # 保留弧度制，这一步得到的就是当前时刻相对于最初生成的天球，绕x轴旋转的角度

        print(f'before degree = {beforeDegree}, after degree = {afterDegree}, rotateX = {rotateXDegree}')

        # 地球上纬度多高，北天极的仰角就是多高，因此这里直接使用当地纬度做为天球上仰的角度
        rotateYDegree =  float(lat)/360 * math.pi * 2      # “天球上仰”指天球在绕x轴旋转所需时角后，绕y轴进行的转动,角度制转弧度制

        # 接下来根据计算，进行场景中所有物体的旋转
        bpy.ops.view3d.snap_cursor_to_center # 游标回归世界原点
        # 这一步 bpy.context.scene.cursor.location = (0.0, 0.0, 0.0) 也可以，但是不好，原因是：
        # cursor是有三轴方向的，类似一个空物体，前者的方法可以让cursor回世界原点的同时，三轴对齐xyz轴；然而后者只能把cursor平移到世界原点，仍保留之前的三轴倾斜
        # 可以在倾斜视角下把cursor随便拖走，再执行两种命令尝试一下

        bpy.context.scene.tool_settings.transform_pivot_point = 'CURSOR' # 把变换轴心点改为cursor  变换轴心点：用于旋转/缩放的轴心中心

        # 全选SPAS集合下的所有物体（刚创建的所有星星）
        for obj in bpy.data.collections['SPAS'].all_objects:
            obj.select_set(True)

        bpy.ops.transform.rotate(value = -rotateXDegree, orient_axis='X') # 绕X轴旋转，角度为计算出来的，当前时刻相对于默认状态的天球旋转时角
        bpy.ops.transform.rotate(value = rotateYDegree, orient_axis='Y') # 绕Y轴旋转，角度为所在纬度

        bpy.context.scene.tool_settings.transform_pivot_point = 'MEDIAN_POINT' # 把变换轴心点改回质心点
        bpy.ops.object.select_all(action='DESELECT') # 取消全选所有物体

        print('Generated and rotated all stars.\n')
        fr.close