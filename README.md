# Strava Improvement Reccomendation System

## Overview
This project uses webscraping to provide improvement reccomendations for Strava users. The workout tracking app has competitive elements which track performance on various "segments." Segments are small parts of user activities which are recorded and compared to other users that also completed that segment in one of thier activities. If a user has on of the ten best positions for a segment it is shown on their profile on their top tens.

The idea behind this project is to look at a user's top ten achievements, find whoever outperformed them, and use their training regimen to find ways for the user to improve their position in their top tens and overall.

## Methodology
The project is constructed using webscraping. Our original plan was to use the Strava API however its scope was too limited for our needs. The Strava API requires authentification before accessing any user's data. While we could authenticate the user themself, the basis of the project relies on using competitor data to provide reccomendations which is not possible with the API. 

## Behind the Design: Scraper construction
The scraper takes in the athlete ID and after logging into a strava account to allow for successful scraping, directs to the users top ten pages. At the top ten page the scraper collects all of the segment links for the tep tens achieved and yields them in the next function. With all of the segment links, all of the athletes with public profiles who performed better than the user are selected along with the date of the acheivement. With this information the better-performing athlete profile is returned with activities from the month before the corresponding top ten segment achievement. On the athelte page ... TO BE DONE

## Behind the Design: Web design
We used flask to create the front-end design for the project. At its core the site take the users strava athlete ID and pushes it to out scraper where the appropriate data is extracted. Once the data is extracted it is formated apprpriately to make the reccomendation to the user, then returned on a results page.

## Reflection
TO DO

**Things to address:**
Still doing only uphill segments?
Return for case where user has not top tens.