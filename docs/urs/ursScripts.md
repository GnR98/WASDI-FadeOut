### User Requirements Specification Document for all the data related Classes
##### DIBRIS – Università di Genova. Scuola Politecnica, Software Engineering Course 80154


**VERSION : 1.0**

**Authors**  
Roberto Gnisci<br/>
Matteo Aicardi


**REVISION HISTORY**
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

# Table of Contents

1. [Introduction](#p1)
	1. [Document Scope](#sp1.1)
	2. [Definitios and Acronym](#sp1.2) 
	3. [References](#sp1.3)
2. [System Description](#p2)
	1. [Context and Motivation](#sp2.1)
	2. [Project Objectives](#sp2.2)
3. [Requirement](#p3)
 	1. [Stakeholders](#sp3.1)
 	2. [Functional Requirements](#sp3.2)
 	3. [Non-Functional Requirements](#sp3.3)
  
  

<a name="p1"></a>

## 1. Introduction
The present document describe the functional and non-functional requirements of multiple data manipulating classes. 
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

<a name="sp1.1"></a>

### 1.1 Document Scope
This document introduces the Requirement Analysis in Software Engineering for the course of Software Engineering at Laurea Magistrale in Computer Engineering in Genova. 


<a name="sp1.2"></a>

### 1.2 Definitios and Acronym


| Name				| Definition | 
| ------------------------------------- | ----------- | 
| NOMINATIM API                                  | Interface used to check and eventually fetch the coordinates|
| METEOSTAT API                                  | Interface used to collect weather data|
| EPSG 32632                                     | Coordinate reference system used in the original pipe network file |
| WGS84                                          | Coordinate reference system needed to use the projection algorithm|
| WASDI                                          | Web Advanced Space Developer Interface |

<a name="sp1.3"></a>

### 1.3 References 
<p>
	https://geopy.readthedocs.io/en/stable/ (Geopy NOMINATIM API)
	</br>
	https://dev.meteostat.net/python/#installation (METEOSTAT library webpage)
	</br>
	https://pyproj4.github.io/pyproj/stable/ (pyproj)
	</br>
	https://shapely.readthedocs.io/en/maint-1.8/ (shapely library)
	</br>
	https://mapshaper.org/ (mapshaper website to visualize shapefiles)
<a name="p2"></a>

## 2. System Description
<a name="sp2.15"></a>

### 2.1 Context and Motivation
<a name="sp2.2"></a>
WASDI operates in various fields including the development of an algorithm capable of recognizing if a water leak has happened near a pipe.
To achieve that they need to train a Machine Learning model with a correct dataset, part of this dataset is inside a database with coordinates of places where a leak has already occured and repaired. Correcting,improving and filtering the dataset are the objectives of the three classes described in the document.


### 2.2 Project Obectives 
<a name="p3"></a>
<p>
	CoordinateChecker creates an excel file with correct coordinates for every repair intervention.
</p>
<p>
	WeatherScraper creates an excel file with precipitation data for each repair intervention.
</p>
<p>
	ShapeFileProjection converts an existing shapefile Coordinate reference system into a more suitable one and then improves an existing excel file with a set of projected coordinates for every network intervention 
## 3. Requirements

| Priorità | Significato | 
| --------------- | ----------- | 
| M | **Mandatory:**   |
| D | **Desiderable:** |
| O | **Optional:**    |
| E | **future Enhancement:** |

<a name="sp3.1"></a>
### 3.1 Stakeholders
WASDI<br/>
FadeOut Software

<a name="sp3.2"></a>
### 3.2 Functional Requirements 
<p>
  CoordinateChecker
  </br>
</p>

| ID | Descrizione | Priorità |
| --------------- | ----------- | ---------- | 
| 1.0 | A CoordinateChecker function shall take in input the location of the excel file |M|
| 2.0 | The same function shall output a new Excel file named "NewGeolocation" |M|
| 2.1 | The "NewGeolocation" file must have the names of the coordinates columns corrected |M|
| 2.2 | The "NewGeolocation" file shall not have null values inside the coordinate columns |M|
| 3.0 | A CoordinateChecker function shall take in input a set of wrong coordinates |M|
| 3.1 | The same function shall correct them using the NOMINATIM API geocoding functions |M|
| 3.2 | The same function shall output the correct set of coordinates |M|

<p>
  </br>
  WeatherScraper 
  </br>
</p>

| ID | Descrizione | Priorità |
| --------------- | ----------- | ---------- | 
| 1.0 | A WeatherScraper function shall take in input the location of the Excel file |M|
| 2.0 | The same function shall take in input the number of days prior the repair date on which to search for data |M|
| 2.1 | The same function shall take in input the number of days following the repair date on which to search for data |M|
| 3.0 | The same function shall take in input the name of the district in order to search data only for the repairs done in the given district |M|
| 4.0 | The same function shall output a new Excel file |M|
| 4.1 | The new Excel file shall have two columns to collect precipitation data, one for the period of time before the repair date and one for the following period of time |M|
| 4.2 | The new Excel file shall have two columns (one for each semi-period of time) containig the mean value of the collected data|M|
| 4.3 | The new Excel file shall have two columns (one for each semi-period of time) containig a true/false/nan value that represents if it has rained in that period of time|O|
| 4.4 | The new Excel file shall have a column containing if the row's coordinates belong to a city,town or village|D|
| 5.0 | The standalone algorithm may take in input a json file containing all the inputs previously specified from point 1.0 to point 3.0 |D|

<p>
  </br>
  ShapeFileProjection 
  </br>
</p>

| ID | Descrizione | Priorità |
| --------------- | ----------- | ---------- | 
| 1.0 | A ShapeFileProjection function shall take in input the location of the Excel file |M|
| 2.0 | The same function shall take in input the location of the shapefile containing the locations of all the pipes |M|
| 3.0 | The same function shall take in input the name of the district in order to search data only for the repairs done in the given district |M|
| 4.0 | The same function shall consider only the interventions done on the pipe network.may take in a json file containing all the inputs previously specified |M|
| 5.0 | The same function shall output a new Excel file |M|
| 5.1 | The new Excel file shall have two new columns containing the set pf projected coordinates |M|
| 6.0 | The standalone algorithm may take in a json file containing all the inputs previously specified |D|
| 7.0 | A second ShapeFileProjection function shall take as input a shapefile with Coordinate reference system EPSG 32632|M|
| 8.0 | The same function shall change the Coordinate reference system of the input shapefile to WGS84|M|
| 9.0 | The same function shall create as output the new shapefile with WGS84 Coordinate reference system|M|


<a name="sp3.3"></a>
### 3.2 Non-Functional Requirements 
<p>
  CoordinateChecker
  </br>
</p>

| ID | Descrizione | Priorità |
| --------------- | ----------- | ---------- | 
| 1.0 |The output of the systems shall be created in the project folder |M|
| 2.0 |The algorithm must be as a Python class that can function as a standalone|M|

<p>
  </br>
  WeatherScraper 
  </br>
</p>

| ID | Descrizione | Priorità |
| --------------- | ----------- | ---------- | 
| 1.0 |The output of the systems shall be created in the project folder |M|
| 2.0 |The algorithm must be provided as a Python class that can function as a standalone |M|

<p>
  </br>
  ShapeFileProjection 
  </br>
</p>

| ID | Descrizione | Priorità |
| --------------- | ----------- | ---------- | 
| 1.0 |The output of the systems shall be created in the project folder |M|
| 2.0 |The algorithm must be provided as a package that can also function as a standalone |M|
