# Alexa IMDb Movie Data Skill
## Overview
This Alexa Skill retrieves movie data from IMDb using web scraping. Users can ask Alexa for details about a movie, such as its rating, release date, and synopsis.

## Features
- Fetch movie details from IMDb.
- Provide basic movie information (rating, number of votes, synopsis, director, and duration).
- Process natural language queries via Alexa.

## Deployment
The project was deployed in the Amazon Developer Console. The *peliculas_alexadev.py* Python script was used to test and improve the skill. The *peliculas_cl.py* can be used via the command line to retrieve movie information.

## Requirements
- AWS Lambda (for backend processing)
- Alexa Skills Kit (ASK) SDK
- Python 3.8+
- BeautifulSoup (for web scraping)
- Requests (for HTTP requests)

## Collaborators
Natalia Klinik
Inés Mota
Ren Larrumbide Lin

---
**Note:** This project serves for educational purposes only. As IMDb’s terms of service do not allow automated scraping, it's recommended to use IMDb API to develop the skill.
