### User Requirements Specification Document
##### DIBRIS – Università di Genova. Scuola Politecnica, Software Engineering Course 80154


**VERSION : 1.0**

**Authors**  
Roberto Gnisci<br/>
Matteo Aicardi


**REVISION HISTORY**

| Version    | Date        | Authors      | Notes        |
| ----------- | ----------- | ----------- | ----------- |
| 1.0 | 18/9/2022 |M. Aicardi, R. Gnisci | First Draft |
| 1.1 | 28/9/2022 |M. Aicardi, R. Gnisci | Second Draft |
| 1.2 | 7/10/2022 |M. Aicardi, R. Gnisci | Third Draft |
| 1.2 | 10/10/2022 |M. Aicardi, R. Gnisci | Final Draft |

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
The present document describe the functional and non-functional requirements of a script that checks in the leaks database excel file if 
the pairs of coordinates are correct. If a pair is outstandingly wrong than an approximation is computed and substituted


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
has already occured and repaired. If the coordinates are not correct then it is impossible to retrieve weather data which means that, when analyzing images with water,
the origin of said water cannot be assured (eg it could have rained that day).

### 2.2 Project Obectives 
<a name="p3"></a>
This algorithm aims to create an excel file with correct coordinates for every repair intervention.

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
| 1.0 | The algorithm shall take in input the location of the excel file |M|
| 2.0 | The algorithm shall output a new Excel file named "NewGeolocation" |M|
| 2.1 | The "NewGeolocation" file shall not change the name of the coordinates columns |M|
| 2.2 | The "NewGeolocation" file shall not have null values inside the coordinate columns |M|



<a name="sp3.3"></a>
### 3.2 Non-Functional Requirements 
 
| ID | Descrizione | Priorità |
| --------------- | ----------- | ---------- | 
| 1.0 |The output of the systems shall be created in the project folder |M|
| 2.0 |The algorithm must be as a Python class |M|
