#####################################################################
# OP-3e: Media Scraping Bot Project                                 #
# V: 0.9.0                                                          #
# Follow local laws and websites guidelines when using this scraper #
#####################################################################

####################################################################################################
# Setup Phase: Import Libraries and setup global standards                                         # 
####################################################################################################
import os
import subprocess
import sys

BASE_PATH = "internal"                                          # Root directory for databases
QUERIES = os.path.join(BASE_PATH, "query.db")                   # Database for managing internal query managment
BLACKLIST = os.path.join(BASE_PATH, "blacklist.db")             # Database for universal blacklist applications (Booru's only)
BATCHFILE = os.path.join(BASE_PATH, "batch_load.txt")           # File for batch loading in links to be automaticly executed on the bots next run 
DOWNLOAD_ARCHIVES = os.path.join(BASE_PATH, "downloaded.db")    # Database achrive of downloaded files to avoid redownloading

GLOBAL_BLACKLIST = []                                           # Internal structure for managing the globally applied blacklist (Booru's only)
GLOBAL_MODULES_MAP = {"BRU": [], "PXV": [], "OTH": []}          # Mapper for Engines to maintain a list of modules


####################################################################################################
# Scraper class: related to mechanisms of database managment, query building, and query execution  #
####################################################################################################
class Scraper:
    ####################################################################################################
    # Module class: represents an internal module to track a queries metadata                          #
    ####################################################################################################
    class Module:
        # TODO: Expand this class to support downloading a users bookmarked favorite(PXV)
        # NOTE: https://www.pixiv.net/en/users/58453252 [/bookmarks/artworks] 
        # Module initalizer, sets up metadata for a query from either the database or user input @ runtime
        def __init__(self, engine, query, lid, lob, rating, mode):
            self.engine = engine                    # Engine used to execute the query
            self.query = query                      # the query to be executed (TAG)
            self.lid = lid                          # last id of image downloaded, used in automating fresh downloads (Booru's)
            self.lob = lob                          # Local blacklisted tags
            self.rating = rating                    # Query image safety rating classification
            self.mode = mode                        # What type of query is being executed (Tag, User, etc.)
            self.generated_query = ""               # Query for execution (built from the rest of the modules metadata)
            GLOBAL_MODULES_MAP[engine].append(self) # Append this module to the mapper
        
        @staticmethod
        def create_module():
            isMoreModules, isVaildInput = True, False
            response, engine, query, lob, rating, lid, mode = [None] * 7
            # Add an engine for deviantart and X, investigate blueskies TODO
            while (isMoreModules): # While the user wants to add more entries
                while (isVaildInput == False):
                    print("\nEnter engine # to use:")
                    print("[1] Booru")
                    print("[2] Pixiv")
                    # print("[3] Deviantart [NOT IMPLEMENTED YET]") #TODO
                    print("[4] Manual mode (direct query entry)")
                    print("[0] Exit Entry mode")
                    response = input("#: ")
                    sys.stdout.flush()
                    isVaildInput = True
                    if response == '0':
                        print("Exiting input mode...\n")
                        isMoreModules = False
                        return
                    elif response == '1': # Booru
                        engine = "BRU"
                    elif response == '2': # Pixiv input mode
                        engine = "PXV"
                    elif response == '4': # Manual Mode
                        engine = "OTH"
                    else:
                        isVaildInput = False

                # Execute further steps based on the engine selected
                if engine == "BRU":
                    print("\nInput search query (Do not input blacklist identifiers, currently supports 1 query):")
                    query = input("> ")
                    sys.stdout.flush()
                    isVaildInput = False

                    while (isVaildInput == False):
                        # Determine image rating classification
                        print("\nInput Rating # Classification:")
                        print("[1] Safe")
                        print("[2] Sensitive")
                        print("[3] Explicit")
                        isVaildInput = True
                        response = input("#: ")
                        if response == '1': # Safe
                            rating = "SFE"
                        elif response == '2': # Sensitive
                            rating = "SEN"
                        elif response == '3': # Explicit
                            rating = "EXP"
                        else:
                            isVaildInput = False
                        sys.stdout.flush()
                    
                    if(Scraper.Module.duplicateModuleChecker(engine, query, rating)):
                        print("Module already in database, skipping...")
                    else:
                        print("\nInput Local blacklists seperated by a space (Press enter for None):")
                        lob = input()
                        sys.stdout.flush()
                        print("\nEnter the BOORU's Last ID (LID) to download from, or Enter to skip [QUERIES TRANSSFER MODE]")
                        try:
                            response = int(input())
                            lid = response
                        except:
                            lid = 0
                        mode = "TAG"
                        print("\nGenerating query...")
                        Scraper.Module(engine, query, lid, lob, rating, mode)
                        Scraper.Module.save_module(engine, query, lid, lob, rating, mode, 'a')
                elif engine == "PXV":
                    isVaildInput = False
                    print("\nInput qwery mode:")
                    print("[1] User ID")
                    print("[2] Tag Search")
                    while(isVaildInput == False):
                        isVaildInput = True
                        response = input("#: ")
                        if response == '1': # User input mode
                            mode = "USR"
                            print("\nInput Users ID's to track (seperate by spaces):")
                            query = input().split(' ')
                        elif response == '2': # Tag Search mode
                            mode = "TAG"
                            print("\nInput Tags:")
                            query = input()
                            isVaildInput = False
                            while (isVaildInput == False):
                                isVaildInput = True
                                print("\nInput Rating # Classification:")
                                print("[1] All")
                                print("[2] Safe")
                                print("[3] Explicit")
                                response = input("#: ")
                                if response == '1': # Safe
                                    rating = "ALL"
                                elif response == '2': # Sensitive
                                    rating = "SFE"
                                elif response == '3': # Explicit
                                    rating = "EXP"
                                else:
                                    isVaildInput = False

                            isVaildInput = False
                            while (isVaildInput == False):
                                isVaildInput = True
                                print("\Explicit?:")
                                print("[y] Yes")
                                print("[n] No")
                                isVaildInput = True
                                response = input("#: ")
                                if response == 'y': # Safe
                                    rating = "EXP"
                                elif response == 'n': # Sensitive
                                    rating = "SFE"
                                else:
                                    isVaildInput = False
                                sys.stdout.flush()

                    print("\nGenerating queries...")
                    for entry in query:
                        if entry != '':
                            if(Scraper.Module.duplicateModuleChecker(engine, query, rating)):
                                print("Module already in database, skipping...")
                            else:
                                Scraper.Module(engine, entry, lid, lob, rating, mode)
                                Scraper.Module.save_module(engine, query, lid, lob, rating, mode, 'a')
                elif (engine == "OTH"):
                    print("\nInput search query (Do not input blacklist identifiers, currently supports 1 query):")
                    query = input("> ")
                    Scraper.Module.add_module_from_query(query)
                    isVaildInput = False
                isVaildInput = False

        @staticmethod
        def del_module():
            isVaildInput = False
            while (isVaildInput == False):
                print("Select Engine:")
                print("[BRU] Booru Engine")
                print("[PXV] Pixiv Engine")
                print("[OTH] Other Engine")
                response = input("#: ")
                sys.stdout.flush()
                print("")
                isVaildInput = True
                if response in GLOBAL_MODULES_MAP:
                    modules = GLOBAL_MODULES_MAP[response]
                    for i in range(0, len(modules)):
                        print("ID:    ", i)
                        print("QUERY: ", modules[i].query)
                        print("")
                else:
                    isVaildInput = False

                modules = GLOBAL_MODULES_MAP[response]
                isVaildInput = False
                while (isVaildInput == False):
                    print("SELECT MODULE ID: [ 0, ", len(modules) - 1, "]")
                    isVaildInput = True
                    try:
                        response = int(input("> "))
                        sys.stdout.flush()
                        if (response > 0 and response < len(modules)):
                            mod = modules[response]
                            print("Deleting Entry #", str(response))
                            print("Engine: ", mod.engine)
                            print("Query:  ", mod.query)
                            modules.remove(mod)
                            print("Query Deleted")
                        else:
                            isVaildInput = False
                    except:
                        isVaildInput = False


        @staticmethod
        def add_module_from_query(response):
            # Make a better de-tokenizing system for query generation #TODO
            engine, query, lob, rating, lid, mode = [""] * 6
            components = response.split("/")
            engine = components[2].split(".")[-2]
            if (engine == "pixiv"):
                engine = "PXV"
                mode = components[4]
                if (mode == "users"):
                    mode = "USR"
                    query = components[5]
                elif (mode == "tags"):
                    mode = "TAG"
                    query = components[5]
                if(Scraper.Module.duplicateModuleChecker(engine, query, rating)):
                    print("Module already in database, skipping...")
                else:
                    Scraper.Module(engine, query, lid, lob, rating, mode)
                    Scraper.Module.save_module(engine, query, lid, lob, rating, mode, 'a')
            elif (engine == "gelbooru"):
                engine = "BRU"
                lid = "0"
                query = components[3].split("tags=")[1].split("+")[-1]
                if(Scraper.Module.duplicateModuleChecker(engine, query, "EXP")):
                    print("Module already in database, skipping...")
                else:
                    Scraper.Module(engine, query, lid, lob, "EXP", mode)
                    Scraper.Module.save_module(engine, query, lid, lob, "EXP", mode, 'a')

        @staticmethod
        def duplicateModuleChecker(engine, query, rating):
            for entry in GLOBAL_MODULES_MAP[engine]:
                if query == entry.query and rating == entry.rating:
                    return True
            return False
        
        @staticmethod
        def save_module(engine, query, lid, lob, rating, mode, IO):
            with open(QUERIES, IO) as file:
                db_enc = ""
                if engine == "BRU":
                    db_enc += "BRU|"
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
                elif engine == "OTH":
                    db_enc += engine
                db_enc += mode + "@"
                file.write(db_enc)

        @staticmethod
        def print_modules():
            isVaildInput = False
            while (isVaildInput == False):
                print("Select Engine:")
                print("[BRU] Booru Engine")
                print("[PXV] Pixiv Engine")
                print("[OTH] Other Engine")
                response = input("#: ")
                sys.stdout.flush()
                print("")
                isVaildInput = True
                if response in GLOBAL_MODULES_MAP:
                    modules = GLOBAL_MODULES_MAP[response]
                    for module in modules:
                        print("ENGINE:             ", module.engine)
                        print("MODE:               ", module.mode)
                        print("QUERY:              ", module.query)
                        print("LOCAL BLACKLIST:    ", module.lob)
                        if (module.engine == "BRU"):
                            print("LATS ID DOWNLOADED: ", module.lid)
                        print("RATING:             ", module.rating)
                        print("")
                    print("")
                else:
                    isVaildInput = False
            print("Printing modules:\n")
            for key, value in GLOBAL_MODULES_MAP.items():
                print("Engine: ", key)
                for mod in value:
                    print("Mode:   ", mod.mode)
                    print("Query:  ", mod.query)
                    if mod.engine == "BRU":
                        print("LID:    ", mod.lid)

    @staticmethod
    def bot_init():
            dependencies = ["gallery-dl"]
            for package in dependencies:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            
            # Load the QUERIES database into the program and proccess them, notify user if no query database exist
            if not os.path.exists("internal"):
                os.makedirs("internal")

            try:
                with open(QUERIES, 'r') as file:
                    contents = file.read()
                queries = contents.split('@')
                for query in queries:
                    if query == '':
                        break
                    fragments = query.split('|')
                    Scraper.Module(*fragments) # Generate modules from the tokenized database entries    
            except:
                print("No database file exists, please run -a to add queries to the query database")
            
            # Load and initialize the global blacklist, notify user if no entries exist
            try:
                with open(BLACKLIST, 'r') as file:
                    contents = file.read().split("|")
                for element in contents:
                    if element != '':
                        GLOBAL_BLACKLIST.append(element)
            except:
                print("No blacklist database file exists, please run -b to add tags to the global blacklist database")

            # Proccess Batchfile
            with open(BATCHFILE, 'a+') as file:
                file.seek(0)
                contents = file.read()
            for query in contents.splitlines():
                Scraper.Module.add_module_from_query(query)

            with open(BATCHFILE, 'w') as file:
                print("Batchfile Proccessed")

    @staticmethod
    def print_blacklist():
        print("Printing blacklist entries:")
        for entry in GLOBAL_BLACKLIST:
            print(entry)
        print()

    @staticmethod
    def generate_queries():
            for key, value in GLOBAL_MODULES_MAP.items():
                for module in value:
                    # Build the queries from the modules metadata
                    query = ""
                    if module.engine == "BRU":
                        query += "https://gelbooru.com/index.php?page=post&s=list&tags="
                        query += module.query
                        query += "+id:>" + str(module.lid)
                        if module.rating == "SFE":
                            query += "+rating:general"
                        if module.rating == "SEN":
                            query += "+rating:questionable"
                        if module.rating == "EXP":
                            if module.engine == "BRU":
                                query += "+rating:explicit" 
                        for entry in GLOBAL_BLACKLIST + module.lob.split(" "):
                            if entry != '':
                                query += "+-" + entry
                    elif module.engine == "PXV":
                        if module.mode == "TAG":
                            query += "https://www.pixiv.net/en/tags/"
                            query += module.query + "/"
                            if module.rating == "EXP":
                                query += "illustrations?mode=r18"
                            elif module.rating == "SFE":
                                query += "illustrations?mode=safe"
                        elif module.mode == "USR":
                            query += "https://www.pixiv.net/en/users/"
                            query += module.query + "/"
                    elif module.engine == "OTH":
                        query += module.engine
                    module.generated_query = query

    @staticmethod
    def execute_queries():
        for key, value in GLOBAL_MODULES_MAP.items():
            for module in value:
                print("Downloading: \n" + module.generated_query)
                try:
                    resCapture = subprocess.run(["gallery-dl", "--download-archive", DOWNLOAD_ARCHIVES, module.generated_query], capture_output=True, text=True)
                    if resCapture.stdout != "":
                        # print(resCapture.stdout.splitlines()[0].split('id:>')[1].split('_')[0].split(" ")[0])
                        with open(DOWNLOAD_ARCHIVES, 'a') as file:
                            # Send output to download archives
                            file.write(resCapture.stdout)
                        # Gets the token for BRU storage
                        lid_token = resCapture.stdout.splitlines()[0].split('_')[-2] if resCapture.stdout else None
                        if (module.engine == "BRU" and lid_token != None):
                            print(lid_token)
                            module.lid = lid_token
                    print("Execution Completed\n")
                except:
                    print("Error: Failed to execute query\n")

    @staticmethod
    def save_queries():
        for key, value in GLOBAL_MODULES_MAP.items():
            for m in value:
                Scraper.Module.save_module(m.engine, m.query, m.lid, m.lob, m.rating, m.mode, 'w')

    @staticmethod
    def duplicateBlacklistChecker(query):
        for entry in GLOBAL_BLACKLIST:
            if (query == entry):
                return True
        return False

