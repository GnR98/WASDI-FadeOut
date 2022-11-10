# Data manipulation Classes

## Design Requirement Specification Document

DIBRIS – Università di Genova. Scuola Politecnica, Corso di Ingegneria del Software 80154

**Authors**  
Roberto Gnisci<br/>
Matteo Aicardi

### REVISION HISTORY

<p>
  CoordinateChecker History
  </br>
</p>

| Version    | Date        | Authors      | Notes        |
| ----------- | ----------- | ----------- | ----------- |
| 1.0 | 18/9/2022 |M. Aicardi, R. Gnisci | First CoordinateChecker update|
| 1.1 | 28/9/2022 |M. Aicardi, R. Gnisci | Second CoordinateChecker update |
| 1.2 | 7/10/2022 |M. Aicardi, R. Gnisci | Third CoordinateChecker update |
| 1.3 | 10/10/2022 |M. Aicardi, R. Gnisci | Fourth CoordinateChecker update |
| 1.4 | 25/10/2022 |M. Aicardi, R. Gnisci | Fifth CoordinateChecker update |
| 1.5 | 5/11/2022 |M. Aicardi, R. Gnisci | Sixth CoordinateChecker update |
| 1.6 | 9/11/2022 |M. Aicardi, R. Gnisci | Final CoordinateChecker update |

<p>
  </br>
  WeatherScraper History
  </br>
</p>

| Version    | Date        | Authors      | Notes        |
| ----------- | ----------- | ----------- | ----------- |
| 1.0 | 17/8/2022 |M. Aicardi, R. Gnisci | First WeatherScraper update |
| 1.1 | 25/8/2022 |M. Aicardi, R. Gnisci | Second WeatherScraper update |
| 1.2 | 31/8/2022 |M. Aicardi, R. Gnisci | Third WeatherScraper update |
| 1.3 | 10/9/2022 |M. Aicardi, R. Gnisci | Fourth WeatherScraper update |
| 1.4 | 20/9/2022 |M. Aicardi, R. Gnisci | Fifth WeatherScraper update |
| 1.5 | 10/10/2022 |M. Aicardi, R. Gnisci | Sixth WeatherScraper update |
| 1.5 | 18/10/2022 |M. Aicardi, R. Gnisci | Seventh WeatherScraper update |
| 1.5 | 25/10/2022 |M. Aicardi, R. Gnisci | Eight WeatherScraper update |
| 1.5 | 6/11/2022 |M. Aicardi, R. Gnisci | Ninth WeatherScraper update |
| 1.5 | 9/11/2022 |M. Aicardi, R. Gnisci | Final WeatherScraper update |

<p>
  </br>
  ShapeFileProjection History
  </br>
</p>

| Version    | Date        | Authors      | Notes        |
| ----------- | ----------- | ----------- | ----------- |
| 1.0 | 10/10/2022 |M. Aicardi, R. Gnisci | First ShapeFileProjection update |
| 1.1 | 12/10/2022 |M. Aicardi, R. Gnisci | Second ShapeFileProjection update |
| 1.2 | 14/10/2022 |M. Aicardi, R. Gnisci | Third ShapeFileProjection update |
| 1.3 | 18/10/2022 |M. Aicardi, R. Gnisci | Fourth ShapeFileProjection update |
| 1.4 | 20/10/2022 |M. Aicardi, R. Gnisci | Fifth ShapeFileProjection update |
| 1.5 | 25/10/2022 |M. Aicardi, R. Gnisci | Final ShapeFileProjection update |


## Table of Content

