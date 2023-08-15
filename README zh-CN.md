<center>

# 精密科学天文系统——真实世界天球仿真
<font size="5">插件文档（简体中文）</font>
<br>
<font size="3"> 
<br>本插件为Blender开发，提供任何时间地点下，尽可能精确、真实的天体仿真<br>
</font>

<br><font size="4"> 

**作者：**

B-MH <sup>1</sup>&emsp;WannaR <sup>2</sup>

**2023年8月15日**

**中国 北京**

</font></center><br>

## 第一章 插件概况

&emsp;&emsp;这是一个由 B-MH 和 WannaR 开发的 Blender 项目，未经许可，请勿转载、复制、二次售卖。<br>

&emsp;&emsp;本项目用 Python 编写，设计中使用英文（作者是国人），旨在尽力为 Blender 用户提供最科学和精确的天体仿真模拟。具体来说，**本插件允许用户选定地球上的任意地点（通过指定经纬度坐标和海拔高度），生成该地任意时刻（通过输入时区、日期和时间）的真实天球。**<br>

&emsp;&emsp;天球内容包括：SAO 星表收录的最多 258997 颗恒星、太阳、月亮（地球的天然卫星，打括号是因为英语moon还有卫星意）、太阳系行星（显然没法显示地球吧）、冥王星；可以实现的天文现象演示包括日食、行星被月球掩食、行星被太阳掩食、内行星（水星、金星）相位、月球相位、月球潮汐锁定、月球天平动、土星环倾斜周年视运动。<br>

&emsp;&emsp;插件尚不支持动态演示，生成的天空会静止在指定地点的指定时刻；目前还不包含对月食、内行星凌日、太阳和行星自转的演示效果。后续版本更新中，我们计划持续添加对太阳系行星的卫星、矮行星、小行星、彗星、自定义人造卫星等天体和银河的支持。<br>

&emsp;&emsp;本项目借助 SAO 星表、 NASA 公开的行星和月球三维模型以及开源Python包“pyephem”和天文算法等实现。我们注意到，当下已经有了像Stellarium这样优秀的天文计算和模拟程序，但似乎没有人将它们移植到Blender，这使得用户获得真实天空背景的需求很难满足。我们相信这样的需求永远存在，例如天文学家 Neil deGrasse Tyson 曾经指出电影《泰坦尼克号》的特效使用了错误的背景星空；此外，对于在做一些夜景、航空和近地轨道项目的用户来说，使用正确且准确的星空背景总能够起到锦上添花的效果。<br>

&emsp;&emsp;该项目计划以开源形式发布，项目的代码结构和实现方法稍后可能会以文档或视频的形式进行阐释。我们衷心感谢该插件的每一位用户和为该插件的代码提出优化想法的开发人员。<br>

&emsp;&emsp;这是本插件的第一个版本，我们相信它的功能和囊括的天体都是十分有限的，代码也存在很大的优化空间。因此，未来我们将根据不断增长的需求持续开发这个项目，并发布新版本，敬请关注！<br>

&emsp;&emsp;版权所有 B-MH 和 WannaR ，保留所有权利。<br><br>



## 第二章 插件使用说明

### 1. 在Blender中使用.zip文件安装并启用插件（这部分请浏览相关网络教程）<br>

### 2. 安装并启用完成后，应当能在Blender的Layout界面右侧看到名为SPAS的标签，点击并展开SPAS面板<br>

### 3. 进行必要的参数输入，包括：<br><br>

- **日期和时间输入** <br><br>
首先在时区下拉菜单中选择目标地点的时区，此时区应当是该地区官方规定采用的，如中国全境采用东八区北京时间（UTC+8），无论实际处于什么经度；<br><br>
时区一项涵盖了从UTC-12到UTC+14的27个时区，对于极特殊的UTC+8:45这种时区，没有设置；<br><br>
其次输入目标地点当地的日期时间，为格里高利历公元纪年。其中年月日时分秒，如数值不等于“0”，则均不能以0开头（“00”，“7”这种输入是对的；“02”这种是不接受的）。类似的，这里的年月日时分秒也应当是该地区官方规定采用的当地时间，而不是UTC+0的格林威治时间；<br><br>

