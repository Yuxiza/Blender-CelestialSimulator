# -*- coding: UTF-8 -*-
import bpy
import os
import csv
import math
from . import ephem as ep

# 通过从预先构建的模型-节点库（3DModelAppend.blend）追加所需天体，实现对太阳，月亮，除地球外的七大行星，冥王星的创建
# 文件中包含天体的模型，材质节点，以及用于对齐极轴的几何节点，追加天体时都会一并进来

# 天体模型路径
# APPEND_BLEND = "./3DModelScale.blend"

# 关于计算天体生成位置，视直径大小，极轴朝向等等的类
class classE:
    # 静态数据库
    planet_list = ["moon","mercury","venus","mars","jupiter","saturn","uranus","neptune","pluto"] # 提供的天体列表
        # 这里记录了地球J2000.0纪元下，各天体的极轴（自转轴，在blender里使用天体的局部+z轴）朝向
        # 获取方法是，在Stellarium直接设置位置为该天体，获取其北天极点的恒星，即“该天体视角下的北极星”
        # 取此北极星在 “地球赤道坐标系J2000.0纪元” 的赤经赤纬，而不是在 “该天体赤道坐标系” 的赤经赤纬，不然只能是赤经任意，赤纬90°

    polar_axis = {"sun":['19:02:55',63.9],
                  "moon":['17:54:29',67.7],
                  "mercury":['18:44:10',61.5],
                  "venus":['18:10:56',67.2],
                  "mars":['21:10:00',53.0],
                  "jupiter":['17:51:42',64.4],
                  "saturn":['2:45:16',83.6],
                  "uranus":['17:09:19',-15.3],
                  "neptune":["19:57:30",43.0],
                  "pluto":["08:52:21",-6.3]} 

    bodies = {}
    bodies["sun"] = ep.Sun()
    bodies["moon"] = ep.Moon()
    bodies["mercury"] = ep.Mercury()
    bodies["venus"] = ep.Venus()
    bodies["mars"] = ep.Mars()
    bodies["jupiter"] = ep.Jupiter()
    bodies["saturn"] = ep.Saturn()
    bodies["uranus"] = ep.Uranus()
    bodies["neptune"] = ep.Neptune()
    bodies["pluto"] = ep.Pluto()

    # 本地信息和天球半径声明为全局变量
    local = ep.Observer()
    r=0
    alt=0

    def __init__(self):
        
        # 路径绝对化，详见C文件注释
        currentPyFilePath = os.path.abspath(__file__) # 当前.py文件的路径
        parentPyFilePath = os.path.dirname(currentPyFilePath) # 当前.py文件所在的文件夹（整个插件所有文件都在这里）
        file004 = os.path.join(parentPyFilePath,'Database','004_Parameters obtained from UI panel.csv')
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
                self.r = int(line[0]) # 天球半径

            row+=1
        
        time = str(year) + '/' + str(month) + '/' + str(day) + ' ' + str(hour) + ':' + str(minute) + ':' + str(second)
        findex.close
        # 从用户输入更新本地信息
        self.local.lon = str(lon)
        self.local.lat = str(lat)
        self.local.elevation = alt
        self.local.date = time
        print('Updated local information.')


    # 从文件中追加选定的天体pl
    def append_bodies(self,pl:str):
        '''
        pl from ["sun","moon","mercury","venus","mars","jupiter","saturn","uranus","neptune","pluto"]
        '''
        # 追加前选定 SPAS 为活动集合
        bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection.children['SPAS']
        # file_path = APPEND_BLEND
        # inner_path = "Object"
        # bpy.ops.wm.append(filepath=os.path.join(file_path,inner_path,pl),directory=os.path.join(file_path,inner_path), filename=pl)
        
        # 参考：https://blender.stackexchange.com/questions/38060/
        # blendfile = "3DModelAppend.blend" # 路径绝对化，详见C文件注释

        currentPyFilePath = os.path.abspath(__file__) # 当前.py文件的路径
        parentPyFilePath = os.path.dirname(currentPyFilePath) # 当前.py文件所在的文件夹（整个插件所有文件都在这里）
        blendfile = os.path.join(parentPyFilePath,'3DModelAppend.blend')
        
        section   = "\\Object\\"
        object    = pl

        filepath  = blendfile + section + object
        directory = blendfile + section
        filename  = object

        bpy.ops.wm.append(
            filepath=filepath, 
            filename=filename,
            directory=directory)
        
        print(f'Appended {pl}')

    # 追加的天体关联到SPAS集合（这一步不必，追加之前选中SPAS为活动集合，追加的东西自然会进去）
    # def link_collection(self,pl:str):
    #     '''
    #     pl from ["sun","moon","mercury","venus","mars","jupiter","saturn","uranus","neptune","pluto"]
    #     '''
    #     self.link_collection(pl)
    #     bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection.children['SPAS']
    #     bpy.data.collections["SPAS"].objects.link(bpy.context.active_object) 

    # 移动追加的天体pl到指定位置，并且按视直径进行缩放
    def adjust_bodies(self,pl:str):
        '''
        pl from ["sun","moon","mercury","venus","mars","jupiter","saturn","uranus","neptune","pluto"]
        '''
        # 基于某时某地，计算天体相关信息
        print(f'{self.local.lat},{self.local.lon},UTC+0: {self.local.date}')
        self.bodies[pl].compute(self.local)
        print('%s %f %f' %(pl,self.bodies[pl].az,self.bodies[pl].alt))
        print(f'Calculated {pl}\'s information.')

        # 考虑天体的遮挡关系，不同类的天体生成在不同半径R的球面上，通过用户输入的天球半径r乘以一定比例算得

        if pl == "moon":    # 月亮遮挡一切，放在最小的半径上
            R = 0.94 * self.r
        elif pl == "sun":   # 除了地球内层行星有掩凌日现象时，会出现在太阳前面，其余情况下，如果出现在天球同一位置，都会被太阳挡住；外层行星只有被挡住的可能
            R = 0.96 * self.r    # 所以取太阳所在球面半径小于行星的
        else:
            R = 0.98 * self.r

        # 修改新建的天体位置，参考：https://blender.stackexchange.com/questions/120026/
        # 方位角取相反数！！！！！！！！！！！
        ##### 因为地平坐标系方位角az正北（+x）向正东（-y）旋转为正，而球坐标系的方位角φ规定从+x轴向+y轴旋转为正，所以前者换算为后者时方位角要取反，不然生成的天体都是关于xoz平面对称后的
        x = R * math.sin(math.pi/2-self.bodies[pl].alt+0.0) * math.cos(-self.bodies[pl].az+0.0)
        y = R * math.sin(math.pi/2-self.bodies[pl].alt+0.0) * math.sin(-self.bodies[pl].az+0.0)
        z = R * math.cos(math.pi/2-self.bodies[pl].alt+0.0)                                   
        bpy.data.objects[pl].location = (x,y,z)

        # 按视直径缩放天体
        # self.bodies[pl].size 返回以角秒（arcsec）为单位的视直径，角秒换算成弧度，弧度乘以该天体所在球面半径，就能得到该天体在该球面上占用的弧长
        # 由于视直径（单位arcsec）很小，弧长可以近似等于视直径（单位meter），3DModelScale.blend 中，所有天体直径已经初始化为 1m ，所以视直径是多少就直接缩放多少倍即可
        # 角秒换算弧度，一圈共 360degrees * 3600 arcsec/degree ，共 2π 弧度
        rad = self.bodies[pl].size / (360 * 3600) * (2 * math.pi)
        scale = rad * R # 计算视直径（单位meter）
        # 但是这样生成的虽然真实，看起来却太小了，让视直径扩大一些吧
        if pl == 'sun' or pl == 'moon':
            scale *= 2
        else:
            scale *= 5
        bpy.data.objects[pl].scale = (scale,scale,scale) # 按视直径放大物体

        print(f'Adjusted {pl}\'s location and size.')


        # 通过在一定位置添加一定亮度、半径的灯，来模拟太阳系除了太阳的其他天体被太阳照亮的效果

        if pl == 'sun':
            pass # 太阳不需要再额外添加灯来模拟被照亮
        else:

            sunIndependent = ep.Sun()            # 独立于生成太阳时创建的self.bodies['sun']实例，在这里单独创建一个太阳的实例
            sunIndependent.compute(self.local)   # 这样无论用户是否选择生成太阳，在其他计算需要获取太阳数据时，都不会因为太阳实例未定义而报错

            # 不是太阳的情况，先算出太阳和该天体pl各自的直角坐标，其中天体pl的xyz，上文已给出，下面这是太阳的
            # 方位角取相反数！！！！！！！！！！！原因见前文注释，不再赘述
            x_sun = R * math.sin(math.pi/2-sunIndependent.alt+0.0) * math.cos(-sunIndependent.az+0.0)
            y_sun = R * math.sin(math.pi/2-sunIndependent.alt+0.0) * math.sin(-sunIndependent.az+0.0)
            z_sun = R * math.cos(math.pi/2-sunIndependent.alt+0.0)

            vector = [x_sun-x, y_sun-y, z_sun-z] # 此为天体pl指向太阳的的向量AS
            # 在Blender试验发现，在太阳和天体连线上，距离天体2a的位置，放一个5kW的点光，半径1.2a，a为天体视直径（单位meter），刚好能模拟出天体pl被阳光照亮一半的效果
            vector_length = math.sqrt(vector[0]*vector[0] + vector[1]*vector[1] + vector[2]*vector[2]) # 向量模长|AS|
            vector[0] /= vector_length # 原向量除以模长，取单位向量AS/|AS|=ASe，方向仍为天体pl指向太阳
            vector[1] /= vector_length
            vector[2] /= vector_length

            vector[0] *= 2*scale # 向量长度改为2a，这里a=scale，点光源距离天体pl为2a，ASe*2a=AP，此AP向量就是天体指向点光源的向量
            vector[1] *= 2*scale
            vector[2] *= 2*scale

            x_light = vector[0] + x # 天体→点光源的向量AP，加上原点→天体的矢径OA，得到原点→点光源矢径OP
            y_light = vector[1] + y
            z_light = vector[2] + z
            
            # 创建点光，移动到矢径OP所指位置，
            # scale是直径，所以除以2得到半径，乘4是因为blender中，radius这项数据要填写meter数除以4的结果，如radius=4，实际半径为1m
            if pl == 'moon':
                bpy.ops.object.light_add(type='POINT', radius=4*1.2*scale/2, location=(x_light, y_light, z_light))
                bpy.context.object.data.energy = 100000 # 月球亮度调定6000W，调整半径为1.2倍天体pl半径，刚好能照亮一半
            elif pl == 'mercury' or pl == 'venus':
                bpy.ops.object.light_add(type='POINT', radius=4*1.2*scale/2, location=(x_light, y_light, z_light))
                bpy.context.object.data.energy = 500000   # 内行星亮度调定3000W，调整半径为1.2倍天体pl半径，刚好能照亮一半
            else:
                bpy.ops.object.light_add(type='POINT', radius=4*4*scale/2, location=(x_light, y_light, z_light))
                bpy.context.object.data.energy = 1000   # 外行星亮度调定3000W，调整半径为4倍天体pl半径，照亮绝大部分星体
            bpy.context.object.name= pl + '\'s sunlight' # 是谁的就重命名成什么的日光

        
    
    ##########
    # 核心代码
    ##########
    """
    以下赤经赤纬均基于地球赤道坐标系J2000.0纪元讨论
    为还原天体pl真实自转轴倾角（这一点在土星的的周年季节变化有明显体现），需要让每个天体的极轴（自转轴，天体模型的局部+z轴）对齐它自己的北天极，亦即上面polar_axis记载的赤经赤纬
    由于各大天体pl生成时，就是按照当地当时的地平坐标系（方位角，仰角）确定的坐标，这里也要让其极轴对齐当时当地它自己的北极点方向，或者说，“对齐当时当地该pl天体的北极星”
    这需要获取该“北极星”当时当地的位置，但是ephem并未预置所有恒星的相关数据，因此这里手动添加这些 “北天极” 为一个虚拟星-“北极星”，这一步通过FixedBody函数实现，提供赤经赤纬即可
    然后通过ephem计算出这“虚拟北极星”在当时当地的方位角仰角，进一步转换成直角坐标，如ArtificialPolar -> P(x0,y0,z0)
    则，从地心(0,0,0)指向该“虚拟北极星”的向量OP=(x0,y0,z0)，就可以近似代替该pl天体质心指向“虚拟北极星”的向量（由于地球和太阳系其他天体pl的距离线度远远小于到恒星的距离）
    进一步地，应该使pl天体+z轴方向向量平行于此OP向量，这一步通过“对齐欧拉至矢量”几何节点实现
    """
    
    # 对齐天体pl的极轴
    def calibrate_axis(self,pl:str):
        '''
        Assuming the target is in the SPAS collection
        '''
        # 读入北天极赤经赤纬，生成虚拟北极星
        polar_point = ep.FixedBody()
        polar_point._ra = self.polar_axis[pl][0]
        polar_point._dec = self.polar_axis[pl][1]
        polar_point.compute(self.local)

        # 对于月球，需要对齐两个轴，+z轴对准北极星，+x轴对准地球，实现潮汐锁定
        if pl == "moon":
            
            # 对齐极轴，这里取球坐标系r=1，即取极轴方向向量的单位向量
            # 地平球坐标系转地平空间直角坐标系，计算 “虚拟北极星” 坐标
            # 方位角取相反数！！！！！！！！！！！原因见前文注释，不再赘述
            bpy.data.node_groups[pl].nodes["Align Euler to Vector"].inputs[2].default_value[0] = math.sin(polar_point.alt+0.0) * math.cos(-polar_point.az+0.0) # x
            bpy.data.node_groups[pl].nodes["Align Euler to Vector"].inputs[2].default_value[1] = math.sin(polar_point.alt+0.0) * math.sin(-polar_point.az+0.0) # y
            bpy.data.node_groups[pl].nodes["Align Euler to Vector"].inputs[2].default_value[2] = math.cos(polar_point.alt+0.0)                                # z
            
            # 对齐+x轴，使月球正面朝向地球，潮汐锁定
            # 从月球在地平坐标系的球坐标，转换为月球的空间直角坐标
            # 这里取球坐标系r=-1，即取极轴方向向量的反向单位向量，因为月球的位置向量是地球指向月球，但是+x轴朝向是月球指向地球
            # 方位角取相反数！！！！！！！！！！！原因见前文注释，不再赘述
            bpy.data.node_groups[pl].nodes["Align Euler to Vector.001"].inputs[2].default_value[0] = -1 * math.sin(math.pi/2-self.bodies[pl].alt+0.0) * math.cos(-self.bodies[pl].az+0.0) # x
            bpy.data.node_groups[pl].nodes["Align Euler to Vector.001"].inputs[2].default_value[1] = -1 * math.sin(math.pi/2-self.bodies[pl].alt+0.0) * math.sin(-self.bodies[pl].az+0.0) # y
            bpy.data.node_groups[pl].nodes["Align Euler to Vector.001"].inputs[2].default_value[2] = -1 * math.cos(math.pi/2-self.bodies[pl].alt+0.0)                                   # z
        
        else:
            # 和月球对齐极轴同理
            # 方位角取相反数！！！！！！！！！！！原因见前文注释，不再赘述
            bpy.data.node_groups[pl].nodes["Align Euler to Vector"].inputs[2].default_value[0] = math.sin(polar_point.alt+0.0) * math.cos(-polar_point.az+0.0) # x
            bpy.data.node_groups[pl].nodes["Align Euler to Vector"].inputs[2].default_value[1] = math.sin(polar_point.alt+0.0) * math.sin(-polar_point.az+0.0) # y
            bpy.data.node_groups[pl].nodes["Align Euler to Vector"].inputs[2].default_value[2] = math.cos(polar_point.alt+0.0)                                # z

        print(f'Calibrated {pl}\'s polar axis.')

