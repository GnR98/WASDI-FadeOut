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
| 1.5 | 25/10/2022 |M. Aicardi, R. Gnisci | Sixth ShapeFileProjection update |
| 1.6 | 3/11/2022 |M. Aicardi, R. Gnisci | Seventh ShapeFileProjection update |
| 1.7 | 7/11/2022 |M. Aicardi, R. Gnisci | Eighth ShapeFileProjection update |
| 1.8 | 14/11/2022 |M. Aicardi, R. Gnisci | Final ShapeFileProjection update |


## Table of Content

1. [Introduction](#intro)
    1. [Purpose and Scope](#purpose)  
    2. [Definitions](#def)
    3. [Bibliography](#biblio)
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
        2. [Dynamic Models](#dm)


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
      For the correction algorithm the only row values that may be incorrect are the ones regarding the latitude/longitude and the date on which the repairings were finished
    </p>
    <p>
      For the correction algorithm if in a row the coordinates are not correct and the address contains only the city, the algorithm will assume that the city is in Italy
    </p>
    
  
</details>

## <a name="system-overview"></a>  3 System Overview


### <a name="architecture"></a>  3.1 System Architecture
<details> 
    <summary> Diagram of how the system architecture composed by the three classes
    </summary>
     <img src="imgs/ScriptSA.png" alt="ScriptSA" style="float: left; margin-right: 10px;" />
</details>

### <a name="interfaces"></a>  3.2 System Interfaces
<p>These classes do not have a real UI and are mostly executed via terminal.
</br>
</br>
Each class, if launched as a standalone program, supports typing manually the inputs instead of creating a json file
</p>


## <a name="data"></a>  3.3 System Data


### <a name="inputs"></a>  3.3.1 System Inputs
<details> 
    <summary> Details of the inputs for each class
    </summary>
    <p>
	</br>
	CoordinateChecker:
	    <ul>
		    <li>The location of the Excel database
	</ul>
    </p>
    <p>
	WeatherScraper (each parameter can also be specified in a json file):
	<ul>
		<li>The location of the Excel database     (EXCELLOC)
		<li>The number of days before the repair date on which you want to fecth weather data    (DAYSBEFORE)
		<li>The number of days after the repair date on which you want to fecth weather data    (DAYSAFTER)
		<li>The district of which it is desired to obtain weather data    (DISTRICT)
	</ul>
    </p>
    <p>
	ShapeFileProjection (each parameter can also be specified in a json file):
	<ul>
		<li>The location of the Excel database     (EXCELLOC)
		<li>The location of the Shapefile    (SHAPELOC)
		<li>The district of which it is desired to obtain projected coordinates for each row     (DISTRICT)
	</ul>
   </p>
</details>

### <a name="outputs"></a>  3.3.2 System Ouputs
<details> 
    <summary> Details of the output for each class
    </summary>
     <p>
	</br>
	CoordinateChecker:
	    <ul>
	            A new Excel file with the same columns as the original
            </ul>
     </p>
     <p>
	WeatherScraper:
	<ul>
		<p>
		A new Excel file with the following columns (format of column_name:: explanation)
		</p>
		<li>Comune::  Same as in the original Excel   
		<li>Data Inizio Esito::  Same as in the original Excel
		<li>COORD_X SNAPSHOT GIS (LAT)::  Same as in the original Excel
		<li>COORD_Y SNAPSHOT GIS (LNG)::  Same as in the original Excel
		<li>Precipitations (in mm), from <DAYSBEFORE> days before (in ascending order of date):: Real number array containing weather data in the days before the repair (including that day), can contain nan values
		<li>Precipitations (in mm), until <DAYSAFTER> days after (in ascending order of date)::  Real number array weather data in the days after the repair (including that day), can contain nan values
		<li>Mean precipitation value in the <DAYSBEFORE> days before the repair date (in mm):: Mean value calculated without considering nan values, can be nan if all the values in the precipitation cell are nan
		<li>Mean precipitation value in the <DAYSAFTER> days after the repair date (in mm):: Mean value calculated without considering nan values, can be nan if all the values in the precipitation cell are nan
		<li>Type of location:: A string that may be "city","town" or "village" depending to which the location belongs
		<li>Name of location:: A string containing the name of the location (may be different from the district)
		<li>Did it rain before the repair date ?:: Boolean value indicating if it has rained before the repair, can be nan if all the values in the precipitation cell are nan
		<li>Did it rain after the repair date ?:: Boolean value indicating if it has rained after the repair, can be nan if all the values in the precipitation cell are nan
	</ul>
    </p>
    <p>
	ShapeFileProjection:
	<ul>
		<p>
		Shapefile conversion:
		</p>
		<li>Changes the origial shapefile coordinate reference system without creating a new file
	</ul>
			</br>
	<ul>
		<p>
			Shapefile projection:
		</p>
		<p>
		        Creates a new Excel file with the following columns (format of column_name:: explanation)
		</p>
		<li>Intervento:: Same as in the original Excel
		<li>Comune:: Same as in the original Excel	
		<li>Indirizzo:: Same as in the original Excel
		<li>Civico:: Same as in the original Excel
		<li>Note Esecutore:: Same as the original
		<li>Data Inizio Esito:: Same as in the original Excel
		<li>Data fine:: Same as in the original Excel
		<li>ID SNAPSHOT:: Same as in the original Excel
		<li>COORD_X SNAPSHOT GIS (LAT):: Latitude of the projected point on the shapefile (closest point on the same address)
		<li>COORD_Y SNAPSHOT GIS (LNG):: Longitude of the projected point on the shapefile (closest point on the same address)
		<li>COORDINATE RISULTANTI:: Same as in the original Excel
	</ul>			
    </p>
</details>

## <a name="sys-module-1"></a>  4 System Module 1
<details> 
    <summary> CoordinateChecker summary
    </summary>
    <p>This class is used to fix all the possible error inside the excel Coordinate file in input, such as LNG and LAT columns inverted 
    and inconsistent coordinate values respect them street name </p>
</details>
<details>
    <summary> WeatherScraper summary
    </summary>
    <p> This class fetch data about precipitations in a set of given places and dates. Taking into account the chosen place and the date ranges
 	it fecthes the precipitation data for every day between (reparation date-daysBefore) and (reparation date+daysAfter). 
	Additional information are added such as the mean value for the past and future days, a boolean variable that tells whether it has rained or not before or 	   after the reparation date, and the type of place (city,town,village). A new excel file will be created with all the relevant columns
   </p>
</details>
<details>
    <summary> ShapefileProjection summary
    </summary>
    <p> This class calculates all the projections on the main pipes of the works performed, it also has a functionality 
    to fix problems inside the shapefile in input such as different coordinate reference system (converted into epsg-4326) and wrong
    addresses with respect to coordinates.
   </p>
</details>

### <a name="sd"></a>  4.1 Structural Diagrams

#### <a name="cd"></a>  4.1.1 Class diagram
<details> 
    <summary> Class diagram for all the classes 
    </summary>
    <img src="imgs/ScriptsUML.png" alt="ScriptsUML" style="float: left; margin-right: 10px;" />

</details>

##### <a name="cd-description"></a>  4.1.1.1 Class Description
<details> 
    <summary> CoordinateChecker Class description
    </summary>
    <p>Attributes:</p>
	<ul>
		<li> sheet : excel file in input.
		<li> geolocator : object instance from the geopy library, used to convert the coordinate into address and viceversa.
	</ul>
    <p>Methods:</p>
	<ul>
		<li> Checker : main method of the class, it checks if the coordinates in the excel files are correct and if they are not,
        		      corrects them. A new file NewGeolocation.xlsx will be created in the project folder.
		<li> util :  method used to correct the coordinates by using the do_geocode method and then substituting the newly obtained
        		    coordinates in the i-th row.
		<li> do_geocode : given an address this method will return the respective coordinate (refering to the WGS84 coordinate system),
			  	  recursive method that will try to get the result in a max of "max_attempts" retry.
		<li> do_reverse : given a coordinate (refering to the WGS84 coordinate system) this method will return the respective address,
			  	  recursive method that will try to get the result in a max of "max_attempts" retry.
	</ul>
			
</details>
<details> 
    <summary> WeatherScraper Class description
    </summary>
    <p>Attributes:</p>
	<ul>
		<li> sheet : excel file in input.
		<li> geolocator : object instance from the geopy library, used to convert the coordinate into address and viceversa.
	</ul>
    <p>Methods:</p>
	<ul>
		<li> WeatherStat : main method of the class, it calculates values and mean values of precipitations, if there were or not any precipitations and the 					location type, given a range date and a specific district present on the excel file in input.
		<li> do_reverse : given a coordinate (refering to the WGS84 coordinate system) this method will return the respective address,
			  	  recursive method that will try to get the result in a max of "max_attempts" retry.
	</ul>
			
</details>
<details> 
    <summary> ShapeFileProjection Class description
    </summary>
    <p>Attributes:</p>
	<ul>
		<li> sheet : excel file in input.
		<li> geod:  object instance from the pyproj library, used to calculate distance between line and point.
		<li> geolocator : object instance from the geopy library, used to convert the coordinate into address and viceversa.
		<li> dict: dictionary used to contains all the new projected coordinates calculated from the shapefile and the excel file.
	</ul>
    <p>Methods:</p>
	<ul>
		<li> getAllProjections : create a new Excel file with all the columns inside NewGeolocation plus two more 
		                         containing the coordinates of the projected points.
		<li> projectOnClosestPipe :  method used to calculate the nearest point to the working point belonging to the main line. 
		<li> convertShapefile :  convert and substitute the coordinates in the selected shapefile from EPSG 32632 to WGS84.
		<li> do_reverse : given a coordinate (refering to the WGS84 coordinate system) this method will return the respective address,
			  	  recursive method that will try to get the result in a max of "max_attempts" retry.
	</ul>
			
</details>

#### <a name="dm"></a>  4.2 Dynamic Models
<details> 
    <summary> CoordinateChecker Dynamic Model
    </summary>
    <img src="imgs/DynamicsCoordinatesChecker.png" alt="DynamicsCoordinatesChecker" style="float: left; margin-right: 10px;" />
</details>
<details> 
    <summary> WeatherScraper Dynamic Model
    </summary>
    <img src="imgs/DynamicWeatherScraper.png" alt="DynamicWeatherScraper" style="float: left; margin-right: 10px;" />

</details>
<details> 
    <summary> ShapefileProjection Dynamic Model
    </summary>
    <img src="imgs/DynamicShapeFileProjection.png" alt="DynamicShapeFileProjection" style="float: left; margin-right: 10px;" />

</details>

