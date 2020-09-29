# Morocco Covid-19 data analysis & Prediction, news headlines scrapping and sentimental analysis using machine learning models in a multi agents system architecture.

### Objective:
The main objective of the project is the implementation of an intelligent multi-agent system based on several supervised and unsupervised learning algorithms. The system will be composed of several intelligent and interactive agents, from which each agent performs a specific task. In addition to a Single page Application (Angular based) that will interact with the system.

***The project is built using the following Frameworks
+ MongoDB - The used to store data
+ Django- The web framework used to build the smart layer API
+ Spring Boot - The web framework used to build the MAS layer API
+ JADE Framework - The framework used to implement agents in the MAS layer
+ Angular - The framework used to build the front-end layer

Smart layer:
This is a Django based REST api containing all the scripts needed to scraping, pre-processing and loading data into a Mongodb database in addition to all the models we have developed for predictions, sentimental analysis and visualizations.

Multi Agent System (MAS) layer:
This is a REST api based on SpringBoot containing JADE Framework with all agents, and their behaviours and how they communicate with each other and how they serve the SPA frontend layer.

Single Page Application (SPA) layer:
This is the front-end part which contains pages for each agent ( predictions, sentimental analysis and data visualisation), each page communicates with it's own appropriate agent using a restful architecture.



## SMA Spring boot LAYER :
https://github.com/MedAmrani/Agents_Layer


## Visualisation Angular LAYER : 
https://github.com/MedAmrani/Covid_19_Dashboard