# 这些大约的确是没用了，就算用户不输入，下面的csv也会从blender的property里读取我设的默认值
# local = ep.Observer()
# local.lat = '39.904214'
# local.lon = '116.407413'
# local.date = "2023/7/30 20:43:40"

    # 这里记录了生成一个天体pl所需的全流程所有函数
    def generate_bodies(self,pl):
        self.__init__(classE)
        self.append_bodies(classE,pl) # 从 3DModelScale.blend 追加所需天体pl
        self.adjust_bodies(classE,pl) # 调整刚追加的天体pl的位置，大小
        self.calibrate_axis(classE,pl) # 对齐天体pl的极轴，潮汐锁定（仅月球）
        print(f'{pl} added successfully.\n')


        
    """
    天体模型来源:
    https://solarsystem.nasa.gov/resources/2352/sun-3d-model/
    https://solarsystem.nasa.gov/resources/2369/mercury-3d-model/
    https://solarsystem.nasa.gov/resources/2343/venus-3d-model/
    https://solarsystem.nasa.gov/resources/2372/mars-3d-model/
    https://solarsystem.nasa.gov/resources/2375/jupiter-3d-model/
    https://solarsystem.nasa.gov/resources/2355/saturn-3d-model/
    https://solarsystem.nasa.gov/resources/2344/uranus-3d-model/
    https://solarsystem.nasa.gov/resources/2364/neptune-3d-model/
    https://solarsystem.nasa.gov/resources/2357/pluto-3d-model/
    https://open3dmodel.com/3d-models/moon-from-nasa_595918.html
    """

    # 追加 3DModelAppend.blend 中的 世界材质-天空纹理
    def append_skyTexture(self):
        # 参考：https://blender.stackexchange.com/questions/38060/
        # blendfile = "3DModelAppend.blend" # 路径绝对化，详见C文件注释
        currentPyFilePath = os.path.abspath(__file__) # 当前.py文件的路径
        parentPyFilePath = os.path.dirname(currentPyFilePath) # 当前.py文件所在的文件夹（整个插件所有文件都在这里）
        blendfile = os.path.join(parentPyFilePath,'3DModelAppend.blend')

        section   = "\\World\\"
        object    = 'World Sky Texture'
        filepath  = blendfile + section + object
        directory = blendfile + section
        filename  = object
        bpy.ops.wm.append(
            filepath=filepath, 
            filename=filename,
            directory=directory)
        
        # 刚追加进来的世界材质做为当前世界环境，参考：https://blenderartists.org/t/how-to-set-a-worlds-shader-to-the-world-with-python-please/636247/3
        bpy.context.scene.world = bpy.data.worlds['World Sky Texture']

        sunIndependent = ep.Sun()            # 独立于生成太阳时创建的self.bodies['sun']实例，在这里单独创建一个太阳的实例
        sunIndependent.compute(self.local)   # 这样无论用户是否选择生成太阳，在其他计算需要获取太阳数据时，都不会因为太阳实例未定义而报错

        bpy.data.worlds["World Sky Texture"].node_tree.nodes["Sky Texture"].sun_elevation = sunIndependent.alt          # 设定太阳高度角，单位弧度
        bpy.data.worlds["World Sky Texture"].node_tree.nodes["Sky Texture"].sun_rotation = sunIndependent.az+math.pi/2  # 设定太阳方位角，单位弧度
        # 由于Blender中天空纹理，以+y轴为0度，而地平坐标系以+x轴正北为0度，所以要加90度，即π/2弧度，这里不涉及地平坐标转球坐标，方位角不需要取负
        bpy.data.worlds["World Sky Texture"].node_tree.nodes["Sky Texture"].altitude = self.alt                             # 设定海拔高度为用户输入

        print(f'Appended World Sky Texture')