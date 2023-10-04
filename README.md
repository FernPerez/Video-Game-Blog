# Video-Game-Blog/Journal App
## Introduction
This is a website I created using Python and Flask not only as a means to refresh and improve my web development skills, but also as a tool that I could personally use for my hobbies. I am a massive fan of video games, and I also love taking note of my "journey" playing games over the years. While I used to use tier list maker websites to rank my played games, this became kind of repetitive to do and didn't let me fully express my thoughts on a game or rank them in as much detail. So I thought, "Wait a minute. I'm a programmer. I went to school for doing things like this." So I decided to create this site as a sort of passion project and a way to test my skills. So far, I am quite satisfied with the way it has come out.

As of writing this, the application can now log in multiple users who can each add their own individual games independent of one another. Note that the ability to upload images is only available in the private unhosted version of the site. Due to most of the images being potentially copyrighted, I do not want to allow users to upload and risk infringing on someone's copyright. Instead, users can select one of multiple images that I created using Microsoft Paint.

The current main branch of the project is where the private unhosted version lives, while the public version is located in the public branch. I plan on moving the current main branch into a 'private' branch and then moving the public version over to main, since that's
arguably the more important one.

## Features
### Games Page
This is what I consider the main page of the site. It contains a grid of all the games the user has played with their own individual thumbnails. The page also lets you use multiple different sorting options such as title, score, and release date. You can also filter by franchise, series, genre, and platforms. You can also search manually using the searchbar. The thumbnails load in with an animation, and also expand when hovered over. The images on these thumbnails are dynamically taken from each game's own record in the database.

### Game Info
When a game in the grid is clicked, the user is brought to a page that contains details about the respective game. These details include the game's title, series, franchise, release date, systems, and genres. The page also contains the user's own personal feelings on the game in the form of a description and score. Also worth noting is the "Date Started" and "Date Finished" parameters, which are useful to keep track of when the user played these games. Sliding animations are given to the elements of the page. Finally, there is the update button which lets users change any information in the page.

### Adding and Updating Game Info
When the user wants to add a game to their list, they need to go to the Add Game page to insert the necessary information. This page lets them input all the details as well as selecting an image to represent the game. When the user wants to update a game's info, they can find the game and then select the Update button. The update page is very similar to the add page, but it will have the game's previous info already in the fields.

## Planned New Features
### Major
- Having series and franchise filters in games page populate given the user's current list of games. At the moment, it only uses some franchises and series I added, but if a user adds a game from a different one, they will not be able to filter by them.
- Creating a game backlog/future games page. This one is pretty big as it would require some big changes to the database, but it is something I plan on adding at some point.

## Minor
- Making the front end more nice to look at, particularly the background.
- Allowing users to delete games.
