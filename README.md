# scraping-bot-manager
======
## Table of Contents
- [Description](#description)
    - [What this project solves](#)
    - [Why this project exists](#)
- [Key Features](#key-features)
- [Instalation & Usage](#installation)
- [Usage](#usage)
- [Credits](#credits)
- [Support](#support)
- [License](#license)

## Description
This bot is designed to act as a tool for managing and automating downloads through a self reliant database. It features both manual and automatic entry managment and a guided command line interface to add, manage, and delete entries as well as work with a global blacklist system to block tags on BOORU sites.

### What this project solves
This project is designed to be an  media scraper that can be used with a schedular or run manually to automate media scraping. As far as i know, there is no existing project that achives this specific goal at the time of release

### Why this project exists
This project was designed with the sole purpouse of being a dynamic self maintaining web scraper for media hoarding, preservation, and archiving.

### Key challenges or unique aspects of your implementation
- This program originated from a collection of scripts that I had previously written to achive the goals listed above, there was lots of challenges is designing a program that took several loose scripts into a uniform program that was dynamic enough to solve these issues. 
- There were also problems in being an Agile project, alot of constant rewriting and reformatting were neccesarry while under a limited time frame to complete the work

> [!NOTE]
> The technical arcitecture of this program uses the XP Agile framework due to the limited time availible on the time of its creation

## Features
- A fully self maintaining database for tracking entries
- Automatic entry into the database through batch proccessing
- Manual entry system for adding entries to the database 

## Limitations
- This project currently only supports pixiv and gelbooru, more engines will be added very soon
- This project does not support video scraping (YET)
- This project is not built with a security focus and as such, has no such features

## Installation
[Install the newest version of python3](https://www.python.org/downloads/)
The script automaticly downloads its [required dependencies](#credits)

## Internal Structure
### Program Structure
### U.I Structure

## Demo's & Examples
TODO

## Future Goals
- [ x ] Initial Release (2024/12/24)
- [ ] Implementation of more engines (Selectable Booru's, Deviantart, X, Blueskies, etc.)
- [ ] Implementation of video scraping
- [ ] Better database access - Better Read/Write implementation
- [ ] Refactor codebase for better efficency & Cleaner Code [Internal ]
- [ ] Setup debugging logger

## Usage
### Automatic Execution
python3 /path/to/bot/media-bot.py -e

## Credits
This program uses two external libraries to form the backend of the scraper, check below for sources
[gallery-dl](https://github.com/mikf/gallery-dl)
[yt-dlp](https://github.com/yt-dlp/yt-dlp)

## License
Licensed under the MIT License. See [LICENSE](LICENSE) for more details