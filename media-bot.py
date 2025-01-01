#####################################################################
# OP-3e: Media Scraping Bot Project                                 #
# Written by Alice C. G.                                            #
# Follow local laws and websites guidelines when using this scraper #
#####################################################################

####################################################################################################
# Setup Phase: Import Libraries and setup global standards                                         # 
####################################################################################################
import os
import subprocess
import sys

VERSION = "1.1.0"                                               # Scripts version
BASE_PATH = "internal"                                          # Root directory for databases
ENTRIES = os.path.join(BASE_PATH, "entry.db")                   # Database for managing internal entry managment
BLACKLIST = os.path.join(BASE_PATH, "blacklist.db")             # Database for universal blacklist applications (Booru's only)
CONFIG = os.path.join(BASE_PATH, "config.db")                   # Scraper configuration file
BATCHFILE = os.path.join(BASE_PATH, "batch_load.txt")           # File for batch loading in links to be automaticly executed on the bots next run 
DOWNLOAD_ARCHIVES = os.path.join(BASE_PATH, "downloaded.db")    # Database achrive of downloaded files to avoid redownloading
LOG_ARCHIVE = os.path.join(BASE_PATH, "logs.txt")               # Internal log file to track errors and failures
GLOBAL_BLACKLIST = []                                           # Internal structure for managing the globally applied blacklist (Booru's only)
BOORU_DICT = {}                                                 # Mapper for custom Booru engines
ENTRY_DICT = {}                                                 # Mapper for Engines to maintain a list of modules

