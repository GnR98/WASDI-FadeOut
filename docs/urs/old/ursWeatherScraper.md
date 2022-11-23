### User Requirements Specification Document
##### DIBRIS – Università di Genova. Scuola Politecnica, Software Engineering Course 80154


**VERSION : 1.0**

**Authors**  
Roberto Gnisci<br/>
Matteo Aicardi


**REVISION HISTORY**

| Version    | Date        | Authors      | Notes        |
| ----------- | ----------- | ----------- | ----------- |
| 1.0 | 17/8/2022 |M. Aicardi, R. Gnisci | First Draft |
| 1.1 | 25/8/2022 |M. Aicardi, R. Gnisci | Second Draft |
| 1.2 | 31/8/2022 |M. Aicardi, R. Gnisci | Third Draft |
| 1.3 | 10/9/2022 |M. Aicardi, R. Gnisci | Fourth Draft |
| 1.4 | 20/9/2022 |M. Aicardi, R. Gnisci | Fifth Draft |
| 1.5 | 10/10/2022 |M. Aicardi, R. Gnisci | Final Draft |

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
The present document describe the functional and non-functional requirements of a script that reads from an Excel leaks database where
and when a leak occured, then fetches precipitation data of a given period of time for that place. The script also approximately recognizes if a
pair of coordinates reside in a city, a town or a village


<a name="sp1.1"></a>

### 1.1 Document Scope
This document introduces the Requirement Analysis in Software Engineering for the course of Software Engineering at Laurea Magistrale in Computer Engineering in Genova. 


<a name="sp1.2"></a>

### 1.2 Definitios and Acronym


| Name				| Definition | 
| ------------------------------------- | ----------- | 
| METEOSTAT API                                  | Interface used to check and eventually fetch the coordinates|
| WASDI                                   | Web Advanced Space Developer Interface |

<a name="sp1.3"></a>

### 1.3 References 

https://dev.meteostat.net/python/#installation (METEOSTAT library webpage)
<a name="p2"></a>

## 2. System Description
<a name="sp2.15"></a>

### 2.1 Context and Motivation
<a name="sp2.2"></a>
WASDI operates in various fields including the development of an algorithm capable of recognizing if a water leak has happened near a pipe.
To achieve that they need to train an AI with a correct dataset, part of this dataset is inside a database with coordinates of places where a leak
has already occured and repaired. When analyzing an image it is needed to know if the water that is visible is caused by the leak or by other
causes, collecting precipitation data helps to filter the images where rain might have been the origin of the visible water.
The assignment of city, town or village to a pair of coordinates is useful to recognize if agricultural activities may be nearby.

### 2.2 Project Obectives 
<a name="p3"></a>
This algorithm aims to create an excel file with precipitation data for each repair intervention.

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
| 2.0 | The algorithm shall take in input the number of days prior the repair date on which to search for data |M|
| 2.1 | The algorithm shall take in input the number of days following the repair date on which to search for data |M|
| 3.0 | The algorithm shall take in input the name of the district in order to search data only for the repairs done in the given district |M|
| 4.0 | The algorithm may take in a json file containing all the inputs previously specified |D|
| 5.0 | The algorithm shall output a new Excel file |M|
| 5.1 | The new Excel file shall have two columns to collect precipitation data, one for the period of time before the repair date and one for the following period of time |M|
| 5.2 | The new Excel file shall have two columns (one for each semi-period of time) containig the mean value of the collected data|M|
| 5.3 | The new Excel file shall have two columns (one for each semi-period of time) containig a true/false/nan value that represents if it has rained in that period of time|O|
| 5.4 | The new Excel file shall have a column containing if the row's coordinates belong to a city,town or village|D|

<a name="sp3.3"></a>
### 3.2 Non-Functional Requirements 
 
| ID | Descrizione | Priorità |
| --------------- | ----------- | ---------- | 
| 1.0 |The output of the systems shall be created in the project folder |M|
| 2.0 |The algorithm must be provided as a package that can also function as a standalone |M|