# Program entry point
def main():
    # Setup Step
    Scraper.bot_init()

    

    isExecuting = True

    # Automatic execution when called from a schedular
    if (len(sys.argv) == 2):
        if sys.argv[1] == "-e":
            Scraper.generate_queries()
            Scraper.execute_queries()
            Scraper.save_queries()
            isExecuting = False

    # Promting Stage
    while(isExecuting):
        print("Enter Command:")
        print("[e]  EXECUTE")
        print("[c]  Create entries")
        print("[d]  Delete entries")
        print("[b]  add to global blacklist (Booru's only)")
        print("[pm] Print active modules")
        print("[pb] Print global blacklist")
        print("[q]  To quit")
        query = input("> ")
        if query == "e":
            print("Execuitng database queries, this may take a while...")
            Scraper.generate_queries()
            Scraper.execute_queries()
            Scraper.save_queries()
        elif query == "c":
                Scraper.Module.create_module()
        elif query == "d":
                Scraper.Module.del_module()
        elif query == "b":
            print("Enter globaly applied blacklisted tags to be added to the database (seperate with spaces):")
            response = input()
            tokens = response.split(' ')
            with open(BLACKLIST, 'a') as file:
                for token in tokens:
                    if (Scraper.duplicateBlacklistChecker(token) == False):
                        file.write(token + "|")
                    else:
                        print(token + " is already registered to the global blacklist")
        elif query == "pm":
            Scraper.Module.print_modules()
        elif query == "pb":
            Scraper.print_blacklist()
        elif query == "q":
            print("shutting down...")
            isExecuting = False
    
if __name__ == "__main__":  main()
####################################################################################################
# Developers TODO:
# Implement video scraping (Tall order, low priority, do everything else first)
# Implement the readme
# Add step back functionality across the program
####################################################################################################