####################################################################################################
# Entry class: represents an internal module to track a queries metadata                           #
####################################################################################################
class Entry:
        # Entry initalizer, sets up metadata for a query from either the database or user input @ runtime
        def __init__(self, engine, query, lid, lob, rating, mode, db_query):
            self.engine = engine                    # Engine used to execute the query
            self.query = query                      # the query to be executed (TAG)
            self.lid = lid                          # last id of image downloaded, used in automating fresh downloads (Booru's)
            self.lob = lob                          # Local blacklisted tags
            self.rating = rating                    # Query image safety rating classification
            self.mode = mode                        # What type of query is being executed (Tag, User, etc.)
            self.db_query = db_query                # Database representation of the query
            self.generated_query = ""               # Query for execution (built from the rest of the modules metadata)
            ENTRY_DICT[engine].append(self)         # Append this module to the mapper

        def add_entry():
            isMoreModules, isVaildInput = True, False
            response, engine, query, lob, rating, lid, mode, db_query = [None] * 8
            while (isMoreModules): # While the user wants to add more entries
                while (isVaildInput == False):
                    print("\nEnter engine # to use, or press 0 to return to previous menu")
                    print("[1] Booru site")
                    print("[2] Pixiv")
                    # print("[3] Deviantart")
                    print("[4] Manual mode (direct query entry)")
                    print("[0] Exit Entry mode")
                    response = input("#: ")
                    sys.stdout.flush()
                    if response == "0":
                        return
                    elif response == "1": # BOORU Mode
                        if len(BOORU_DICT) != 0:
                            isValidEngine = False
                            while (isValidEngine == False):
                                isValidEngine = True
                                print("\nSelect BOORU engine, or enter 0 to return to previous menu:")
                                Scraper.print_booru_engines()
                                engine = input("# ")
                                if engine == "0":
                                    continue
                                elif engine in BOORU_DICT.keys():
                                    print("\nInput search query (Do not input blacklist identifiers, currently supports 1 query):")
                                    query = input("# ")
                                    sys.stdout.flush()
                                    rating = Entry.get_rating()
                                    
                                    if Entry.duplicateEntryChecker(engine, query, rating) == True:
                                        print("Entry allready exists")
                                    else:
                                        print("\nInput Local blacklists seperated by a space (Press enter for None):")
                                        lob = input("# ")
                                        sys.stdout.flush()
                                        print("\nEnter the BOORU's Last ID (LID) to download from, or Enter to skip")
                                        try:
                                            response = int(input("# "))
                                            lid = response
                                        except Exception as e:
                                            lid = 0
                                        mode = "TAG"
                                else:
                                    print("Invalid Key!")
                        else:
                            print("No BOORU engines registered, please configure the BOORU registry (Configure Scraper)")
                    elif response == "2": # Pixiv Mode
                        engine = "PXV"
                        isVaildInput = False
                        while(isVaildInput == False):
                            print("\nInput qwery mode:")
                            print("[1] User ID")
                            print("[2] Tag Search")
                            isVaildInput = True
                            response = input("#: ")
                            lob = ''
                            rating = ''
                            lid = ''
                            if response == '1': # User input mode
                                mode = "USR"
                                print("\nInput Users ID's to track (seperate by spaces):")
                                query = input("# ").split(' ')

                            elif response == '2': # Tag Search mode
                                mode = "TAG"
                                print("\nInput Tags to track (seperate by spaces):")
                                query = input("# ").split(' ')
                                rating = Entry.get_rating()
                                sys.stdout.flush()
                                isVaildInput = True

                            for entry in query:
                                if entry != '':
                                    if Entry.duplicateEntryChecker(engine, entry, rating) == True:
                                        print("Entry already exists")
                                        query.remove(entry)
                                else:
                                    query.remove(entry)
                    # elif response == "3": # Deviantart Mode
                    elif response == "4":
                        print("Insert web query (or press 0 to return to the previous menu)")
                        response = input("# ")
                        if response != "0":
                            Entry.add_entry_from_query(response)
                    else:
                        return
                    
                    if query != None:
                        print("Confirm entry:")
                        print("Engine: ", engine)
                        if type(query) is list:
                            print("Queries:", end=' ')
                            for entry in query:
                                print(entry, end=' ')
                        else:
                            print("Query:  ", query, end=' ')
                        print("\nLID:    ", lid)
                        print("LOB:    ", lob)
                        print("RATING: ", rating)
                        print("Mode:   ", mode)
                        if confirm() == True:
                            print("Generating entry...")
                            if type(query) is list:
                                for entry in query:
                                    # Scraper
                                    db_query = Scraper.generate_db_ent(engine, entry, lid, lob, rating, mode)
                                    Entry(engine, entry, lid, lob, rating, mode, db_query) 
                                    Scraper.save_db(ENTRIES ,db_query, 'a')
                            else:
                                db_query = Scraper.generate_db_ent(engine, query, lid, lob, rating, mode)
                                Entry(engine, query, lid, lob, rating, mode, db_query)
                                Scraper.save_db(ENTRIES ,db_query, 'a')
                        else:
                            print("Scrapping entry...")
                    isVaildInput = False # Reset

        def add_entry_from_query(response):
            engine, query, lob, rating, lid, mode = [""] * 6
            components = response.split("/")
            if len(components) < 3:
                raise("Bad entry")
            web_base = "https://" + components[2]
            if web_base in BOORU_DICT.values():
                tag_base = components[3].split("=")[3]
                lid = 0
                rating = "ALL"
                extracted = tag_base.split("+")
                for element in extracted:
                    if len(element.split("id%3a>")) > 1:
                        lid = int(element.split("id%3a>")[1])
                    elif len(element.split("rating%3a")) > 1:
                        element = element.split("rating%3a")
                        if element[1] == "general":
                            rating = "SFE"
                        elif element[1] == "sensitive":
                            rating = "SEN"
                        elif element[1] == "explicit":
                            rating = "EXP"
                        else:
                            rating = "ALL"
                    elif element[0] == '-':
                        lob += element[1:] + ' '
                    else:
                        query = element
                # Reverse determine engine Code
                for key, value in BOORU_DICT.items():
                    if web_base == value:
                        engine = key
                        break
                mode = "TAG"
                if Entry.duplicateEntryChecker(engine, query, rating):
                    print("Duplicate Entry Detected, skipping...")
                else:
                    db_query = Scraper.generate_db_ent(engine, query, lid, lob, rating, mode)
                    Entry(engine, query, lid, lob, rating, mode, db_query)
                    Scraper.save_db(ENTRIES, db_query, 'a')
            elif web_base == "https://www.pixiv.net":
                engine = "PXV"
                mode = components[4]
                if (mode == "users"):
                    mode = "USR"
                    query = components[5]
                elif (mode == "tags"):
                    mode = "TAG"
                    query = components[5]
                if(Entry.duplicateEntryChecker(engine, query, rating)):
                    print("Module already in database, skipping...")
                else:
                    db_query = Scraper.generate_db_ent(engine, query, lid, lob, rating, mode)
                    Entry(engine, query, lid, lob, rating, mode, db_query)
                    Scraper.save_db(ENTRIES, db_query, 'a')
            else:
                print("Unrecognized Engine")
           
        def modify_entry():
            isExecuting = True
            while (isExecuting):
                print("\nSelect Engine:")
                print("[1] Booru Engine")
                # print("[2] Pixiv Engine")
                print("[0] Previous Menu")
                response = input("#: ")
                sys.stdout.flush()
                isVaildInput = True
                if response == "0":
                    return
                elif response == "1":
                    if len(BOORU_DICT) != 0:
                        isValidEngine = False
                        while (isValidEngine == False):
                            isValidEngine = True
                            print("\nSelect BOORU engine, or enter 0 to return to previous menu:")
                            Scraper.print_booru_engines()
                            engine = input("# ")
                            if engine == "0":
                                continue
                            elif engine in ENTRY_DICT.keys():
                                entries = ENTRY_DICT.get(engine)
                                for i in range(len(entries)):
                                    print("ID:                ", i)
                                    print("QUERY:             ", entries[i].query)
                                    print("Last Download ID:  ", entries[i].lid)
                                    print("Rating:            ", entries[i].rating + "\n")
                                    print("Local Blacklist:   ", entries[i].lob)
                            isVaildInput = False
                            entry = None
                            while (isVaildInput == False):
                                print("SELECT MODULE ID: [ 0, ", len(entries) - 1, "]")
                                try:
                                    response = int(input("# "))
                                    sys.stdout.flush()
                                    if (response >= 0 and response < len(entries)):
                                        isVaildInput = True
                                        entry = entries[response]
                                    else:
                                        isVaildInput = False
                                except:
                                    isVaildInput = False
                        isMoreModifications = True
                        new_lob = entry.lob
                        new_lid =  entry.lid
                        new_rating = entry.rating
                        while (isMoreModifications == True):
                            print("\n========================================")
                            print("Modifying Entry #", str(response))
                            print("========================================")
                            print("QUERY:             ", entry.query)
                            print("Local Blacklist:   ", new_lob)
                            print("Last Download ID:  ", new_lid)
                            print("Rating:            ", new_rating + "\n")
                            print("[1] Modify Last ID (LID)")
                            print("[2] Modify Local Blacklist")
                            print("[3] Modify Rating")
                            print("[9] Save Modifications")
                            print("[0] Previous Menu")
                            res = input("# ")
                            sys.stdout.flush()
                            if res == "1": # Modify LID
                                isVaildInput = False
                                while(isVaildInput == False):
                                    isVaildInput = True
                                    print("Old LID: ", entry.lid)
                                    print("Enter New LID:")
                                    try:
                                        new_lid = int(input("# "))
                                        sys.stdout.flush()
                                    except:
                                        print("Invalid LID")
                                        isVaildInput = False
                            elif res == "2": # Modify LOB
                                print("\nOld Blacklist:", entry.lob)
                                print("Enter New Blacklist (Replaces old blacklist)")
                                new_lob = input("# ")

                            elif res == "3": # Modify RATING
                                print("Old Rating:", entry.rating)
                                new_rating = Entry.get_rating()

                            elif res == "9": # Return to previous menu 
                                # Rewrite database entry
                                if confirm():
                                    entry.lob = new_lob
                                    entry.lid = new_lid
                                    entry.rating = new_rating
                                    old_db = entry.db_query
                                    entry.db_query = Scraper.generate_db_ent(entry.engine, entry.query, new_lid, new_lob, new_rating, entry.mode)
                                    Scraper.overwrite_db(ENTRIES, old_db, entry.db_query)
                                    isMoreModifications = False
                            elif res == "0":
                                isMoreModifications = False
                                print("\nScrapping entry...")
                    else:
                        print("No BOORU engines registered, please configure the BOORU registry (Configure Scraper)")
                else:
                    print("No BOORU engines registered, please configure the BOORU registry (Configure Scraper)")

        def remove_entry():
            isVaildInput = False
            engineSelection = ""
            while (isVaildInput == False):
                print("Select Engine:")
                print("[1] Booru Engine")
                print("[2] Pixiv Engine")
                print("[3] Other Engine")
                print("[0] Previous Menu")
                isVaildInput = True
                response = input("#: ")
                sys.stdout.flush()
                if response == "0":
                    return
                elif response == "1":
                    # Print Availible BOORU Engines
                    for key, value in BOORU_DICT.items():
                        print(key, "|", value)
                        isValidSelection = False
                    # Select BOORU engine to remove from
                    isVaildEngine = False
                    while (isVaildEngine == False):
                        print("Select engine to remove from:")
                        engineSelection = input("# ")
                        isVaildEngine = True if engineSelection in BOORU_DICT else False
                elif response == "2":
                    engineSelection = "PXV"
                elif response == "3":
                    engineSelection = "OTH"
                else:
                    isVaildInput = False

                entries = ENTRY_DICT.get(engineSelection)
                for i in range(len(entries)):
                    id = "[" + str(i) + "]"
                    print(id, entries[i].query)

                isVaildInput = False
                while (isVaildInput == False):
                    print("SELECT MODULE ID: [ 0, ", len(entries) - 1, "]")
                    isVaildInput = True
                    try:
                        response = int(input("# "))
                        sys.stdout.flush()
                        if (response >= 0 and response < len(entries)):
                            entry = entries[response]
                            print("Deleting Entry #", str(response))
                            print("Engine: ", entry.engine)
                            print("Query:  ", entry.query)
                            print("Mode:   ", entry.mode)
                            if confirm():
                                print("Deleting entry...")
                                old_ent = entry.db_query
                                Scraper.overwrite_db(ENTRIES, old_ent, "")
                                entries.remove(entry)
                            else:
                                print("Scrappiing Command...")
                                isVaildInput = False
                        else:
                            isVaildInput = False
                    except:
                        isVaildInput = False

        def print_entries():
            isVaildInput = False
            while (isVaildInput == False):
                print("\nSelect Engine:")
                print("[1] Booru Entries")
                print("[2] Pixiv Entries")
                print("[3] Other Entries")
                print("[0] Previous Menu")
                response = input("#: ")
                sys.stdout.flush()

                isVaildInput = True
                if response == "0":
                    return
                elif response == "1": # Booru
                    if len(BOORU_DICT) != 0:
                        isValidEngine = False
                        while (isValidEngine == False):
                            isValidEngine = True
                            print("\nSelect BOORU engine, or enter 0 to return to previous menu:")
                            Scraper.print_booru_engines()
                            engine = input("# ")
                            if engine == "0":
                                continue
                            elif engine in ENTRY_DICT.keys():
                                site = BOORU_DICT.get(engine)
                                print("ENGINE:             ", site, "[", engine, "]\n")
                                for entry in ENTRY_DICT.get(engine):
                                    print("QUERY:           ", entry.query)
                                    print("MODE:            ", entry.mode)
                                    print("LOCAL BLACKLIST: ", entry.lob)
                            else:
                                isVaildInput = False
                    else:
                        print("No BOORU engines registered, please configure the BOORU registry (Configure Scraper)")
                elif response == "2": # Pixiv
                    print("ENGINE:         ", "https://www.pixiv.net/en/ [ PXV ]\n")
                    for entry in ENTRY_DICT["PXV"]:
                        print("QUERY:           ", entry.query)
                        print("MODE:            ", entry.mode, "\n")
                        if entry.mode == "USR":
                            print("Rating:            ", entry.rating)
                elif response == "3": # Other
                    for entry in ENTRY_DICT["OTH"]:
                        print("QUERY:           ", entry.query)

        def duplicateEntryChecker(engine, query, rating):
            for entry in ENTRY_DICT[engine]:
                if query == entry.query and rating == entry.rating:
                    return True
            return False
        
        def get_rating():
            while (True):
                print("\nInput Rating # Classification:")
                print("[1] Safe")
                print("[2] Sensitive")
                print("[3] Explicit")
                print("[4] All")
                response = input("#: ")
                sys.stdout.flush()
                if response == "1": # Safe
                    return "SFE"
                elif response == "2": # Sensitive
                    return "SEN"
                elif response == "3": # Explicit
                    return "EXP"
                elif response == "4": # All
                    return "ALL"
                
