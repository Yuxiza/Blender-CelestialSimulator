# -*- coding: UTF-8 -*-
import bpy


# 这里声明囊括一切的 calssB 和 mainB 纯属只是为了套用register_class函数格式，没啥其他用处，从A文件复制来的bl_name等等是为了解决以下报错：
# RuntimeError: register_class(...):, missing bl_rna attribute from 'type' instance (may not be registered)
class classB():

    def mainB():
        
        # # 全选、删除世界中所有物体
        # bpy.ops.object.select_all(action='SELECT')
        # bpy.ops.object.delete(use_global=False, confirm=False)

        # 游标位置、旋转均对齐世界原点
        bpy.ops.view3d.snap_cursor_to_center()

        # 视图裁切终点设为20000m
        # 参考：https://blender.stackexchange.com/questions/265858/
        screens = (s for w in bpy.data.workspaces for s in w.screens)
        V3Dareas = (a for s in screens for a in s.areas if a.type=='VIEW_3D')
        V3Dspaces = (s for a in V3Dareas for s in a.spaces if s.type=='VIEW_3D')
        for space in V3Dspaces:
            space.clip_end = 20000

        """
        文件结构：
        【集合】场景集合
            ┕【集合】Collection
                ┕ （用户自己原有的stuffs）
            ┕【集合】SPAS（插件生成的所有东西都在这里面）
                ┕【集合】starExample.1
                    ┕【棱角球】starExample.1
                ┕【集合】starExample.2
                    ┕【棱角球】starExample.2
                ......
                ┕【集合】starExample.9
                    ┕【棱角球】starExample.9

                （以下是依据starExample.1~9创建的实例集合）
                ┕【实例集合】starExample.10
                    ┕【实例集合】starExample.11
                ......
                ┕【实例集合】starExample.n+9（n为用户输入的星星数量）
        """

        # 新建集合，重命名为SPAS，并从blender后台文件移动到视图层文件
        # 参考：https://blender.stackexchange.com/questions/184363/
        createCollection = bpy.data.collections.new('SPAS')
        bpy.context.scene.collection.children.link(createCollection)
        # 设置SPAS集合为活动项
        bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection.children['SPAS']

        # 创建九个棱角球，各自放在一个集合中，各自赋予不同自发光材质，用作后续实例化的子物体
        for i in range(1,10):
            
            # 新建集合，重命名（名称和集合中物体名相同），并从blender后台文件移动到视图层文件
            # 参考：https://blender.stackexchange.com/questions/184363/
            createCollection = bpy.data.collections.new("starExample." + str(i))
            bpy.context.scene.collection.children.link(createCollection)

            # 在原点新建一个细分2大小0.25的棱角球，挪到原点之外20000m的位置
            ######################################################################################################################
            
            # 这样写的原因是，这九颗标准星做为 “实例化” 操作的子物体，本应该在创建后被隐藏（Blender中的“eyeball”图标，而不是“monitor”图标）
            # 然而Blender直到3.6版本，依然没有任何支持这一操作的api指令，参考：https://blenderartists.org/t/show-hide-collection-blender-beta-2-80/1141768
            # Blender的api原生支持 “禁用选择（pointer 图标）” ， “禁用显示（monitor图标）” ， “禁用渲染（camera图标）”
            # 却没有指令关于 “暂时隐藏显示（eyeball图标）” ，对应地，hotkey H键 也没有对应api
            # 在Blender3.2中，还可以通过 “bpy.context.active_object.hide = True” 这种原生api不存在的方式设定隐藏，但是这一指令在3.6不再支持
            # 所以 我们不得不选择把这九颗标准星移动到视图看不到的地方，既然设定了渲染裁切终点20000m，就挪到原点之外20000m好了
            # 但是这些自带 +x方向 20000m偏移 的标准星，生成的实例也会带有偏移
            # 为避免这种情况，需要给实例子级 starExample.x 的集合 starExample.x 设置同为 +x 20000m 的实例偏移，告诉Blender有偏移这件事，以自动在生成实例时消除这部分偏移
            # 这部分设置在 Collection Properties - Instancing 下面，api为 bpy.data.collections["Collection"].instance_offset[0] = 0


            bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=0.25,location=(20000,0,0))
            # 重命名新生成的棱角球，重命名（名字中的数字1-5-9对应恒星颜色的蓝-白-红）
            bpy.context.object.name = "starExample." + str(i)
            
            # 创建新材质，重命名
            newMat=bpy.data.materials.new(name='material.' + str(i))    # 创建名为{'material.' + str(i)}的新材质 参考：https://juejin.cn/post/7167268956770664456
            newMat.use_nodes = True                                     # 新材质将使用节点
            newMat.node_tree.nodes.get("Principled BSDF")               # 设定节点的值，新材质使用原理化BSDF节点 参考：https://blender.stackexchange.com/questions/160042/
            # 调定自发光强度为20
            bpy.data.materials['material.' + str(i)].node_tree.nodes["Principled BSDF"].inputs[20].default_value = 20
            # 调定自发光颜色（后面有解释）
            bpy.data.materials['material.' + str(i)].node_tree.nodes["Principled BSDF"].inputs[19].default_value = (0.25+0.05*i, min(0.25+0.05*i,0.75-0.05*i), 0.75-0.05*i, 1)
            # 将新建材质应用于活动物体（也就是刚刚新建的棱角球）
            bpy.context.active_object.data.materials.append(newMat)
            # 把活动物体放进指定名称的集合 参考：https://blender.stackexchange.com/questions/132112/
            bpy.data.collections["starExample." + str(i)].objects.link(bpy.context.active_object) 
            # 给实例子级所在集合设定 +x 20000m 的实例偏移
            bpy.data.collections["starExample." + str(i)].instance_offset[0] = 20000

            # 为了节省工作量，本项目只根据光谱大类判断恒星颜色，按温度从高到低排序依次为 (W)OBAFGK(S)M（W是wolf-rayet星），颜色从蓝色到红色过渡
            # 颜色通过调节(R,G,B,A)色彩实现，偏红的就提高R比例，偏蓝的就提高B，A是不透明度默认恒为1；RGB比例取值范围在0到1之间，不妨使R+B=1，这样在R或B其一较高时效果较好
            # 但是两者比例接近时会出现粉色，这就不对了，所以需要一些绿色；随便在blender里试试发现，总取G等于R、B中较小的那个值，就是一种很简便也很好看的做法，使得红蓝之间以白色而非粉色过渡，更符合真实情况
            # 避免星星蓝/红得太离谱，R和B的值都以0.5为基准上下0.2浮动，即最红的material.9是(0.7,0.3,0.3)，最蓝的material.1是(0.3,0.3,0.7)
            
            # 对于刚创建的物体，在视图层（而非全局）禁用视图显示，参考：https://blender.stackexchange.com/questions/94320/
            # bpy.context.active_object.hide = True

            # 禁用九颗标准星的选中功能，使其不能在D文件“全选SPAS集合下所有物体”这一步被选中，从而不参与天球旋转，维持（20000,0,0）的坐标和x=20000的实例偏移
            # 不然标准星也会随天球转动，坐标发生改变，但系统仍用x=20000修正偏移，会导致整个天球跑偏
            bpy.context.active_object.hide_select = True

            # 并且禁用渲染，参考：https://devtalk.blender.org/t/still-able-to-hide-objects-with-python/5418
            # bpy.context.object.hide_render = True
            # 不能禁用渲染......不然实例化出来的东西也会禁止渲染

        # 再次设置SPAS集合为活动项，准备将实例化的内容放进去
        bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection.children['SPAS']

        # 使用Cycles渲染器，GPU计算渲染
        bpy.context.scene.render.engine = 'CYCLES'
        bpy.context.scene.cycles.device = 'GPU'

        print('Prepared the world.')

# def register():
#     from bpy.utils import register_class
#     register_class(classB)

# def unregister():
#     from bpy.utils import unregister_class
#     unregister_class(classB)
