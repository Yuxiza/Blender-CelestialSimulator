<center>

# Scientific and Precision Astronomical System - Real World Celestial Simulation
<font size="5">Add-on Documentation (English)</font>
<br>
[中文文档](https://github.com/Yuxiza/Blender-CelestialSimulator/blob/main/README%20zh-CN.md)
<font size="3"> 
<br>This add-on aims to provide users with the most precise and scientific celestial simulation whenever and wherever as possible, specially designed for Blender.<br>
</font>

<br><font size="4"> 

**Author:**

B-MH <sup>1</sup>&emsp;WannaR <sup>2</sup>

**April 15<sup>th</sup>, 2023**

**Peking, P.R.C.**

</font></center><br>

## Chapter 1&emsp;Add-on Introduction

&emsp;&emsp;This is a Blender project developed by B-MH and WannaR. Please do not reprint, copy, or resell without permission.<br>

&emsp;&emsp;This project, written in Python, designed in English (the authors are Chinese) aims to provide Blender users with the utmost scientific and precision simulation of celestial objects as possible.Specifically, **this add-on allows users to select any location on Earth (by specifying latitude and longitude and altitude) and generate a real celestial sphere of that location at any time (by inputting time zone, date, and time).**<br>

&emsp;&emsp;The celestial sphere includes: up to 258997 stars included in the SAO star catalog, the sun, moon (natural satellite of Earth), planets in the solar system (obviously unable to display Earth), and Pluto; Demonstrations of astronomical phenomena that can be achieved include solar eclipses, planets being eclipsed by the moon, planets being eclipsed by the sun, phases of inner planets (Mercury, Venus), phases of the moon, tidal locking of the moon, lunar libration, and annual tilt motion of Saturn's rings. <Br>

&emsp;&emsp;The add-on does not yet support dynamic demonstration, and the generated sky will remain stationary at the specified location and time; At present, it does not include demonstration effects on lunar eclipses, planetary transits, and the rotation of the sun and planets. In future version updates, we plan to continue adding support for celestial bodies such as satellites of solar system planets, dwarf planets, asteroids, comets, and custom artificial satellites in the solar system, as well as the Milky Way. <Br>

&emsp;&emsp;It has been made possible through published resources like the SAO Star Catalog, Planetary and Lunar 3d-model from NASA, as well as open-source Python package "pyephem" and algorithms. We have noticed that there are already excellent astronomical computing and simulating programs such as Stellarium, but it seems that no one has ported them to Blender, making it difficult to meet the need to obtain real sky backgrounds. We believe that such needs are always existing, for instance, the movie special effect of Titanic has been pointed out by astronomer Neil deGrasse Tyson for applying wrong background starry sky; moreover, for users performing some night scenes, aviation, and Low Earth Orbit projects, using correct and accurate star background is always the icing on the cake.<br>

&emsp;&emsp;This project is planned to be released in an open-source format, and the code structure and implementation methods of the project may be explained in the form of documentations or videos later. We sincerely appreciate every user of the add-on, and developer who has proposed optimization ideas for the code of this add-on.<br>

&emsp;&emsp;This is the first version of the add-on, we believe its functionality and inclusion of celestial bodies are limited, there are also some possibilities for code optimization. So in the future, we are continually developing this project according to the increasing needs and release new versions. Stay tuned!<br>

&emsp;&emsp;Copyright B-MH and WannaR , all rights reserved.<br><br>



## Chapter 2&emsp;Usage Guidelines

### 1. Install this add-on via the .zip file in Blender and enable it (please follow internet tutorials about this section)<br>

### 2. After have the installation and enabling finished, one shall be able to see a label named "SPAS" in the right of Blender's Layout interface, click it and expand the panel <br>

### 3. Do necessary parameter input, include:<br><br>

- **Date and time** <br><br>
Firstly, select the time zone of the target location from the time zone drop-down menu. The selected time zone should be officially adopted by the region. For example, the East Eighth Zone Beijing Time (UTC+8) is used throughout China, regardless of the actual longitude;<br><br>
The 27 time zones cover from UTC-12 to UTC+14, and is not set for the extremely special time zone like UTC+8:45;<br><br>
Secondly, enter the local date and time of the target location, in Gregorian calendar year. The used year, month, day, hour, minute, and second value, if not equal to "0", cannot have leading "0" (inputs such as "00" and "7" are correct; inputs such as "02" are not acceptable). Similarly, the date and time here should also be the local time used by the official regulations of the region, rather than UTC+0 Greenwich Mean Time;

- **Location and altitude** <br><br>
Enter the latitude and longitude coordinates and altitude of the target location;<br><br>
The latitude and longitude coordinates support four decimal places; the north latitude and east longitude are represented by positive numbers; The south latitude and west longitude are represented by negative numbers. Latitude range [-90.0000°, 90.0000°], longitude range [-180.0000°, 180.0000°] <br><br>
The altitude only supports integers, in meters.<br><br>

- **Expected star amount settings** <br><br>
Enter the expected number of stars to generate (sorted by star brightness from high to low, with a maximum support of 258997 stars);<br><br>
We do not recommend using too large numbers: usually on a clear city night, without the use of cameras or telescopes, approximately 3000 to 6000 stars can be seen with the naked eye; After testing, this add-on requires the following time to create different numbers of stars without generating Sun, Moon and other ecliptic celestial bodies (planets, dwarf planets, etc.):<br><br>

**<center>Device info.</center>**
<center>AMD Ryzen 9 5900HX&emsp;NVIDIA GeForce RTX 3050 Ti&emsp;RAM 4GB&emsp;Blender 3.2</center>

**<center>Text Results</center>**


<center>

|Amount|Time (Second)|Amount|Time (Second)|
|:--:|:--:|:--:|:--:|
|500|1.5|1000|18|
|2000|37.5|5000|327|

</center>

**<center>Table 1-1</center>**<br>

- We are puzzled by the results above, as the relationship between the number of stars been generated and the required time is neither linear nor exponential, and the reason for this phenomenon is still unclear. However, considering the visual effect and the required time, we still recommend selecting a quantity between 500 and 2000.<br><br>

- **Select Additional celestial bodies**<br><br>
This add-on generates a specified number of stars by default. For other celestial bodies in the solar system, three additional options are provided: "Sun", "Moon"(Earth's moon), "Planet and Pluto". Users can check the celestial bodies they want to generate. In future version updates, we plan to continue adding support for celestial bodies such as satellites, dwarf planets, asteroids, comets, and custom artificial satellites in the solar system, as well as the Milky Way.<br><br>
It should be noted that even if the option "Sun" is not selected, the world still comes with a sky texture, where the light source orientation is the true sun orientation, but the sun disk is not displayed. If you do not need this sky texture, you can manually go to Blender's Shader  interface and disconnect the connection from the "sky texture" to the "background" in the world environment. At this time, the default world background color is black (# 000000). <br><br>

- **Set the radius of celestial**<br><br>
The celestial sphere was originally a virtual sphere established by humans to study stars in an equatorial coordinate system. Its polar axis coincides with the Earth's polar axis, with star "Polaris" as the celestial North Pole and the distance from Polaris to Earth as the radius of the sphere, projecting all stars in the sky towards the Earth's center onto the sphere. This add-on is also written based on the star sky generated by this model. All stars will be distributed on a virtual sphere. Right here we allow users to customize the radius of the virtual sphere, in meters.<br><br>

### 4. Initialize the world and generate the celestial<br><br>

- **First, click on the "Initialize World" button and wait for a few seconds** <br><br>
At this point, the system will create some collections, objects, materials, etc. in the world as preparation for generating the celestial sphere and extracting the data input from the panel for calculation.<br><br>

- **After the creation is completed, click the "Generate Celestial" button and wait for a few seconds to minutes** <br><br>
You can estimate the time required to generate stars based on the actual machine test results and your own device performance given in Table 1-1 above.<br><br>

### 5. Finishing Generation<br><br>
Now you can set up other scenes within the generated celestial sphere, and look up to see the real restored sky at the selected time and location. Of course, it may be night sky or day.<br><br>
Please note that after adding a camera to the scene, adjust the "Lens - End Point" item in the camera object attribute to make it larger than the input radius of the celestial sphere, otherwise, the remote image cannot be obtained during rendering.<br><br>

### 6. Possible errors and solutions<br><br>
Due to changes in the Blender API, code that runs normally on version 3.2 may experience issues on later versions. During the Blender 3.6 real machine testing of this add-on, it was found that if Blender interface translation was enabled, an error of "Unable to find 'Principled BSDF'" may be reported. In this case, set Blender's language to English, exit the program, re-enter, and repeat the operations in sections 1-4 above. <br><br>
We have tried various special data, from various locations on Earth, to special date and time such as crossing year and crossing month, apart from the errors caused by the translation issues mentioned above, we have not found any problems in the testing. As long as users ensure that the input longitude and latitude coordinates are accurate, the input date, time, and time zone are all specified by the local authorities, the generated celestial sphere can always meet the simulation results of Stellarium under the same conditions. <br><br>

<br>
<center>———— Contents below may be referenced by the developers ————</center>

## Chapter 3&emsp;File Structure

### 1. File Conponents
+ Scientific and Precision Astronomical System

    + [ \_\_pycache\_\_ ](Auto-Generate while running)
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


### 2. File Functions
+ What is in the \_\_pycache\_\_ Folder are cache files generated during code execution<br>

+ The Database folder stores the data that needs to be read and written during code execution, among this folder:<br>

    + 001_The original SAO Star Catalog (just act as a back-up here).txt
        + It is the original SAO star catalog file, which is kept as a backup for developers, sourced from : https://heasarc.gsfc.nasa.gov/W3Browse/star-catalog/sao.html<br><br>

    + 002_Document of the original SAO Star Catalog.txt
        + It is the official explanation documentation for the SAO star catalog mentioned above, which is kept as a backup for developers and comes from the same source as the SAO catalog<br><br>

    + 003_Sorted SAO Star Catalog (sort accroding to the star's visual magnitude).txt
        + It is the pre-processed SAO star catalog using Python, the star SAO numbers, declination and declination in the J2000.0 era, visual magnitude, and spectral types were extracted from the original catalog, and sorted according to brightness from high to low (visual magnitude from small to large)<br><br>

    + 004_Parameters obtained from UI panel.csv
        + This file is used to store user parameter inputs in the panel<br><br>

    + 005_Pre-Operated index to generate code for Blender.csv
        + This file stores the calculated star (x,y,z) Cartesian coordinates, which are calculated from the right ascension, right ascension, and celestial radius (user-defined) by converting the spherical coordinate system to the Cartesian coordinate system; Assuming the user chooses to generate n stars, n+10 pieces of data will be calculated and stored in this file. The additional 10 pieces are to avoid errors caused by easily overlooked issues<br><br>

+ ephem is an open-source Python library responsible for astronomical calculations. Here, only some of the core content will be explained. For more information, please refer to the ephem project address: https://rhodesmill.org/pyephem/

    + \_\_init\_\_.py 
        + Due to the fact that the ephem library is written in C language, its computational core is actually compiled from several C language files and header files `_libastro.cp310-win_amd64.pyd` file. Here, the \_\_init\_\_.py is mainly to access variables in the .pyd file, call functions within it, etc.<br><br>
    
    + _libastro.cp310-win_amd64.pyd<br>_libastro.pyd
        + Directly using the downloaded ephem library folder will run the \_\_init\_\_.py's `import _libastro` with an error stating that `the .pyd file could not be found`. So we just rename the original `_libastro.cp310 win_amd64.pyd` file to `_libastro.pyd` . We have two comments in the \_\_init\_\_.py. <br><br>Also, please note that through Blender 3.2 to Blender 3.6, all of them use Python 3.10 and support CPython, hence we choose the `ephem 4.1.4 CP310` version. If you need to migrate this project to another Python version of Blender, please change it to the ephem library with the `_libastro.cpXXX win_amd64.pyd` core that uses the corresponding CP version number, otherwise, an error will be reported that the DLL file cannot be found.<br><br>
        
    + cities.py<br>stars.py
        + Stored some related city and star data preset in the ephem library correspondingly

    + tests
        + This folder stores some ephem test code and NASA JPL ephemeris used for calculations<br><br>
        

+ \_\_init\_\_.py
    + Blender's standardized formats for creating add-on and registration files<br><br>

+ A_Generate_UI.py
    + Generate the UI panel, read and store user's input data on the panel, and define two button's operations<br><br>

+ B_Preparing_the_Blender_Scene.py
    + Initialize the Blender world and create the necessary collections, objects, and materials. The specific functions will be expanded in the next chapter<br><br>

+ C_Convert_star_info.py
    + Call the star catalog data and user input data in the Database folder, calculate the (x, y, z) Cartesian coordinates of the star in Blender, the correspondence between visual magnitude and scale coefficient, spectral type and self luminous color, based on the star's right ascension and declination, user input celestial sphere radius, and amount of to-be-generated stars<br><br>

+ D_Generate_the_stars.py
    + Generate the required number of stars for the user, where the celestial sphere is "polar lying on the x-axis", where (r,0,0) is the northern celestial pole, (0,0,-r) is the vernal equinox, and (0,0,r) is the autumnal equinox; Therefore, it will also calculate the time angle, rotate the celestial sphere to the current time angle, and rotate the celestial sphere to the current elevation angle based on latitude<br><br>

+ E_Generate_Sun_Moon_Planet.py
    + Accroding to user's selection, generate corresponding solar system celestial bodies and offset the rotation axis of each celestial body to its true situation, and set lunar tidal locking; For all selected celestial bodies except the sun (regardless of whether the user chooses to generate the sun), add illumination from the direction of the sun<br><br>

## Chapter 4&emsp;Code Implementation Principles

*We only record the general idea here, for technical details and algorithm, please refer to the comments in the code, where many have been written. For the calling method and code writing format of the ephem library, please refer to the ephem official website: https://rhodesmill.org/pyephem/*

### Extra-Solar-System star
+ **1. Generation of stars**

    We extracted the SAO numbers, declination & declination in the J2000.0 era, visual magnitude, spectral type data of 258997 stars, stored in `001_The original SAO Star Catalog (just act as a back-up here).txt` in folder Database. Then sorted them by star brightness from high to low, storing the outcome in `003_Sorted SAO Star Catalog (sort accroding to the star's visual magnitude).txt`.<br><br> **The first step is to generate the required number of stars on a virtual sphere - the celestial sphere**.<br><br> The principle of generating stars is that when you click the "Initialize World" button, `B_Preparing_the_Blender_Scene.py` will execute, programmatically creating nine standard stars in the world and assigning different colors of self-luminous materials. Color and spectral type are related, so subsequent generation of stars only needs to instantiate a standard star based on their spectral type, calculate the proportion according to the mapping formula from the visual magnitude to the scale coefficient, scale it (we distinguish the brightness of the stars by size), and then move it to the corresponding position.<br><br>This position calculation is achieved by treating the right ascension, right ascension, and right ascension as spherical coordinates, and applying mathematical formulas to convert them into Cartesian coordinates; The radius of this celestial sphere is also set by the user , which is directly used as the radius of the spherical coordinate system. <br><br> The code for the coordinate system conversion section is located in `C_Convert_star_info.py`, the conversion results are stored in `Database\004_Parameters obtained from UI panel.csv`, the code for the instantiation part is in the beginning of `D_Generate_the_stars.py`.<br><br> **There are two points that need to be noted which are easily overlooked:**<br>
    + **球坐标系转直角坐标系**<br>

        The formula for transforming from the spherical coordinate system (r,θ,φ) to the Cartesian coordinate system (x, y, z) is:<br><br>

        <center>

        $$
        \begin{cases}
        x\enspace=\enspace rsinθcosφ\\
        y\enspace=\enspace rsinθsinφ\\
        z\enspace=\enspace rcosθ
        \end{cases}
        $$

        </center>

        <br>
        The form of right ascension, declination, and radius is (directly using the radian system of the SAO catalog, instead of the "hour minute second" or "degree minute second" formats):<br><br>

        <center>

        $$
        \begin{cases}
        Right ascension Ra\enspace=\enspace a\enspace(rad)\\
        Declination Dec\enspace=\enspace b\enspace(rad)\\
        Radius r\enspace=\enspace c\enspace(米)
        \end{cases}
        $$

        </center>

        <br>If we directly consider the right ascension as φ, Regard declination as θ, problems may arise:<br><br>
        **About φ**<br><br>In the universal right hand coordinate system, the spherical coordinate system φ angle is actually from the+x-axis to the+y-axis, which means that if the line of sight looks down in the - z direction,  the φ angle increases counterclockwise. This is the same numbering method as the celestial right ascension, because when viewed from above the northern celestial pole, the right ascension also increases counterclockwise.<br><br> However, this regulation is opposite to the azimuth angle of a geographic coordinate system. The geographic azimuth angle is usually 0 ° due north, and it rotates from due north to due east, which means that when viewed from above, the geographic azimuth angle increases clockwise.<br><br> Therefore, if the+x axis is the true north direction and the azimuth and altitude angles of the geographic coordinate system need to be used to generate Cartesian coordinates, the azimuth angle should be taken as the opposite number (according to the principle of arbitrary angle in mathematics) in order to be used as φ and participate in calculations.<br><br>

        **About θ**<br><br>This θ It is the angle between the radius vector of a point P on the sphere and the +z axis, rather than the elevation angle of the radius vector relative to the xoy plane. Therefore, whether it is the elevation of a geographic coordinate system or the declination, it must be subtracted by π/2 in order to be θ and participate in calculations, such as θ = π/2 - Dec<br><br>

    + **The initial celestial state**<br>
    
        *Please refer to the code comments for details of this section*<br>
        The celestial sphere generated by the above method has a polar axis that coincides with the +z axis, meaning that the northern celestial pole is at (0,0, r). This is not conducive to making adjustments based on latitude in the future, as the North Celestial Pole should be at the same elevation as the latitude. At this point, the default elevation should be 0, which should be rotated if necessary. So this celestial sphere should also rotate 90 degrees around the y-axis from +z to +x direction, and the original point D (x0, y0, z0) will become a new point D '(x, y, z)=(z0, y0, -x0) <br><br>

+ **2. Rotating celestial sphere**

    Obviously, the celestial sphere generated through the above process is a celestial sphere on the Earth's equator with a time angle of 0, that is, the northern celestial pole at (r, 0,0), the vernal equinox at (0,0, - r), and the autumnal equinox at (0,0, r). To obtain the celestial sphere with a set time and location, we need to rotate it twice, the first time around the polar axis (+x axis) to rotate the time angle, and the second time around the y-axis to rotate the elevation angle of the north celestial pole.<br><br>
    This part of the code is in the ending part of `D_Generate_the_stars.py` .

    + **Calculate time angle**<br><br>
        We were not feel like to write those low-precision time angle estimation formulas, so we directly called the built-in stellar bright star library of ephem and selected Sirius, the brightest star in the sky, as the calculation target. We used ephem to calculate the azimuth and altitude angles of Sirius at the set time and location (as the azimuth here is a geographical azimuth, we need to take the opposite number to be used as the φ participating in the calculation, as explained earlier)<br><br>
        It should be noted that the location used for ephem calculation here has a longitude equal to the user input, but a latitude of 0 ° is used because the celestial sphere at this time is still "on the Earth's equator with a time angle of 0". At this step we only calculate the time angle at the equator and does not consider latitude issues temporarily<br><br>
        The Sirius calculated in this way, relative to its initial state, should only have rotated one angle around the polar axis (x-axis), in real time. This angle can be calculated using  `arctan(after Z / after Y) - arctan(before Z / before Y)` . Then select all the stars in the entire celestial sphere, and rotate the negative value of the angle around the x-axis . <br><br>
        Why is it a negative value? I can't figure it out, maybe it's a matter of perspective? The rotation angle calculated using the above formula is the yoz plane Cartesian coordinate system facing the -x direction, while the rotation is calculated using the angle facing +x? But in short, adding a minus sign to complete the conversion is right anyway......
    
    + **Rotating elevation angle**<br><br>
        The north celestial pole should be at the same elevation as the latitude, so after turning the time angle, just directly rotate the local latitude around the y-axis

### Celestial bodies in Solar System

+ **Append bodies**<br><br>
    To simplify code, solar system celestial bodies are not generated programmatically, but are directly added from the preset file A. When celestial bodies are added to the world, they also involve their own materials, textures, and collection nodes into the Blender file to prepare for subsequent operations<br><br>
    Source of celestial model:<br>
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
    For the required celestial bodies, they will be moved to the specified position after being added. The position calculation method is to calculate the azimuth and altitude angles of the target celestial body using the set time and location by ephem, and then convert them into Cartesian coordinates<br><br>
    To increase authenticity, each body's the visual diameter (in angular seconds) calculated by ephem is multiplied by the radius of the spherical surface to obtain the visual diameter (in meters), which is then scaled to restore its true visual size<br><br>
    Here, we choose to let different types of solar system celestial bodies move on spheres of different radii. Assuming the radius of the celestial sphere is set to r, the radius of the sphere where planets and Pluto are located is 0.98r, the radius of the sun is 0.96r, and the radius of the moon is 0.94r. This can form a certain occlusion relationship, achieving phenomena such as solar eclipses, planets being eclipsed by the moon, and planets being eclipsed by the sun; But at the same time, there are also some things that are destined to be impossible to achieve, such as lunar eclipses and planetary transits. The former, because the "Earth" here is not a physical entity, cannot block the moon from forming a lunar eclipse in its shadow; The latter is because the planet's sphere is located outside the sun's sphere, and there is never a chance to block the sun <br><br>
    In future versions, we may fix these issues, such as reconstructing the solar system to a true scale instead of placing all solar system objects on virtual celestial spheres. This will theoretically support all astronomical phenomena, except for lunar eclipses, as "Earth" is still the coordinate system in Blender and there are no entities that can cast shadows

+ **Align Axis**<br><br>
    To restore the astronomical phenomena of solar system celestial bodies, rather than manually writing visual effects code, it is better to directly orient the polar axis (+z axis of the local coordinate system of the celestial model) of all solar system celestial bodies towards their true direction. In this way, when the relative position of celestial bodies and the Earth changes, phenomena such as lunar libration and annual apparent motion of Saturn's ring tilt will naturally be observed, which is consistent with the formation mechanism of astronomical phenomena in the real solar system<br><br>
    In addition, the moon has one more step of tidal locking, so that the front of the moon (the+x-axis of the lunar local coordinate system) always points towards the Earth while rotating around the +z axis<br><br>
    The above two things can be achieved through the "Align euler to vector" geometry node of the celestial body when adding:<br><br>
    Simply copy the readily available "North Celestial Pole" right ascension and declination of the target celestial body in Stellarium. Use the "Fixedbody()" function of the ephem library to register as a "virtual star", which is the "North Polar Star" of the target celestial body. Calculate the elecation angle and azimuth angle of the "virtual star" at the set time and place, convert them into Cartesian coordinates, and use them as the vector to align the polar axis (vector parallel)<br><br>
    Similarly to tidal locking, the vector that the+x-axis of the lunar local coordinate system needs to align with is the vector that the moon points towards the Earth. Therefore, taking the opposite number of lunar Cartesian coordinates and inverting it is sufficient<br><br>

+ **Add sunlight**<br><br>
    All celestial bodies in the solar system (except for the sun itself) are illuminated by sunlight. Blender 3.2- Blender 3.6 versions do not yet support light exclusion unless other visual layers are used, but that will seriously affect the convenience of plugin usage. We simply equipped each celestial body with a "lamp" to simulate the effect of receiving sunlight in the sunshine area<br><br>
    After experimenting in Blender, it was found that assuming A is the apparent diameter of the celestial body (in meters), placing a point light at a distance of 2A from the celestial body on the line between the sun and the celestial body, with a radius of 1.2A, can simulate the effect of the celestial body being illuminated by half of the sunlight. This part can also be completed through vector calculation, and the brightness of point light is assigned according to different celestial bodies<br><br>
    This point light is generated using an independent ephem sun instance calculation, so regardless of whether the user chooses to generate the sun or not, it does not affect the creation of the correct orientation point light

### World Environment

+ **Sky texture**<br>

    We used Blender's built-in sky texture to simulate the Earth's sky during day or night. This world environment node is also appended from the preset file `3DModelAppend.blend`. In the sky texture node, the sun's orientation and height are also calculated using independent ephem sun instances, so whether the user chooses to generate the sun or not does not affect the correct position of the sun in the sky texture. In addition, during daylight, the light in the sky's texture is bright enough to submerge the stars, which can be considered a more realistic representation of the sky during daylight.

+ **Default environment color**<br>

    If the user does not need the sky lighting effect of the atmosphere when there is sunlight, they can disconnect the connection between the "sky texture" and the "background", and the default world background color is black (# 000000).<br><br>

## Chapter 5 The Scattered Operations That Need To Be Clarified
### Path absolutization
When using relative paths in the same folder, errors will always be reported in Blender. Therefore, the code adopts path absolute operation, which is to obtain the path of the current. py file through `currentPyFilePath=os.path.abspath (__file__)`, and then obtain the folder where the current. py file is located through `parentPyFilePath=os.path.dirname (currentPyFilePath)` (all files in the entire plugin are here), followed by using `os.path.join (...)` to connect to the previous relative path `parentPyFilePath`,

### sys.path.append (......)
Blender always cannot find the ephem library in the same folder, so each time it runs, it will add the current folder to the system path found by Blender Python. exe in the execution of file `__init__.py`

### Greenwich Mean Time
ephem uses Greenwich Mean Time (GMT) as the time input for astronomical calculations, but it does not guarantee that everyone using the plugin knows how to obtain Greenwich Mean Time. This is why the panel requires selecting a time zone and entering the local time, and the program is responsible for calculating Greenwich Mean Time
Unfortunately, whenever ephem involves a date conversion issue of "going back one year or one month", it will make an error, as detailed in the relevant notes in `A_Generate_UI.py`

### Clip end
The radius of the celestial sphere may be very large. To avoid some users finding that the image is missing the distant view and not knowing how to adjust it, the cutting end point of the view is directly preset in the code for all windows: <br>

```Python
    # Set the end point of view clip end to20000m
    # Reference：https://blender.stackexchange.com/questions/265858/
    screens = (s for w in bpy.data.workspaces for s in w.screens)
    V3Dareas = (a for s in screens for a in s.areas if a.type=='VIEW_3D')
    V3Dspaces = (s for a in V3Dareas for s in a.spaces if s.type=='VIEW_3D')
    for space in V3Dspaces:
        space.clip_end = 20000 
```

However, this still cannot solve the problem during rendering. After adding a camera, users need to set a value greater than the radius of the celestial sphere in the "Camera Object Properties - Lens - End Point" section.

### Code comment translation and README translation
The comments for this version of open source code are written in Chinese without English translation. Developers may need to use a translator to read it.<br><br>
Some English marks has been added in some easily confused places, such as marking "meters" where the unit "meter" is mentioned, 'cause the unit "meter" in Chinese is "米", which may be mistranslated to its second meaning "rice".<br><br>
A large fraction in translating README to English has been done in machine translation, though I managed to read each sentence to correct the faults, it's still not perfect anyway.<br><br>
If the add-on gains some popularity in the future, we will consider providing more support on translation issues.<br><br>

<center>

<font size=5>

**致无尽蔚蓝与星汉灿烂！**<br>
**TO INFINITE AZURE & STARRY OCEAN!**

</font>

</center>