####################################################################################################
# Blacklist class: functions for the global blacklist                                              #
####################################################################################################
class Blacklist:
    def add_blacklist():
        print("Enter globaly applied blacklisted tags to be added to the database (seperate with spaces):")
        response = input("# ")
        tokens = response.split(' ')
        with open(BLACKLIST, 'a') as file:
            for token in tokens:
                if (Scraper.duplicateBlacklistChecker(token) == False):
                    file.write(token + "|")
                else:
                    print(token + " is already registered to the global blacklist")

    def remove_blacklist():
        Scraper.print_blacklist()
        print("Enter Entries to remove, seperate by spaces:")
        response = input("# ").split(' ')
        for tokens in response:
            GLOBAL_BLACKLIST.remove(tokens)
        with open(BLACKLIST, 'w') as file:
            for token in GLOBAL_BLACKLIST:
                file.write(token + "|")

    def print_blacklist():
        print("Printing blacklist entries:")
        for entry in GLOBAL_BLACKLIST:
            print(entry, end=' ')
        print("")

    def duplicateBlacklistChecker(query):
        return True if query in GLOBAL_BLACKLIST else False

####################################################################################################
# Scraper class: functions for the opperations of the scraper                                      #
####################################################################################################
class Scraper:
    def init_scraper():
        # Install needed dependencies
        dependencies = ["gallery-dl", "yt-dlp"]
        for package in dependencies:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package], stdout=subprocess.DEVNULL)
        
        # Setup base structure
        if not os.path.exists(BASE_PATH):
            os.makedirs(BASE_PATH)
        
        # Setup / Load CONFIG db
        if not os.path.isfile(CONFIG):
            with open(CONFIG, 'w') as file:
                pass
        else:
            print("Loading configuration...")
            with open(CONFIG, 'r') as file:
                contents = file.read().splitlines()
            if len(contents) == 0:
                print("Registering default BOORU engine...")
                BOORU_DICT["GBU"] = "https://gelbooru.com"
                ENTRY_DICT["GBU"] = []
                Scraper.save_db(CONFIG, "GBU|https://gelbooru.com", 'a')

            for entry in contents:
                try:
                    key, val = entry.split("|")
                    BOORU_DICT[key] = val
                    ENTRY_DICT[key] = []
                except:
                    print("Error in configuration file!")

        # Register other engines
        ENTRY_DICT["PXV"] = []
        ENTRY_DICT["DVA"] = []
        ENTRY_DICT["OTH"] = []

        # Setup Log file [UNUSED]
        # if not os.path.isfile(LOG_ARCHIVE):
        #     with open(LOG_ARCHIVE, 'w') as file:
        #         pass
        
        # Load Entries from the query database
        try:
            with open(ENTRIES, 'r') as file:
                contents = file.read()
            
            # Convert old database format to new standard (Migrate database)
            if "@" in contents:
                print("Old database detected, converting to new format...")
                contents = contents.replace("@", "\n")
                with open(ENTRIES, 'w') as file:
                    file.write(contents)
                print("Database updated!", len(contents.split('\n')) - 1, "queries adjusted")

            # Load queries into program
            print("Loading entries...")
            queries = contents.split('\n')
            for query in queries:
                if query == '':
                    break
                try:
                    fragments = query.split('|')
                    Scraper.validate_entry(fragments)
                    fragments.append(query)
                    Entry(*fragments) # Generate entries from the tokenized database entries
                except Exception as e:
                    print(e.args[0], ":", query)
                    print("Deleting bad entry...")
                    Scraper.overwrite_db(ENTRIES, query, "")
        except FileNotFoundError:
            print("Creating query database...")
            with open(ENTRIES, 'w') as file:
                pass
        
        # Load Global Blacklist Database
        try:
            with open(BLACKLIST, 'r') as file:
                GLOBAL_BLACKLIST = file.read().split("|")
        except FileNotFoundError:
            print("Creating blacklist database...")
            with open(BLACKLIST, 'w') as file:
                pass
        except:
            print("Error in blacklist database")

        # Proccess Batchfile
        with open(BATCHFILE, 'a+') as file:
            file.seek(0)
            contents = file.read()
        for query in contents.splitlines():
            Entry.add_entry_from_query(query)
        with open(BATCHFILE, 'w') as file:
            pass

    def validate_entry(fragments):
        if len(fragments) < 6:
            raise Exception("Invalid fragmentation")
        if fragments[0] not in ENTRY_DICT.keys():
            raise Exception("Unrecognized Engine")
        if fragments[5] not in ["USR", "TAG"]:
            raise Exception("Invalid mode identifier")


    def generate_queries():
        # Generate Queries for dynamic engines
        for engine, entries in ENTRY_DICT.items():
            if engine in BOORU_DICT:
                web_base = BOORU_DICT.get(engine)
                for entry in entries:
                    query = web_base + "/index.php?page=post&s=list&tags="
                    query += entry.query
                    query += "+id:>" + str(entry.lid)
                    if entry.rating == "SFE":
                        query += "+rating:general"
                    if entry.rating == "SEN":
                        query += "+rating:questionable"
                    if entry.rating == "EXP":
                        query += "+rating:explicit"
                    for element in GLOBAL_BLACKLIST + entry.lob.split(" "):
                        if element != '':
                            query += "+-" + element
                    entry.generated_query = query
            elif engine == "PXV":
                for entry in entries:
                    if entry.mode == "TAG":
                        query = "https://www.pixiv.net/en/tags/"
                        query += entry.query + "/"
                        if entry.rating == "EXP":
                            query += "illustrations?mode=r18"
                        elif entry.rating == "SFE":
                            query += "illustrations?mode=safe"
                    elif entry.mode == "USR":
                        query = "https://www.pixiv.net/en/users/"
                        query += entry.query + "/"
                    entry.generated_query = query
            elif entry.engine == "OTH":
                entry.generated_query += entry.engine

    def execute_queries():
        for engine, entries in ENTRY_DICT.items():
            for entry in entries:
                print("Downloading: \n" + entry.generated_query)
                try:
                    resCapture = subprocess.run(["gallery-dl", "--download-archive", DOWNLOAD_ARCHIVES, entry.generated_query], capture_output=True, text=True)
                    if resCapture.stdout != "":
                        # print(resCapture.stdout.splitlines()[0].split('id:>')[1].split('_')[0].split(" ")[0])
                        with open(DOWNLOAD_ARCHIVES, 'a') as file:
                            # Send output to download archives
                            file.write(resCapture.stdout)
                        # Gets the LID for BRU storage
                        lid_token = resCapture.stdout.splitlines()[0].split('_')[-2] if resCapture.stdout else None
                        if (entry.engine in BOORU_DICT and lid_token != None):
                            print(lid_token)
                            old_ent = entry.db_query
                            entry.lid = lid_token
                            entry.db_query = Scraper.generate_db_ent(engine, entry.query, entry.lid, entry.lob, entry.rating, entry.mode)
                            Scraper.overwrite_db(ENTRIES, old_ent, entry.db_query)
                    print("Execution Completed\n")
                except:
                    print("Error: Failed to execute query\n")

    def print_booru_engines():
        if len(BOORU_DICT) == 0:
            print("No registered engines\n")
        else:
            print("[KEY : VALUE]")
            for key, entry in BOORU_DICT.items():
                print(key, ":", entry)
            print()

    def edit_booru_config():
        isExecuting = True
        while(isExecuting):
            print("[1] Add recognized BOORU's")
            print("[2] Edit recongized BOORU's")
            print("[3] Remove recongnized BOORU's")
            print("[4] Print recongnized BOORU's")
            print("[0] Previous menu")
            query = input("# ")
            sys.stdout.flush()
            if query == "1": # Add entry
                print("\nCurrently recognized BOORU's:")
                Scraper.print_booru_engines()
                print("Enter a BOORU site base to associate with a key, or enter 0 to cancel: (Ex: https://gelbooru.com)")
                value = input("# ")
                sys.stdout.flush()
                if value == "0":
                    continue
                elif value in BOORU_DICT.values() and value != "":
                    print(value, "is already associated with a key.\n")
                else:
                    isValidInput = False
                    while(isValidInput == False):
                        print("\nEnter a Key to associate with this site, or enter 0 to cancel: (Ex: GBRU)")
                        key = input("# ")
                        sys.stdout.flush()
                        if key == "0":
                            print("\nScrapping entry...")
                        elif key not in BOORU_DICT.keys():
                            print("\n###########################")
                            print("Key:", key)
                            print("Value:", value)
                            print("###########################")
                            if confirm():
                                BOORU_DICT[key] = value
                                with open(CONFIG, 'a') as file:
                                    file.write(key + "|" + value + "\n")
                                isValidInput = True
                            else:
                                print("\nScrapping entry...")
                        else:
                            print("Key registered to", BOORU_DICT.get(key))
            elif query == "2": # Modify entry
                # Validation checker
                if len(BOORU_DICT) == 0:
                    print("No registered engines to modify")
                    break

                Scraper.print_booru_engines()
                isValidInput = False
                while(isValidInput == False):
                    print("Select Key to modify, or enter 0 to cancel")
                    old_key = input("# ")
                    sys.stdout.flush()
                    if old_key in BOORU_DICT.keys():
                        print("\nEnter a Key to associate with", BOORU_DICT.get(old_key), " or enter 0 to cancel: (Ex: GBRU)")
                        new_key = input("# ")
                        sys.stdout.flush()
                        print("\n###########################")
                        print("Old Key:", old_key)
                        print("New Key:", new_key)
                        print("Value:", BOORU_DICT.get(old_key))
                        print("###########################")
                        if confirm():
                            old_text = old_key + "|" + BOORU_DICT.get(old_key)
                            new_text = new_key + "|" + BOORU_DICT.get(old_key) + "\n"
                            ENTRY_DICT[new_key] = ENTRY_DICT[old_key]
                            BOORU_DICT[new_key] = BOORU_DICT[old_key]
                            for entry in ENTRY_DICT[old_key]:
                                new_query = Scraper.generate_db_ent(new_key, entry.query, entry.lid, entry.lob, entry.rating, entry.mode)
                                Scraper.overwrite_db(ENTRIES, entry.db_query, new_query)
                            Scraper.overwrite_db(CONFIG, old_text, new_text)
                            del ENTRY_DICT[old_key]
                            del BOORU_DICT[old_key]

                            isValidInput = True

                        else:
                            print("\nScrapping entry...")

                        isValidInput = True
                    elif key == "0":
                        isValidInput = True
                    else:
                        print("Key is not registered to a value")
            elif query == "3":
                # Validation checker
                if len(BOORU_DICT) == 0:
                    print("No registered engines to delete")
                    break

                print("####################################################################")
                print("# WARNING! DELETING AN ENGINE ALSO DELETES ALL CORRELATED ENTRIES! #")
                print("####################################################################")
                Scraper.print_booru_engines()
                isValidInput = False
                while(isValidInput == False):
                    print("Select Key to delete, or enter 0 to cancel")
                    to_delete = input("# ")
                    sys.stdout.flush()
                    if to_delete in BOORU_DICT.keys():
                        print("WARNING: DELETING A BOORU ENGINE WILL DELETE ALL RELATED ENTRIES!")
                        if confirm():
                            for entry in ENTRY_DICT.get(to_delete):
                                Scraper.overwrite_db(ENTRIES, entry.db_query, "")
                            conf = to_delete + "|" + BOORU_DICT.get(to_delete)
                            del BOORU_DICT[to_delete]
                            del ENTRY_DICT[to_delete]
                            Scraper.overwrite_db(CONFIG, conf, "")
                            print("Engine and related entries deleted")
                            isValidInput = True
                    elif to_delete == "0":
                        print("Unrecognized engine")
                        isValidInput = True
            elif query == "4":
                Scraper.print_booru_engines()
            elif query == "0":
                return
        
    def generate_db_ent(engine, query, lid, lob, rating, mode):
        db_enc = ""
        if engine in BOORU_DICT.keys():
            db_enc += engine + "|"
            db_enc += query + "|"
            db_enc += str(lid) + "|"
            for entry in lob.split(" "):
                if entry != '':
                    db_enc += entry + " "
            db_enc += "|"
            if rating == "SFE":
                db_enc += "SFE|"
            elif rating == "SEN":
                db_enc += "SEN|"
            elif rating == "EXP":
                db_enc += "EXP|"
        elif engine == "PXV":
            db_enc += "PXV|" + str(query) + "|||"
            if mode == "TAG":
                if rating == "SFE":
                    db_enc += "SFE|"
                elif rating == "EXP":
                    db_enc += "EXP|"
            else:
                db_enc += "|"
        elif engine == "OTH":
            db_enc += engine
        else:
            print("Invalid Entry")
            return
        db_enc += mode + "\n"
        return db_enc

    def save_db(DATABASE, new_ent, IO):
        with open(DATABASE, IO) as file:
                file.write(new_ent)

    def overwrite_db(DATABASE, old_ent, new_ent):
        with open(DATABASE, "r+") as file:
            content = file.read()
            modified_content = content.replace(old_ent + "\n", new_ent)
            file.seek(0)
            file.write(modified_content)
            file.truncate()

