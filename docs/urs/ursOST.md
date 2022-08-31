

### User Requirements Specification Document
##### DIBRIS – Università di Genova. Scuola Politecnica, Software Engineering Course 80154


**VERSION : 1.0**

**Authors**  
Roberto Gnisci<br/>
Matteo Aicardi


**REVISION HISTORY**

| Version    | Date        | Authors      | Notes        |
| ----------- | ----------- | ----------- | ----------- |
| 1.0 | 30/6/2022 |M. Aicardi, R. Gnisci | First Draft |
| 1.1 | 4/7/2022 |M. Aicardi, R. Gnisci | Second Draft |
| 1.2 | 17/8/2022 |M. Aicardi, R. Gnisci | Third Draft |
| 1.3 | 17/8/2022 |M. Aicardi, R. Gnisci | Final Draft |


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
The present document describe the functional and non-functional requirements of an algorithm that wants to process a GRD scene into an ARD product on the WASDI website. 

<a name="sp1.1"></a>

### 1.1 Document Scope
This document introduces the Requirement Analysis in Software Engineering for the course of Software Engineering at Laurea Magistrale in Computer Engineering in Genova. 


<a name="sp1.2"></a>

### 1.2 Definitios and Acronym


| Acronym				| Definition | 
| ------------------------------------- | ----------- | 
| GRD                                   | Ground Range Detected |
| ARD                                   | Analysis Ready Data |
| OST                                    | Open Sar Toolkit |
| WASDI                                   | Web Advanced Space Developer Interface |


<a name="sp1.3"></a>

### 1.3 References 

https://wasdi.readthedocs.io/en/latest/index.html (WASDI documentation)
<a name="p2"></a>

## 2. System Description
<a name="sp2.15"></a>

### 2.1 Context and Motivation
<a name="sp2.2"></a>
WASDI's online website provides access to satellite data, from the Copernicus Sentinels to commercial data providers, display them, run algorithms, visualise and evaluate the results, and share projects among different users.
In the analysis of the satellite images there is not yet a universally recognized standard for satellite images representation, the ARD format (proposed by OST) seems to be the first step towards a real standard.
The ARD data are Earth Observation data pre-processed for users and ‘ready to analyse’ and have a wide area of application, from the soil moisture monitoring to the detection of atmosphere composition.

### 2.2 Project Obectives 
<a name="p3"></a>
This algorithm aims to import the processing of a GRD image into an ARD product on the WASDI website.

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
| 1.0 | The algorithm shall take in input the last date on which to search the image |M|
| 1.1 | The algorithm shall take the number of days in the past on which you want to search compared to the last date|M|
| 2.0 | The algorithm shall take in input a bounding box defined by the user|M|
| 3.0 | The algorithm shall take in input one of the proposed satellite image provider|O|
| 4.0 | The algorithm shall takes in input the product image type|E|
| 5.0 | The algorithm shall takes in input a boolean value to decide to apply the terrain correction |D|
| 6.0 | The algorithm shall provide a GUI on WASDI to insert and select the input values |M|
| 7.0 | The algorithm shall output a mosaic made by ARD images |M|


<a name="sp3.3"></a>
### 3.2 Non-Functional Requirements 
 
| ID | Descrizione | Priorità |
| --------------- | ----------- | ---------- | 
| 1.0 |The output of the systems shall be correctly visualized on WASDI |M|
| 2.0 |The algorithm must be provided as a WASDI processor |M|

