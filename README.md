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
    - [OAuth](#oauth-configuration)
- [U.I Structure](#ui-structure)
- [File Structure](#file-structure)
- [Future Goals](#future-goals)
- [Credits](#credits)
- [Support](#support)
- [License](#license)
- [Changelog](#changelog)

## Description
This bot is designed as a comprehensive tool for managing and automating downloads using a self-reliant database. It offers both manual and automatic entry through a command line tool and a batch file. As well as a guided command line interface to add, manage, and delete entries as well as modify a global blacklist system to block tags on BOORU sites.

### Purpouse and Goals
The primary goal of this project is to streamline media scraping through automation and maintain an organized internal database. It can be scheduled or run manually, ensuring efficient and reliable media scraping. At the time of release, no other project achieves this functionality.

### Why this project exists
This project was conceived to be a dynamic, self-maintaining web scraper for media hoarding, preservation, and archiving. It also needed to be scaleable and easy to maintain for a variety of potential uses.

### Key challenges
- Integrating Loose Code: Combining disparate scripts from various languages into a cohesive, unified system posed significant challenges.
- Agile Development: Implementing an XP Agile framework necessitated frequent rewriting and reformatting to meet changing requirements within a tight deadline.
- Time-Constrained Design: The architecture was developed under a limited timeframe, balancing scalability and functionality.

## Features
- Self-Maintaining Database: Automatically tracks entries, the latest downloads, and the most recent available updates.
- Batch Processing: Enables automated database entry through a streamlined file processing system.
- Manual Entry System: Provides a flexible option for users to add specific entries directly to the database.
- Duplicate Protection: Built in anti duplication functionality
- Robust U.I to make working with this program as simple as possible

## Limitations
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
> Any BOORU sites used must be registered to the bot, see [](#) for more info 

### Manual Entries
1. Launch the bot in its root directory, python3 media-bot.py
2. Follow U.I Prompts

### Automatic Execution
Add the following to a schedular like cron:
```bash
cd /path/to/bot/ && python3 media-bot.py -e
```

### OAuth configuration
See the [gallery-dl](https://github.com/mikf/gallery-dl?tab=readme-ov-file#id25) section about configuring OAuth for Pixiv & Deviantart downloads

## U.I Structure Overview
```
[1] Configure BOORU engines
    [1] Add recognized BOORU's
    [2] Edit recongized BOORU's
    [3] Remove recongnized BOORU's
    [4] Print recongnized BOORU's
    [0] Previous menu
[2] Entry Managment
    [1] Add Entry
    [2] Modify Entry
    [3] Delete Entry
    [4] View Entries
    [5] Add Blacklist tags (BOORU Only)
    [6] Remove Blacklist tags (BOORU Only)
    [7] View Blacklist
    [0] Previous Menu
[3] View Scraper Metadata
    [1] Print Entries
    [2] Print Blacklist
    [3] Print BOORU config
    [0] Previous Menu
[4] Exectute Scraper
[0] Quit
```

## File Structure
- gallery-dl            Download directory for image scraper
- internal              Folder for internal databases, batch loading, etc
    - batch_load.txt    File for batch loading queries into the bot (run at startup)
    - blacklist.db      Blacklist entries that apply to all BOORU queries
    - config.db         Bots configuration database
    - downloaded.db     Log of all files that were downloaded
    - entry.db          Database of queries being tracked        
- LISCENSE   
- media-bot.py

## Future Goals
- [x] Initial Release (2024/12/24)
- [ ] Implementation of more engines (Selectable Booru's, Deviantart, X, Blueskies, Other) (Partial: 2024/12/30)
- [ ] Implementation of video scraping
- [ ] Implement GIF processing for pixiv downloads
- [ ] Localize to Japanese
- [x] Better database access - Better Read/Write implementation (2024/12/30)
- [x] Refactor codebase for better efficiency & Cleaner Code (2024/12/30)
- [ ] Setup debugging logger
- [ ] Enhance configuration system (Automatic compression, gif compression, etc.)

## Credits
This program uses two external libraries to form the backend of the scraper, check below for sources.
- [gallery-dl](https://github.com/mikf/gallery-dl)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)

## Support
If you like my work and want to support me, check out [my Ko-fi](https://ko-fi.com/waffles54)

## License
Licensed under the MIT License. See [LICENSE](LICENSE) for more details

## Changelog
###### 0.9.0: Public Release (Major Update)
- Basic UI Structure
- Create, Delete, and View Entries
- Create, Delete, and View blacklists
- Bot execution functionality
- Schedular / Automatic execution (-e)
- Duplicae entry managment
- batch file proccessing
- Cross compatible framework setup
- Self maintaining database functionality
###### 0.9.1 (Hotfix)
- Patched bot initializer
###### 1.0.0 (UI/UX Update, Hotfix)
- Enhanced UI quality (standerdized)
- Fixed database failure bugs
- Implemented a gitignore file
- Standardized input schematics
###### 1.0.1 (Documentation Update)
- Fixed the gitignore file
###### 1.0.2 (Small Patch)
- Fixed bugged manual entry generation tokenizer
- Implemented an ALL mode for searches
###### 1.0.3 (Small Patch)
- Implemented basic functionality for modifying the database
- Changed output format for blacklist information
- Cleaned up U.I (Spacing, readability, etc)
###### 1.0.4 - 1.0.7 (Documentation Update)
- Readme setup
- Minor code cleanup
###### 1.0.8 (Hotfix)
- Fixes a critical bug that causes the database to be deleted in the instance of an error
###### 1.0.9 (Small Patch)
- Added end data confirmation for BOORU engines
- Actually Fixed critical database failure bug
###### 1.1.0 (Major Patch, Branch Split)
- Dynamic engine updates
- Added end data confirmation for BOORU engines
- Restructured Codebase
- Cleaned up several functions
- Improved readability
- Improved error checking
- dissasembled static booru system, implemented engine registry system
- implemented basic configuration system
- Updated UI
- Added db_query tracking
- improved database reliability
- improved database r/w performance
- improved database stability
- improved various nomenclature issues
- Re-implemented all functions to support dynamic engines
- fixed several program flow fixes
- static engine configuration reimplemented (Non BOORU)
- seperated database managment functions added
- Implemented query generation for dynamic engines
- reconfigured execution function to execute dynamically
- Improved database reliability in the instance of a failure
- Made query generation dynamic
- Added a few entries to the .gitignore
- Implemented booru config removal system
- cleaned up booru config entry code
- Implemented metadata viewing mode
###### 1.2.0 (Major Patch, Branch Split)
- Implementation of automatic GIF compresser (PIXIV)
- Implementation of automatic JPG compression (Space efficency enchancment)
- Removal of Deviantart support
- Better code comments
- Significantly improved UI readability
- Fixed deletion system issues
- Setup OTHER engine
- Fixed overwriting class problem (Internal structure issue)
- Improved on input validation
- Improved global blacklist problems 
- Added detailed record keeping of bots progress (Initialization & Execution)
- Standardized program flow systems
- Standardized output directories (fixed multi folder creation issue every time the bot was run)