####################################################################################################
# Log Class: Functionality for logging class                                                       #
####################################################################################################
# class Log:
    # def log(message, urgency):
        # print("")

# Confirm system
def confirm():
    while (True):
        print("Confirm entry? (y/n)")
        response = input("#: ").lower()
        sys.stdout.flush()
        if response == "y":
            return True
        elif response == "n":
            return False

# Program entry point and driver
def main():
    # Setup Phase
    print("Initializing Bot...")
    print("V:", VERSION)
    Scraper.init_scraper()

    # Automatic Execution
    if (len(sys.argv) == 2):
        if sys.argv[1] == "-e":
            Scraper.generate_queries()
            Scraper.execute_queries()
    else:
        isExecuting = True
        while(isExecuting):
            print("#   Enter Command:   #")
            print("[1] Configure BOORU engines") # Only supports 1 thing right now
            print("[2] Entry Managment")
            print("[3] View Scraper Metadata")
            print("[4] Exectute Scraper")
            print("[0] Quit")
            query = input("# ")
            if query == "1":
                # print("#   Scraper Configuration mode:   #")
                # print("[1] Edit booru engine configuration")
                print("Entering booru config")
                Scraper.edit_booru_config()
            elif query == "2": # Entry Managment
                isMoreInput = False
                while(isMoreInput == False):
                    print("#   Entry settings   #")
                    print("[1] Add Entry")
                    print("[2] Modify Entry")
                    print("[3] Delete Entry")
                    print("[4] View Entries")
                    print("#   Blacklist settings   #")
                    print("[5] Add Blacklist tags (BOORU Only)")
                    print("[6] Remove Blacklist tags (BOORU Only)")
                    print("[7] View Blacklist")
                    print("[0] Previous Menu")
                    query = input("# ")
                    if query == "1": # Add Entry
                        Entry.add_entry()
                    elif query == "2": # Modify Entry
                        Entry.modify_entry()
                    elif query == "3": # Delete Entry
                        Entry.remove_entry()
                    elif query == "4": # View Entries
                        Entry.print_entries()
                    elif query == "6": # Add to Gloabl Blacklist
                        Blacklist.add_blacklist()
                    elif query == "7": # Remove from Global Blacklist
                        Blacklist.remove_blacklist()
                    elif query == "8": # View Global Blacklist
                        Blacklist.print_blacklist()
                    elif query == "0": # Return to previous menu
                        isValidInput = True
            elif query == "3": # View Scraper Metadata
                isMoreInput = False
                while(isMoreInput == False):
                    print("#   View metadata   #")
                    print("[1] Print Entries")
                    print("[2] Print Blacklist")
                    print("[3] Print BOORU config")
                    print("[0] Previous Menu")
                    query = input("# ")
                    if query == "1": # Print entries
                        Entry.print_entries()
                    elif query == "2": # print blacklist
                        Blacklist.print_blacklist()
                    elif query == "3": # Prinr BOORU config
                        Scraper.print_booru_engines()
                    elif query == "0": # Previous Menu
                        isMoreInput = False
            elif query == "4": # Exectute Scraper
                Scraper.generate_queries()
                Scraper.execute_queries()

if __name__ == "__main__":  main()