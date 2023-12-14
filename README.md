# Strava Improvement Reccomendation System

## Overview
Strava is a popular app used by athletes to track workouts. In our project we give users insight to their current performance and use activity data of users that are outperform the user to give reccomendations on how to improve. The segments feature of strava takes stretches from user activity to compare to other users who also complete that strech in one of their logged activities. Any segment in which a user performs amongst the top ten best is stored in the profile under top tens.

This project uses a webscraping approach which required the use of scrapy and selenium. While strava does have an API available to the public, it is severly limited and requires authentification by the user before taking any activity data. Given that our project relies so heavily on a analyzing competitor activities, the API was not of much use to us. This project looks at anyone who outperformed the user in their top tens and use their activity data to help the user improve. With out sraper we first logged into strava, directed to the top tens page, visited all of the top ten segments, got all of the athletes who beat the user in each top ten, then directed to their athelte page to collect all of their activity for the month leading up to their achievement.


## Behind the Design: Scraper construction
The scraper takes in the athlete ID and after logging into a strava account to allow for successful scraping, directs to the users top ten pages. At the top ten page the scraper collects all of the segment links for the tep tens achieved and yields them in the next function. With all of the segment links, all of the athletes with public profiles who performed better than the user are selected along with the date of the acheivement. With this information the better-performing athlete profile is returned with activities from the month before the corresponding top ten segment achievement. On the athelte page selenium is used to scrape the activity data from each athlete page. This is data is then cleaned and condesnsed to provide training reccomendations for users.


