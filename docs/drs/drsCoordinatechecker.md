# Title of the project

## Design Requirement Specification Document

DIBRIS – Università di Genova. Scuola Politecnica, Corso di Ingegneria del Software 80154

**Authors**  
Roberto Gnisci<br/>
Matteo Aicardi

### REVISION HISTORY

| Version    | Date        | Authors      | Notes        |
| ----------- | ----------- | ----------- | ----------- |
| 1.0 | 18/9/2022 |M. Aicardi, R. Gnisci | First Draft |
| 1.1 | 28/9/2022 |M. Aicardi, R. Gnisci | Second Draft |
| 1.2 | 7/10/2022 |M. Aicardi, R. Gnisci | Third Draft |
| 1.3 | 10/10/2022 |M. Aicardi, R. Gnisci | Final Draft |


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
    <summary> The goal of this script is to correct all the pairs of coordinaates that were geocoded incorrectly during the first writing of the water leaks database  </summary>
    <p>In particular each row contains a point that is geolocated with a longitude and a latitude (inverted in the Excel file for some reason), by having these correct it is possible to properly collect data and create a suitable dataset for a future machine learning algorithm</p>
</details>

### <a name="def"></a> 1.2 Definitions
    
| Name				| Definition | 
| ------------------------------------- | ----------- | 
| WASDI                                 | Web Advanced Space Developer Interface |
    
</details>


### <a name="biblio"></a> 1.3 Bibliography
<details> 
    <summary> Libraries Used
    </summary>
    <p>
       https://pandas.pydata.org/ (Pandas to read and write Excel files)
    </p>
    <p>
       https://github.com/geopy/geopy (Geopy for geocoding purposes)
    </p>
</details>

## <a name="description"></a> 2 Project Description

### <a name="project-intro"></a> 2.1 Project Introduction 

   <p> In order to create a new Excel file with correct data the scripts takes as input the database and, for each row, reads the latitude and the longitude of the current point
              and saves the name of the district from the designated columns, then using the geopy library applies reverse geocoding 
              to the coordinates, if the district obtained from this operation is different than the one given in the database a correction process begins.
              The correction process consists of reading the full address of the point from the database and, using again the geopy library, do a geocode operation
              to find a new set of coordinates, this pair is then written in the right columns in the new Excel file.
   </p>


### <a name="tech"></a> 2.2 Technologies used

<details> 
    <summary> Description of the overall architecture. </summary>
    <p>Graphical representation of the system architecture.  May be composed by multiple diagrams depending on the differences in the environment
specifications    </p>
</details>

### <a name="constraints"></a> 2.3 Assumption and Constraint 
<details> 
    <summary> There are both assumptions and constraints
    </summary>
  
    <p>- Since this is a custom script it only works for an Excel file with specific column in specific positions</p>
    <p>- The only datas that may be incorrect are the ones regarding the latitude/longitude and the date on which the repairings finished </p>
    <p>- The user must be able to connect to Internet </p>
  
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