1. [Introduction](#intro)
    1. [Purpose and Scope](#purpose)  
    2. [Definitions](#def)
    3. [Document Overview](#overview)
    4. [Bibliography](#biblio)
2. [Project Description](#description)
    1. [Project Introduction](#project-intro)
    2. [Technologies used](#tech)
    3. [Assumptions and Constraints](#constraints)
3. [System Overview](#system-overview)
    1. [System Architecture](#architecture)
    2. [System Interfaces](#interfaces)
    3. [System Data](#data)
        1. [System Inputs](#inputs)
        2. [System Outputs](#outputs)
4. [System Module 1](#sys-module-1)
    1. [Structural Diagrams](#sd)
        1. [Class Diagram](#cd)
            1. [Class Description](#cd-description)
        2. [Object Diagram](#od)
        3. [Dynamic Models](#dm)
5. [System Module 2](#sys-module-2)
   1. ...

##  <a name="intro"></a>  1 Introduction

    
### <a name="purpose"></a> 1.1 Purpose and Scope
<details> 
    <summary> These classes are used to correct, filter and improve an already existing excel database </summary>
    <p>
      This is needed to supply a good enough dataset to train a Machine Learning model that aims to recognize if a water leak has happened near a pipe network
      analyzing satellitar images of the area.
      </br>
      Each class serves a precise purpose:
    </p>
    <p>
      CoordinateChecker corrects errors in the coordinates inside the database (while also correcting the latitude and longitude)
    </p>
    <p>
      WeatherScraper fetches weather data and creates a "new" database containing these informations, making filtering good cases from bad cases
      (a bad case would be if it rained when a leak was detected) easier
   </p>
   <p>
      ShapefileProjection aims to improve the coordinates given in the database by projecting them directly onto the pipe network
      (useful for example in case of multiple nearby pipes)
   </p>
  
    
</details>

### <a name="def"></a> 1.2 Definitions
    
| Name				| Definition | 
| ------------------------------------- | ----------- | 
| NOMINATIM API                                  | Interface used to check and eventually fetch the coordinates|
| METEOSTAT API                                  | Interface used to collect weather data|
| EPSG 32632                                     | Coordinate reference system used in the original pipe network file |
| WGS84/EPSG 4326                                | Coordinate reference system needed to use the projection algorithm|
| WASDI                                          | Web Advanced Space Developer Interface |
    
</details>


### <a name="biblio"></a> 1.3 Bibliography
<details> 
    <summary> Libraries and references Used
    </summary>
    <p>
      https://pandas.pydata.org/ (Pandas to read and write Excel files)
    </p>
    <p>
      https://geopy.readthedocs.io/en/stable/ (Geopy NOMINATIM API, used to do the geocoding operations)
	  </p>
    <p>
	    https://dev.meteostat.net/python/#installation (METEOSTAT library webpage, used to fetch weather data)
	  </p>
    <p>
	    https://pyproj4.github.io/pyproj/stable/ (pyproj, used to change the coordinate reference system of the shapefiles )
	  </p>
    <p>
	    https://shapely.readthedocs.io/en/maint-1.8/ (shapely library,  execute the projection operations on a shapefile)
	  </p>
    <p>
        https://docs.python.org/3/library/os.html
    </p>
    <p>
        https://docs.python.org/3/library/pathlib.html?highlight=pathlib#module-pathlib (os and Path libraries have been used to manage internal paths)
    </p>
    <p>
        https://docs.python.org/3/library/datetime.html (datetime library used to manage dates)
    </p>
    <p>
      https://docs.python.org/3/library/math.html (math library, basically used only to check for NaN)
    </p>
    <p>
      https://docs.python.org/3/library/json.html?highlight=json#module-json (json library, used to load input parameters from a json file)
    </p>
    <p>
      https://pypi.org/project/Fiona/ (Fiona library, used to open and write on a shapefile)
    </p>
      
    
</details>

## <a name="description"></a> 2 Project Description

### <a name="project-intro"></a> 2.1 Project Introduction 
<ul>
	<li>CoordinateChecker:
		<p>
			ckecks in the leaks database excel file if the pairs of coordinates are correct and, if a pair is outstandingly wrong than an
			approximation is computed and substituted.
		</p>
	<li>WeatherScraper: 
		<p>
			reads from an Excel leaks database where and when a leak occured, then fetches precipitation data of a given period of time for that
			place. The class also approximately recognizes if apair of coordinates reside in a city, a town or a village
		</p>
	<li>ShapeFileProjection: 
		<p>
			reads from the leaks Excel database where a network intervention occured and then projects the obtained coordinates on the pipe
			network.The algorithm inside the class needs a specific coordinate reference system and is able to change the one used in the pipe
			network file to meet this constraint.
		</p>
</ul>

### <a name="tech"></a> 2.2 Technologies used

<details> 
    <summary> Software used to develope the algorithm </summary>
    <p>
        https://www.jetbrains.com/pycharm/  (PyCharm IDE)
    </p>
    <p>
      https://www.microsoft.com/it-it/microsoft-365/excel (Microsoft Excel since the database is given as an Excel file)
    </p>
    <p>
	    https://mapshaper.org/ (mapshaper website to visualize shapefiles)
    </p>
</details>

### <a name="constraints"></a> 2.3 Assumption and Constraint 
<details> 
    <summary> There are both assumptions and constraints
    </summary>
    <p>
      </br>
      Each class was created assuming that a specificly formatted Excel file would be given as input, thus they will not work with differently formatted files
    </p>
    <p>
      No strict time constraints were given for the algorithms, as such some functions may take a while if the Excel file has a lot of rows
    </p>
    <p>
      The user must be able to connect to Internet
    </p>
    <p>
      For the correction algorithm the only row values that may be oncorrect are the ones regarding the latitude/longitude and the date on which the repairings were finished
    </p>
  
</details>

## <a name="system-overview"></a>  3 System Overview
<details> 
    <summary> Put a summary of the section
    </summary>
    <p>This sub section should describe ...</p>
</details>

### <a name="architecture"></a>  3.1 System Architecture
<details> 
    <summary> Put a summary of the section
    </summary>
    <p>This sub section should describe ...</p>
</details>

### <a name="interfaces"></a>  3.2 System Interfaces
<details> 
    <summary> Put a summary of the section
    </summary>
    <p>This sub section should describe ...</p>
</details>

### <a name="data"></a>  3.3 System Data
<details> 
    <summary> Put a summary of the section
    </summary>
    <p>This sub section should describe ...</p>
</details>

#### <a name="inputs"></a>  3.3.1 System Inputs
<details> 
    <summary> Put a summary of the section
    </summary>
    <p>This sub section should describe ...</p>
</details>

#### <a name="outputs"></a>  3.3.2 System Ouputs
<details> 
    <summary> Put a summary of the section
    </summary>
    <p>This sub section should describe ...</p>
</details>

## <a name="sys-module-1"></a>  4 System Module 1
<details> 
    <summary> Put a summary of the section
    </summary>
    <p>This sub section should describe ...</p>
</details>

### <a name="sd"></a>  4.1 Structural Diagrams
<details> 
    <summary> Put a summary of the section
    </summary>
    <p>This sub section should describe ...</p>
</details>

#### <a name="cd"></a>  4.1.1 Class diagram
<details> 
    <summary> Put a summary of the section
    </summary>
    <p>This sub section should describe ...</p>
</details>

##### <a name="cd-description"></a>  4.1.1.1 Class Description
<details> 
    <summary> Put a summary of the section
    </summary>
    <p>This sub section should describe ...</p>
</details>

#### <a name="od"></a>  4.1.2 Object diagram
<details> 
    <summary> Put a summary of the section
    </summary>
    <p>This sub section should describe ...</p>
</details>

#### <a name="dm"></a>  4.2 Dynamic Models
<details> 
    <summary> Put a summary of the section
    </summary>
    <p>This sub section should describe ...</p>
</details>
