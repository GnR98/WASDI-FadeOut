### User Requirements Specification Document
##### DIBRIS – Università di Genova. Scuola Politecnica, Software Engineering Course 80154


**VERSION : 1.0**

**Authors**  
Roberto Gnisci<br/>
Matteo Aicardi


**REVISION HISTORY**

| Version    | Date        | Authors      | Notes        |
| ----------- | ----------- | ----------- | ----------- |
| 1.0 | 10/10/2022 |M. Aicardi, R. Gnisci | First Draft |
| 1.1 | 12/10/2022 |M. Aicardi, R. Gnisci | Second Draft |
| 1.2 | 14/10/2022 |M. Aicardi, R. Gnisci | Third Draft |
| 1.3 | 18/10/2022 |M. Aicardi, R. Gnisci | Fourth Draft |
| 1.4 | 20/10/2022 |M. Aicardi, R. Gnisci | Fifth Draft |
| 1.5 | 25/10/2022 |M. Aicardi, R. Gnisci | Final Draft |

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
The present document describe the functional and non-functional requirements of a python class that reads from the leaks Excel database where an intervention occured and then projects
the obtained coordinates on the pipe network. The algorithm inside the class needs a specific coordinate reference system and is able to change the one used in the pipe network file to meet this constraint.


<a name="sp1.1"></a>

### 1.1 Document Scope
This document introduces the Requirement Analysis in Software Engineering for the course of Software Engineering at Laurea Magistrale in Computer Engineering in Genova. 


<a name="sp1.2"></a>

### 1.2 Definitios and Acronym


| Name				| Definition | 
| ------------------------------------- | ----------- | 
| NOMINATIM API                           | Interface used to check and eventually fetch the coordinates|
| EPSG 32632                              | Coordinate reference system used in the original pipe network file |
| WGS84                                   | Coordinate reference system needed to use the projection algorithm|
| WASDI                                   | Web Advanced Space Developer Interface |

<a name="sp1.3"></a>

### 1.3 References 

https://geopy.readthedocs.io/en/stable/ (Geopy NOMINATIM API)
https://pyproj4.github.io/pyproj/stable/ (pyproj)
https://shapely.readthedocs.io/en/maint-1.8/ (shapely)
<a name="p2"></a>

## 2. System Description
<a name="sp2.15"></a>

### 2.1 Context and Motivation
<a name="sp2.2"></a>
WASDI operates in various fields including the development of an algorithm capable of recognizing if a water leak has happened near a pipe.
To achieve that they need to train an AI with a correct dataset, part of this dataset is inside a database with coordinates of places where a leak
has already occured and repaired. The coordinates, however, may not exactly correspond to a pipe in the pipe network leaving a doubt about which one had the leak.


### 2.2 Project Obectives 
<a name="p3"></a>
This algorithm aims to create an excel file containing also a set of projected coordinates for each selected intervention.

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

| ID | Descrizione | Priorità |
| --------------- | ----------- | ---------- | 
| 1.0 | The algorithm shall take in input the location of the Excel file |M|
| 2.0 | The algorithm shall take in input the location of the shapefile containing the locations of all the pipes |M|
| 3.0 | The algorithm shall take in input the name of the district in order to search data only for the repairs done in the given district |M|
| 4.0 | The algorithm shall consider only the interventions done on the pipe network.may take in a json file containing all the inputs previously specified |M|
| 5.0 | The algorithm may take in a json file containing all the inputs previously specified |D|
| 6.0 | The algorithm shall be able to change the coordinate reference system of a shapefile from EPSG 32632 to WGS84|M|
| 7.0 | The algorithm shall output a new Excel file |M|
| 7.1 | The new Excel file shall have two new columns containing the set pf projected coordinates |M|

<a name="sp3.3"></a>
### 3.2 Non-Functional Requirements 
 
| ID | Descrizione | Priorità |
| --------------- | ----------- | ---------- | 
| 1.0 |The output of the systems shall be created in the project folder |M|
| 2.0 |The algorithm must be provided as a package that can also function as a standalone |M|