- **地点和海拔输入** <br><br>
输入目标地点的经纬度坐标，海拔高度；<br><br>
经纬度坐标支持四位小数，北纬、东经用正数表示；南纬、西经用负数表示。纬度范围 [-90.0000°,90.0000°] ，经度范围 [-180.0000°,180.0000°] <br><br>
海拔高度仅支持整数，单位为米。<br><br>

- **期望星数设定** <br><br>
输入期望生成多少颗星（按恒星亮度从高到低排序，最多支持258997颗）；<br><br>
我们并不建议使用太大的数字：一般在城市晴朗的晚上，不借助相机或望远镜等设备，肉眼大约可见3000-6000颗星；经测试，本插件在不生成太阳，月亮和其他黄道天体（行星、矮行星等）的情况下，创建不同数目的恒星需要如下时间：<br><br>

**<center>设备信息</center>**
<center>AMD Ryzen 9 5900HX&emsp;NVIDIA GeForce RTX 3050 Ti&emsp;RAM 4GB&emsp;Blender 3.2</center>

**<center>测试结果</center>**


<center>

|数量|耗时（秒）|数量|耗时（秒）|
|:--:|:--:|:--:|:--:|
|500|1.5|1000|18|
|2000|37.5|5000|327|

</center>

**<center>表1-1</center>**<br>

- 对以上结果我们感到非常奇怪，生成恒星数量和所需时间之间并非是线性关系，又不像指数关系，产生这种现象的原因仍然不清楚。不过综合视觉效果和所需时间，我们还是建议把数量选在500-2000之间。<br><br>

- **选定附加天体**<br><br>
本插件默认生成指定数目的恒星，对于太阳系的其他天体，这里给出了 “太阳”、“月亮”（地球卫星）、“行星及冥王星” 三个附加选项，用户可以勾选希望生成的天体。后续版本更新中，我们计划持续添加对太阳系行星的卫星、矮行星、小行星、彗星、自定义人造卫星等天体和银河的支持。 <br><br>
需要注意的是，即使不勾选生成太阳，世界仍然会自带一个天空纹理，其中的光源方位就是真实的太阳方位，只不过不显示日轮。如果不需要此天空纹理，可以手动到Blender的Shader着色器界面，断开世界环境中 “天空纹理” 到 “背景” 的连接，此时默认世界背景颜色为黑色（#000000）。<br><br>

- **设定天球半径**<br><br>
天球原本是一个虚拟的球，是人类为了建立赤道坐标系研究恒星而规定的。其极轴与地球极轴重合，以北极星为天球北极点，北极星到地球的距离为球体半径，将天上所有恒星向地心方向投射在球面上。本插件也是基于此模型生成的星空，所有恒星将会分布在一个虚拟的球体上，这里允许用户自定义该虚拟球体的半径，单位为米。<br><br>

### 4. 初始化世界 生成天球：<br><br>

- **首先单击 “Initialize World” 按钮**，等待几秒。<br><br>
这时系统会在世界中创建一些集合、物体、材质等，作为接下来生成天球的准备，同时提取面板中输入的数据，准备进行运算<br><br>

- **等创建完成后，单击 “Generate Celestial” 按钮**，等待数秒到数分钟。<br><br>
可以根据上表1-1的给出的实机测试结果和自身的设备性能，估算生成恒星需要的时间。<br><br>

### 5. 生成完毕<br><br>
现在您可以在生成的天球内布设其他场景了，抬头即可看到选定的时间地点下，真实还原的天空，当然了，那可能是夜空，也可能是白昼。<br><br>
请注意在场景中添加相机后，调整相机物体属性中的 “镜头-结束点” 一项，使其大于输入的天球半径，否则在渲染时无法获取较远处的图像<br><br>

