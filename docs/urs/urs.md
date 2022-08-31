

### User Requirements Specification Document
##### DIBRIS – Università di Genova. Scuola Politecnica, Software Engineering Course 80154


**VERSION : 1.0**

**Authors**  
Massimo Narizzano

All the students of the Software Engineering Course A.A. 2021/2022

**REVISION HISTORY**

| Version    | Date        | Authors      | Notes        |
| ----------- | ----------- | ----------- | ----------- |
| 1.0 | 21/3/2022 |M. Narizzano | First Draft |
| 1.1 | 28/3/2022 |M. Narizzano | Second Draft |
| 1.3 | 11/4/2022 |M. Narizzano | Final Draft |


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
The present document describe the functional and non-functional requirements of a system that wants to translate a file describing a Mealy Machine into a file SMV. 

<a name="sp1.1"></a>

### 1.1 Document Scope
This document introduces the Requirement Analysis in Software Engineering for the course of Software Engineering at Laurea Magistrale in Computer Engineering in Genova. 


<a name="sp1.2"></a>

### 1.2 Definitios and Acronym


| Acronym				| Definition | 
| ------------------------------------- | ----------- | 
| NBA                                   | Non deterministic Buchi Automata |
| LTL                                   | Linear Temporal Logic |
| MM                                    | Mealy Machine |
| SMV                                   | Symbolic Model Verifier |
| NuSMV                                 | New Symbolic Model Verifier |


<a name="sp1.3"></a>

### 1.3 References 

<a name="p2"></a>

## 2. System Description
<a name="sp2.15"></a>

### 2.1 Context and Motivation
<a name="sp2.2"></a>
In computer science (in particular in Artificial Intelligence), model checking is a method for checking whether a finite-state model of a system meets a given specification. In model checking given a system model and a formal property the model chercker checks if the model satisfy the property. NuSMV is one of the most used model checker and it takes in input a finite state machine in a language called SMV and a formal property written in Linear Temporal Logic (LTL), or Computational Tree Logic. The model written in SMV usually define a Kripke Structure a type of Finite State Machine. However one of the most used languages for defining Reactive Systems are the Mealy Machines. So in order to use NuSMV to model check a mealy machine against some LTL property we need to translate the mealy machine into a a SMV file.

### 2.2 Project Obectives 
<a name="p3"></a>
Goal of the project is to develop a translator from a mealy machine to a kripke structure in SMV format. 

## 3. Requirements

| Priorità | Significato | 
| --------------- | ----------- | 
| M | **Mandatory:**   |
| D | **Desiderable:** |
| O | **Optional:**    |
| E | **future Enhancement:** |

<a name="sp3.1"></a>
### 3.1 Stakeholders

<a name="sp3.2"></a>
### 3.2 Functional Requirements 

| ID | Descrizione | Priorità |
| --------------- | ----------- | ---------- | 
| 1.0 | The system shall take in input a Mealy Machine definition in graphviz format|M|
| 1.1 | The system shall take in input a Mealy Machine definition in custom format|D|
| 2.0 | The system shall take in input a Mealy Machine definition in HOA format|D|
| 3.0 | The Mealy Machine shall takes as input a set of input-symbols/alphabet|M|
| 4.0 | The Mealy Machine shall takes as input a set of output-symbols/alphabet|M|
| 5.0 | The system shall output a SMV file |M|
| 6.0 | The system shall translate an input  Mealy Machine into a SMV file |M|
| 7.0 | The system shall provide a GUI for drawing MM picture |E|
| 8.0 | The system shall provide a GUI for modifying the SMV file |E|


<a name="sp3.3"></a>
### 3.2 Non-Functional Requirements 
 
| ID | Descrizione | Priorità |
| --------------- | ----------- | ---------- | 
| 1.0 |The output of the systems shall be parsed correctly by NuSMV |M|
| 1.0 |The system must be provided as  desktop application |M|
| 1.0 |The system must be provided as web based application |E|
| 1.0 |The system must run on Linux based  OS |M|
| 1.0 |The system must run on Windows based OS |E|
| 1.0 |The system must run on MACOS based OS |E|

