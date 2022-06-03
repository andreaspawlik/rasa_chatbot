# rasa_chatbot

## Introduction

This repo is a result of the Zeiss ZDP hackathon challenge in 06/2022. 

## Goal

Build a chatbot to implement a self-service channel to customers. 

- Provide Q&A in a customer self-service scenario
- Use RASA technology for building contextual text-based assistants
- Bot should respond to questions of device-specific information
- Bot should use data from tabular database

## To-do

Due to time constraint, following nice-to-have features haven't been implemented yet:

- Run bot on a server
- Use endpoint to connect bot with MS teams
- Implementation of different languages (DE, CN etc)
- More semantic logics, e.g. “give top-tier smartphone” -> return the most phones
- Contextual understanding

## Getting Started

### Requirement

- python 3.7 or 3.8
- pandas
- rasa 3.1 ([Here for step-by-step installation](https://rasa.com/docs/rasa/installation/))
- fuzzywuzzy: `pip install fuzzywuzzy`

### Starting the bot

Code has been only setup locally.

1. Start the action server:
  1. Navigate to your rasa directory. 
  2. `rasa run actions` . This starts the server for the custom action. Keep this tab open and running when testing the bot. 
  3. Open a second terminal and start the bot by `rasa shell`. 
  4. You can now chat with the bot. :) 