### 6. 可能的错误与解决方法<br><br>
由于 Blender api 变化，在3.2版本上正常运行的代码在更高版本上可能出现问题。本插件在Blender3.6实机测试时，发现如果开启了Blender界面翻译，可能会报出 “找不到‘Principled BSDF’” 的错误，此时，设置Blender的语言为英文，退出程序，重新进入再重复上面1~4小节的操作即可。<br><br>
我们尝试了地球上的诸多地点，跨年、跨月等各种特殊数据，除上述翻译问题造成的报错之外，没再在测试中发现过问题，只要确保输入的经纬度坐标准确，输入的日期、时间和时区均是当地官方所规定的，生成的天球总能够符合 Stellarium 在同样条件下的模拟结果。<br><br>

<br>
<center>———— 以下内容可供开发人员参考 ————</center>

## 第三章 文件结构

### 1. 文件组成
+ Scientific and Precision Astronomical System

    + [ \_\_pycache\_\_ ]（运行时生成）
    + Database
        + 001_The original SAO Star Catalog (just act as a back-up here).txt
        + 002_Document of the original SAO Star Catalog.txt
        + 003_Sorted SAO Star Catalog (sort accroding to the star's visual magnitude).txt
        + 004_Parameters obtained from UI panel.csv
        + 005_Pre-Operated index to generate code for Blender.csv
    + ephem
        + \_\_pycache\_\_
        + doc
        + tests
        + \_\_init\_\_.py
        + _libastro.cp310-win_amd64.pyd
        + _libastro.pyd
        + cities.py
        + stars.py
    + \_\_init\_\_.py
    + A_Generate_UI.py
    + B_Preparing_the_Blender_Scene.py
    + C_Convert_star_info.py
    + D_Generate_the_stars.py
    + E_Generate_Sun_Moon_Planet.py
    + README zh-CN.md
    + README en-US.md


### 2. 文件功能
+ \_\_pycache\_\_ 文件夹中是Python文件运行产生的缓存<br>

+ Database 文件夹存储了代码运行过程中需要读写的数据，其中：<br>

    + 001_The original SAO Star Catalog (just act as a back-up here).txt
        + 是原始的 SAO 星表文件，为开发者留作备份，来源于： https://heasarc.gsfc.nasa.gov/W3Browse/star-catalog/sao.html<br><br>

    + 002_Document of the original SAO Star Catalog.txt
        + 是上述 SAO 星表的官方解释文档，为开发者留作备份，和 SAO 星表来源相同<br><br>

    + 003_Sorted SAO Star Catalog (sort accroding to the star's visual magnitude).txt
        + 这是使用 Python 预处理过的 SAO 星表，从原始星表中提取出了恒星 SAO 编号、J2000.0 纪元下的赤经赤纬、视星等、光谱类型，并按照亮度从高到低（视星等从小到大）进行了排序<br><br>

    + 004_Parameters obtained from UI panel.csv
        + 该文件用于存储用户在面板的参数输入<br><br>

    + 005_Pre-Operated index to generate code for Blender.csv
        + 该文件存储计算得到的恒星 (x,y,z) 直角坐标，由赤经赤纬、天球半径（用户自定义）通过球坐标系转直角坐标系计算得来；假设用户选定生成n颗恒星，则会计算并在本文件中存储n+10条数据，多出的10条是避免一些容易被忽视的问题导致错误<br><br>

+ ephem 是开源的 Python 库，负责进行天文计算，这里仅就部分核心内容进行解释<br>详情请见 ephem 项目地址： https://rhodesmill.org/pyephem/

    + \_\_init\_\_.py 
        + 由于 ephem 库是用C语言编写的，其计算核心其实是若干C语言文件和头文件编译而成的 `_libastro.cp310-win_amd64.pyd` 文件，这里的 \_\_init\_\_.py 主要作用便是存取 .pyd 文件中的变量，调用其中的函数等。<br><br>
    
    + _libastro.cp310-win_amd64.pyd<br>_libastro.pyd
        + 直接使用下载的 ephem 库文件夹会在运行 \_\_init\_\_.py 的 `import _libastro` 字段时报出`找不到 .pyd 文件`的错误，把原先的 `_libastro.cp310-win_amd64.pyd` 文件改名为 `_libastro.pyd` 即可。这部分在 \_\_init\_\_.py 文件中有两处注释<br><br>同时需要注意，由于Blender 3.2 - Blender3.6 均使用 Python 3.10，且支持CPython，所以我们采用的是 `ephem 4.1.4 cp310` 版本，如果有需要移植到其他 Python 版本的 Blender ，请自行更改为带有 “使用相应 cp 版本号的 `_libastro.cpXXX-win_amd64.pyd` 核心的” ephem 库，否则会报出找不到 DLL 文件的错误。<br><br>
        
    + cities.py<br>stars.py
        + 分别存储了一些 ephem 库预设的城市、恒星相关数据

    + tests
        + 本文件夹下存储了一些 ephem 的测试代码，以及用于计算的 NASA JPL 星历<br><br>
        

+ \_\_init\_\_.py
    + Blender 创建插件以及注册文件的规范格式<br><br>

+ A_Generate_UI.py
    + 生成插件UI面板，读取、存储用户在面板输入的数据，定义两个按钮操作<br><br>

+ B_Preparing_the_Blender_Scene.py
    + 初始化 Blender 世界，创建所需的集合、物体、材质，具体作用在下一章进行展开<br><br>

+ C_Convert_star_info.py
    + 调用 Database 文件夹中的恒星星表数据和用户输入数据，根据恒星赤经赤纬、用户输入的天球半径、生成恒星数量，计算得到恒星在 Blender 的 (x,y,z) 直角坐标，视星等与 scale 系数，光谱类型与自发光颜色的对应关系<br><br>

+ D_Generate_the_stars.py
    + 生成用户所需数目的恒星，此时天球是 “极轴躺在x轴上的”，即 (r,0,0) 处为天球北天极， (0,0,-r) 处为春分点， (0,0,r) 处为秋分点；因此还会计算时角，旋转天球到当前时角，根据纬度，旋转天球到当前仰角<br><br>

+ E_Generate_Sun_Moon_Planet.py
    + 根据用户选择，生成对应的太阳系天体，并偏移各天体的自转轴直至其真实情况，设定月球潮汐锁定；对于除了太阳的所有被选天体（无论用户是否选择生成太阳），添加来自太阳方向的光照<br><br>

## 第四章 代码实现原理

*这里只记录大致思路，技术细节和算法请参考代码中的注释，在那里写了很多；关于 ephem 库的调用方法和代码书写格式，参考 ephem 官网：https://rhodesmill.org/pyephem/*

### 太阳系外恒星
+ **1. 生成恒星**

    我们从Database的 `001_The original SAO Star Catalog (just act as a back-up here).txt` 文件提取了258997颗恒星的SAO编号、J2000.0纪元下赤经赤纬，视星等，光谱类型数据，按恒星亮度从高到低排序，存入了 `003_Sorted SAO Star Catalog (sort accroding to the star's visual magnitude).txt` 文件。<br><br>**第一步是将用户所需数目的恒星生成在一个虚拟球体——天球上**。<br><br>生成恒星的原理是，在单击 Initialize World 按钮的时候，会运行 `B_Preparing_the_Blender_Scene.py` ，程序化地在世界中创建九颗标准星，并赋予不同颜色的自发光材质。颜色和光谱类型相关，因而后续生成恒星只需要根据该恒星光谱类型，挑一颗标准星去实例化，按视星等到 scale 系数的映射公式算出比例，进行缩放（以大小区分恒星亮度），再移动到对应位置即可<br><br>这个位置计算通过将赤经赤纬看做球坐标系坐标，套用数学公式转化为直角坐标实现；这个天球的半径也是由用户设定的，直接作为球坐标系的半径使用。<br><br>坐标系转换部分的代码在 `C_Convert_star_info.py` ，转换结果存储在 `Database\004_Parameters obtained from UI panel.csv` ，实例化部分的代码在 `D_Generate_the_stars.py` 的前半部分。<br><br>**这里需要注意两个容易忽视的地方：**<br>
    + **球坐标系转直角坐标系**<br>

        球坐标系 (r,θ,φ) 转直角坐标系 (x,y,z) 的公式为：<br><br>

        <centre>

        $$
        \begin{cases}
        x\enspace=\enspace rsinθcosφ\\
        y\enspace=\enspace rsinθsinφ\\
        z\enspace=\enspace rcosθ
        \end{cases}
        $$

        </centre>

        <br>
        赤经赤纬与半径的形式为（直接采用了SAO星表的弧度制赤经赤纬，而非 “时分秒” 、 “度分秒” 格式）：<br><br>

        <centre>

        $$
        \begin{cases}
        赤经 Ra\enspace=\enspace a\enspace(rad)\\
        赤纬 Dec\enspace=\enspace b\enspace(rad)\\
        半径 r\enspace=\enspace c\enspace(米)
        \end{cases}
        $$

        </centre>

        <br>如果直接把赤经视作φ，把赤纬视作θ，会出问题：<br><br>
        **关于φ**<br><br>在通用的直角坐标系右手系（right-hand system）中，球坐标系的φ实际是由+x轴转向+y轴的辐角，也就是说，视线沿着-z方向向下看去，φ角是逆时针增大的。这一点  倒是与天球赤经的编号方法相同，因为从天球北天极上空向下俯瞰，赤经也是逆时针增大的。<br><br>但是这个规定和地理坐标系的方位角相反，地理方位角通常以正北为0°，正北向正东旋转增大，也就是从上空向下看，地理方位角顺时针增大。<br><br>因此如果以+x轴为正北方向，需要使用地理坐标系的方位角、高度角生成直角坐标时，要把方位角取相反数（根据数学的任意角原理），才能作为φ参与计算<br><br>

        **关于θ**<br><br>这个θ是球面上某点P的矢径（向径）和+z轴的夹角，而不是该矢径相对于 xoy平面的仰角。因此无论是地理坐标系的仰角，还是赤纬，都要被π/2减一次，才能做为θ参与计算，例如 θ = π/2 - Dec<br><br>

    + **初始的天球状态**<br>
    
        *这部分内容详见代码注释*<br>
        按上述方法生成的天球，极轴和+z轴是重合的，即北天极在 (0,0,r) 。这不利于后续根据纬度 进行调整，因为纬度多高，北天极就应该在多高的仰角上，此时应该默认仰角为0，需要时再去旋转对应角度。所以这个天球还应绕y轴，从+z向+x方向转九十度，原本的点 D (x0, y0, z0) 会变  成新的点 D' (x, y, z) = (z0, y0, -x0)<br><br>

+ **2. 旋转天球**

    显然经历上述过程生成的天球，是一个在地球赤道上，时角为0的天球，即 (r,0,0) 处为天球北天极， (0,0,-r) 处为春分点， (0,0,r) 处为秋分点。要想得到设定时间地点的天球，需要对天球进行两次旋转，第一次绕极轴（+x轴）旋转时角，第二次绕y轴旋转北天极仰角。<br><br>
    这部分代码在 `D_Generate_the_stars.py` 的后半部分。

    + **计算时角**<br><br>
        我们懒得写低精度的时角估算公式了，于是直接调用了 ephem 内置的恒星亮星库，选择全天第一亮恒星天狼星做为计算靶标，使用 ephem 计算出设定时间地点天狼星的方位角、高度角（这里的方位角由于是地理方位角，需要取相反数才能做为φ参与计算，原因在上文解释过了）<br><br>
        需要注意的是，这里用于 ephem 计算的地点，其经度等于用户输入，但是纬度使用0°，因为此时的天球还是 “在地球赤道上，时角为0的天球”，这一步在赤道上只计算时角，暂不考虑纬度问题<br><br>
        这样计算出的天狼星，相对于初始状态，应该只是绕极轴（x轴）转了一个角度的，即时角。这个角度可以使用 `arctan(after Z / after Y) - arctan(before Z / before Y)` 计算得到，于是全选整个天球所有恒星，绕x轴旋转这个角度的负值即可<br><br>
        为什么是负值我想不明白，可能是视角问题？用上面公式计算出的旋转角度，是面向-x方向看到的yoz平面直角坐标系，而旋转时用的是面向+x的角度计算？但总之加上负号转完就是对的......
    
    + **旋转仰角**<br><br>
        纬度多高，北天极就应该在多高的仰角上，所以转完时角以后，直接绕y轴旋转当地纬度即可

### 太阳系天体

+ **追加天体**<br><br>
    为减省代码，太阳系天体不采用程序化生成，而是直接从预设的文件 `3DModelAppend.blend` 中追加。天体在被追加进世界的同时，一并携带了其自身的材质、贴图、集合节点进入 Blender 文件，为后续操作做准备<br><br>
    天体模型来源:<br>
    https://solarsystem.nasa.gov/resources/2352/sun-3d-model/<br>
    https://solarsystem.nasa.gov/resources/2369/mercury-3d-model/<br>
    https://solarsystem.nasa.gov/resources/2343/venus-3d-model/<br>
    https://solarsystem.nasa.gov/resources/2372/mars-3d-model/<br>
    https://solarsystem.nasa.gov/resources/2375/jupiter-3d-model/<br>
    https://solarsystem.nasa.gov/resources/2355/saturn-3d-model/<br>
    https://solarsystem.nasa.gov/resources/2344/uranus-3d-model/<br>
    https://solarsystem.nasa.gov/resources/2364/neptune-3d-model/<br>
    https://solarsystem.nasa.gov/resources/2357/pluto-3d-model/<br>
    https://open3dmodel.com/3d-models/moon-from-nasa_595918.html<br><br>
    对于被需要的天体，追加后会被移动到指定位置。位置计算方法是：由 ephem 使用设定的时间地点计算得到目标天体的方位角、高度角，再转化成直角坐标<br><br>
    为增加真实性，每个天体会根据 ephem 计算出的视直径（单位为角秒）乘以所在球面半径，得到视直径（单位为米），进而进行缩放，还原其真实视觉大小<br><br>
    这里，我们选择让不同类型的太阳系天体运动在不同半径的球面上，假定天球半径设为r，则行星和冥王星所在球面半径为0.98r，太阳的在0.96r，月亮的在0.94r，这样就能形成一定的遮挡关系，实现日食、行星被月球掩食、行星被太阳掩食的现象；但同时，也有一些注定无法实现，如月食、内行星凌日。前者因为这里的 “地球” 不是实体，没法将月球挡在地球影子中形成月食；后者是因为行星所在球面在太阳所在球面之外，永远没机会挡住太阳。<br><br>
    后续版本我们可能会对这些问题进行修复，比如按真实比例重建太阳系，而不是将太阳系天体都放在虚拟的天球球面上，这样理论上就能支持的所有天文现象了，除去月食，因为 “地球” 终究还是Blender中的那个坐标系，没有能投射阴影的实体

+ **对齐坐标轴**<br><br>
    还原太阳系天体的天文现象，与其手动编写视觉效果的代码，不如直接让所有太阳系天体的极轴（天体模型局部坐标系的+z轴）朝向其真实情况下的方向。这样在天体和地球相对位置改变时，自然而然地就会观察到月球天平动、土星环倾斜周年视运动等现象，和真实的太阳系中天文现象的形成机理一致<br><br>
    此外，月球多一步潮汐锁定，要让月球正面（月球局部坐标系的+x轴）在绕+z轴转动的同时，始终指向地球<br><br>
    以上两件事都可以通过天体在追加时自带的 “对其欧拉至矢量” 几何节点实现：<br><br>
    只需要在 Stellarium 中抄下现成的，目标天体自己的 “北天极” 赤经赤纬即可。使用 ephem 库的 “Fixedbody()” 函数，注册为一颗 “虚拟星” ，即目标天体的 “北极星” ，计算 “虚拟星” 在设定时间地点的高度角，方位角，转换成直角坐标，做为极轴要对齐（向量平行）的矢量即可<br><br>
    潮汐锁定同理，月球局部坐标系的+x轴要对齐的矢量就是月球指向地球的矢量，所以把月球直角坐标取相反数反转即可<br><br>

+ **添加日光**<br><br>
    太阳系天体（除了太阳本身）都是会被阳光照亮的。Blender 3.2 - Blender 3.6 版本还没有支持灯光排除，除非使用其他视图层，但那会严重影响插件使用的便捷性。我们索性给每个天体配了 “一盏灯”， 模拟阳照区接受日照的效果<br><br>
    在Blender试验发现，假设a为天体视直径（单位meter），在太阳和天体连线上，距离天体2a的位置，放一个点光，半径1.2a，刚好能模拟出天体被阳光照亮一半的效果。这部分也是向量计算即可完成，点光亮度根据天体不同分别赋值<br><br>
    这个点光在生成时使用独立的ephem太阳实例计算，所以无论用户是否选择生成太阳，都不影响创建正确方位的点光

### 世界环境

+ **天空纹理**<br>

    我们使用了Blender内置的天空纹理来模拟白天或黑夜的地球天空。这个世界环境节点同样是从预设的文件 `3DModelAppend.blend` 中追加而来。天空纹理节点中，太阳方位、高度也使用独立的ephem太阳实例计算，所以无论用户是否选择生成太阳，都不影响天空纹理中太阳位置的正确。此外，在白昼，天空纹理的光能足够亮到淹没恒星的光，也算比较真实地还原了白昼期间的天空。

+ **默认环境色**<br>

    如果用户不需要大气在有日光时的天亮效果，可以断开 “天空纹理” 到 “背景” 的连接，此时默认世界背景颜色为黑色（#000000）。<br><br>

## 第五章 需要交代的零散操作
### 路径绝对化
使用同文件夹下的相对路径，在Blender中总会报错，于是代码中采用了路径绝对化操作，即通过 `currentPyFilePath = os.path.abspath(__file__)`  获取当前.py文件的路径，再通过 `parentPyFilePath = os.path.dirname(currentPyFilePath)`  获取当前.py文件所在的文件夹（整个插件所有文件都在这里），然后在 `parentPyFilePath` 后面，使用 `os.path.join(......)` 连接之前的相对路径即可

### sys.path.append (......)
Blender 总是找不到同文件夹下的 ephem 库，所以每次运行时，都会在 `__init__.py` 文件中，把当前文件夹加入Blender Python.exe 会查找到的系统路径

### 格林威治时间
ephem 使用格林威治时间 (GMT) 做为天文计算的时间输入，但不保证每个使用插件的人都清楚怎么得到格林威治时间，这就是面板中要求选择时区并输入当地时间的原因，让程序代劳，来求算格林威治时间<br>
遗憾的是，ephem 每逢涉及 “倒退一年、一月” 的日期换算问题时，就会出错，详见 `A_Generate_UI.py` 中的相关注释

### 裁切终点
天球半径可能是很大的，为避免一些用户发现画面缺失远景又不知道怎么调，直接在代码中为所有窗口预设了视图的裁切终点： <br>

```Python
    # 视图裁切终点设为20000m
    # 参考：https://blender.stackexchange.com/questions/265858/
    screens = (s for w in bpy.data.workspaces for s in w.screens)
    V3Dareas = (a for s in screens for a in s.areas if a.type=='VIEW_3D')
    V3Dspaces = (s for a in V3Dareas for s in a.spaces if s.type=='VIEW_3D')
    for space in V3Dspaces:
        space.clip_end = 20000 
```

但是这样依然不能解决渲染时的问题，还需要用户添加相机后，自己去 “相机物体属性-镜头-结束点” 设定一个大于天球半径的值

### 代码注释翻译和 README 翻译
这个版本开源代码的注释是用全中文写的，没配备英文翻译。开发人员可能需要使用翻译器来阅读。<br><br>
我们在一些容易混淆的地方做了一些英文注记，比如在提到单位“米”的地方标记“meters”，因为在中文中单位 “meter” 是 “米” ，可能被误译为其其它义项 “大米” 。<br><br>
README的中译英大部分是机翻，尽管我尽量逐句纠正了翻译，但应该仍不完美<br><br>
如果该插件在未来能取得一定热度，我们会考虑在翻译问题上提供更多支持<br><br>

<center>

<font size=5>

**致无尽蔚蓝与星汉灿烂！**<br>
**TO INFINITE AZURE & STARRY OCEAN!**

</font>

</center>