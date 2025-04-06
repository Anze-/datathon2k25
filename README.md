# Datathon 2k25 - PUFFERFISH team
This repo contains the works accomplished by our team during the 4th-6th April 2025 Zurich Datathon hackathon.
Team members: Michele Dalle Rive, Fabrizio DeCastelli, Mark Sobolev, Alberto Anzellotti

NDA NOTICE: some or all of the content, code and data in this repo might be covered by an NDA, please know that if you are granted to see this code you are bound not to disclose its content.

# Challenge
Our challenge was kindly proposed by Orderfox, and consists in building a RAG agent that can answer questions about supply chain.

We briefly describe our solution (further explained in the report) and give instruction on how to build and run the application.

## Available data
We were kindly provided with ~13,000 scraped websites, each consisting of 50-70 webpages. The dataset is provided in `json` format and, because of its size, we do not include it in the repository.

## 4 solution steps

1. Data preprocessing and feature engineering
2. Data embedding and storage
3. RAG
4. Agent and UI

## Proposed Proof of Concept
Our proof of concept takes care of selecting the most important data, embedding it and storing it in a Vector Database. The RAG agent is then able to answer user's questions, integrating the existing data with the LLM knowledge.

# Code

## Code architecture
The repository is organized in the following structure:
```
- data/: contains some resources used for processing and analyzing data
- frontend/: web interface to interact with the chatbot.
- indexing/: contains code used for indexing of the dataset and storing.
- notebooks/: notebooks used together with data/ for analysis and processing
- notes/: some generic notes used during the hackathon
- rag/: code for the RAG agent and the webserver used to deploy it
```
Some important files in the repository are:
- requirements.txt: list of required packages. The hackathon environment is very frenetic, so some packages could be missing. We apologise for any inconvenience.
- Dockerfile: a Dockerfile that can be used to start the backend (only!) in a Docker container.
- main.py: the main file to run the backend API. Further instructions are given in the next section.

## Install
In order to install all the required pre-requisites for the backend, you can use the `requirements.txt` file, or you can use the Dockerfile to build a Docker image that contains all the required packages.
The packages for the frontend can be installed from the `frontend/` directory using `npm install`.

## How to run
We suggest running the backend using the provided Docker container, or -- after installing all the required packages -- by running:
```
uvicorn main:app --host 0.0.0.0. --port 8000
```

## Datasets
Some of the datasets we used to preprocess data are not available in the repository for space reasons. They can however be downloaded from the following links:
- [geonames-all-cities-with-a-population-1000.csv](https://public.opendatasoft.com/explore/dataset/geonames-all-cities-with-a-population-1000/api/?disjunctive.cou_name_en&sort=name&location=2,0.90932,-0.05452&basemap=jawg.light)
- [us-cities-demographics.csv](https://public.opendatasoft.com/explore/dataset/us-cities-demographics/export/)
