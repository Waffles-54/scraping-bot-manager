# scraping-bot-manager
## Table of Contents
- [Description](#description)
    - [Purpouse and Goals](#purpouse-and-goals)
    - [Why this project exists](#why-this-project-exists)
    - [Key challenges](#key-challenges)
- [Features](#features)
- [Limitations](#limitations)
- [Usage](#usage)
    - [First time setup](#first-time-setup)
    - [Batch Processing](#batch-proccessing)
    - [Manual Entries](#manual-entries)
    - [Automatic Execution](#automatic-execution)
- [U.I Structure](#ui-structure)
- [File Structure](#file-structure)
- [Future Goals](#future-goals)
- [Credits](#credits)
- [Support](#support)
- [License](#license)

## Description
This bot is designed as a comprehensive tool for managing and automating downloads using a self-reliant database. It offers both manual and automatic entry through a command line tool and a batch file. As well as a guided command line interface to add, manage, and delete entries as well as modify a global blacklist system to block tags on BOORU sites.

### Purpouse and Goals
The primary goal of this project is to streamline media scraping through automation and maintain an organized internal database. It can be scheduled or run manually, ensuring efficient and reliable media scraping. At the time of release, no other project achieves this functionality.

### Why this project exists
This project was conceived to be a dynamic, self-maintaining web scraper for media hoarding, preservation, and archiving. It also needed to be scaleable and easy to maintain for a variety of potential uses.

### Key challenges
- Integrating Loose Code: Combining disparate scripts from various languages into a cohesive, unified system posed significant challenges.
- Agile Development: Implementing an XP Agile framework necessitated frequent rewriting and reformatting to meet changing requirements within tight deadlines.
- Time-Constrained Design: The architecture was developed under a limited timeframe, balancing scalability and functionality.

## Features
- Self-Maintaining Database: Automatically tracks entries, the latest downloads, and the most recent available updates.
- Batch Processing: Enables automated database entry through a streamlined file processing system.
- Manual Entry System: Provides a flexible option for users to add specific entries directly to the database.
- Duplicate Protection: Built in anti duplication functionality

## Limitations
- This project currently only supports Pixiv and Gelbooru, more engines will be added very soon
- This project does not support video scraping [(yet)](#future-goals)
- This project is not built with a security focus and as such, has no such features
> [!CAUTION]
> Modifying the database directly may cause the bot to fail and the database to be scrubbed, DO NOT DIRECTLY ALTER THE DATABASE

## Usage
### First time setup
1. [Install the newest version of python](https://www.python.org/downloads/)
2. Download the project
3. Move the project to a desired location
4. run the python file from a command line in the root folder you have selected, the bot will initialize and setup its file structure
5. follow the onscreen prompts to add an entry to the database, You are now ready to go ✨
### Batch Proccessing
Once the bot has been initalized once, add any links you want to track to the batch_file.txt file under the internal folder
> [!NOTE]
> Currently only suppors Gelbooru & Pixiv, this will be updated soon, see [Future Goals](#future-goals) for more info 

### Manual Entries
1. Launch the bot in its root directory, python3 media-bot.py
2. Follow U.I Prompts

### Automatic Execution
Add the following to a schedular like cron:

python3 /path/to/bot/media-bot.py -e

## U.I Structure
- [1] Database Managment
    - [1] View Entries
        - [BRU] Booru Entries
        - [PXV] Pixiv Entries
        - [OTH] Other Entries
        - [ALL] All Entries
        - [0] Previous Menu
    - [2] Add Entry
        - [1] Gelbooru
        - [2] Pixiv
        - [3] Manual mode (direct query entry)
        - [0] Exit Entry mode
    - [3] Modify Entry
        - [BRU] Booru Engine
        - [0] Previous Menu
    - [4] Delete Entry
        - [BRU] Booru Engine
        - [PXV] Pixiv Engine
        - [OTH] Other Engine
        - [0] Previous Menu
    - [5] View Blacklist
    - [6] Add Blacklist tags (BOORU Only)
    - [7] Remove Blacklist tags (BOORU Only)
    - [0] Previous Menu
- [2] View Bot Info
    - [1] View Entries
    - [2] View Blacklist
    - [0] Previous Menu
- [3] Exectute Bot
- [0] Quit

## File Structure
- gallery-dl            Download directory for image scraper
- internal              Folder for internal databases, batch loading, etc
    - batch_load.txt
    - blacklist.db
    - downloaded.db
    - query.db
- LISCENSE   
- media-bot.py 

## Future Goals
- [x] Initial Release (2024/12/24)
- [] Implementation of more engines (Selectable Booru's, Deviantart, X, Blueskies, etc.)
- [] Implementation of video scraping
- [] Better database access - Better Read/Write implementation
- [] Refactor codebase for better efficiency & Cleaner Code
- [] Setup debugging logger

## Credits
This program uses two external libraries to form the backend of the scraper, check below for sources.
- [gallery-dl](https://github.com/mikf/gallery-dl)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)

## Support
If you like my work and want to support me, check out [my Ko-fi](https://ko-fi.com/waffles54)

## License
Licensed under the MIT License. See [LICENSE](LICENSE) for more details
