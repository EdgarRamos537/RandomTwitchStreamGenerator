# Imports
import json, requests, io, random, re, pyperclip, pretty_errors

########################################################
################### Helper Functions ###################
########################################################

# Helper Function to strip spaces and format game names for searching
def noSpaces(string:str):
    tagRegex = re.compile(r'(\w){8}-(\w\w\w\w-){3}(\w){12}')
    mo1 = tagRegex.search(string)
    mo2 = re.findall(r'".*"', string)
    count = 0
    stringList = [] 
    
    # Returns a Stream Tag with no additional characters or spaces
    if mo1 != None:
        return mo1.group()
    # Else returns a list of games in the proper format
    else:
        # Formating any game with the specified delimiter "," to be included in search 
        if mo2 != []:
            mo2 = str(mo2).replace("'", '').replace('[', '').replace(']', ''). replace('", ', '"\n')
            mo2 = mo2.splitlines()
            
            for i in range(len(mo2)):
                string = string.replace(mo2[i], '').strip()
                mo2[i] = mo2[i].replace('"', '')
            
            # Creating a list of games w/o "," in their name
            if string != '':
                stringList = string.split(',')
            
                for i in range(len(stringList)):
                    if len(stringList[i - count]) == None or len(stringList[i - count]) == 0 or stringList[i - count].isspace():
                        stringList.pop(i - count)
                        count += 1                 
            
                    if len(stringList) != 0:    
                        stringList[i - count] = stringList[i - count].strip() 
            
            for j in range(len(mo2)):
                stringList.append(mo2[j]) 
            
            return stringList
            
        # Formats and returns a list of games w/o "," in their name
        else: 
            stringList = string.split(',')
            for i in range(len(stringList)):
                stringList[i] = stringList[i].strip()  
            
            return stringList

# Helper Function that returns json data for Games
def games(gamesIncluded, gamesExcluded):
    CLIENT_ID = '---'
    TOKEN = '---'
    PARAMS2 = {
               "Client-Id": CLIENT_ID,
               "Authorization": f"Bearer {TOKEN}"
              }
    
    # Formatting user inputted string
    gamesIncluded = noSpaces(gamesIncluded)
    gamesExcluded = noSpaces(gamesExcluded)

    # Check if user wants to search for specific game(s) 
    if gamesIncluded != [''] and gamesIncluded != None:
        count = 0
        
        # For-loop to request json data using Twitch API for a specific game
        for name in gamesIncluded:
            url = ("https://api.twitch.tv/helix/games?name=" + str(name)).replace('&', '%26').replace('+', '%2B')
            r = requests.get(url = url, headers= PARAMS2)
            r.raise_for_status()
            
            data = r.json()
            
            if len(data['data']) != 1:
                return None

            with open('game' + str(count) + '.txt', 'w') as outfile:
                json.dump(data, outfile, sort_keys=True)
            
            count += 1
        
        # If user requested more than one game, each games' json data will be combined into one json file
        if count > 1:
            with open('game0.txt', 'r') as data:
                contents = data.read()
                gamesResult = contents[:contents.rfind(']')] + ', '
                
                for i in range(1, len(gamesIncluded)):
                    if i == len(gamesIncluded) - 1:
                        with open('game' + str(i) + '.txt', 'r') as data:
                            contents = data.read()
                            gamesResult = gamesResult + contents[10:]
                    else:
                        with open('game' + str(i) + '.txt', 'r') as data:
                            contents = data.read()
                            gamesResult = gamesResult + contents[10:contents.rfind(']')] + ', '
                            
        
            data = json.loads(gamesResult)

        with open('games.txt', 'w') as outfile:
            json.dump(data, outfile, sort_keys=True, indent= 4)
        
        return data            
    
    # Else Twitch's Top 200 Games are collected in a json file and returned
    else:
        # Games 0-99
        count = 0
        url = "https://api.twitch.tv/helix/games/top?first=100"

        r = requests.get(url = url, headers= PARAMS2)
        r.raise_for_status()

        gamesSet1 = r.json()

        with open('top100.txt', 'w') as outfile:
            json.dump(gamesSet1, outfile, sort_keys=True)
            
        # Games 100-199
        next100 = '&after=' + str(gamesSet1['pagination']['cursor'])
        url = url + next100
        
        r = requests.get(url = url, headers= PARAMS2)
        r.raise_for_status()

        gamesSet2 = r.json()
        
        with open('top200.txt', 'w') as outfile:
            json.dump(gamesSet2, outfile, sort_keys=True)  
            
        # Combining the Game Data
        with open('top100.txt', 'r') as data:
            contents = data.read()
            gamesData = contents[:contents.rfind(']')] + ', '
                    
        with open('top200.txt', 'r') as data:
            contents = data.read()
            gamesData = gamesData + contents[10:]
            
        data = json.loads(gamesData)
        
        # Removing any requested game from the Top 200
        if gamesExcluded != ['']:
            for i in range(len(data['data'])):
                if data['data'][i - count]['name'] in gamesExcluded:
                    data['data'].pop(i - count)
                    count += 1

        return data
    
# Helper Function to convert user select language to corresponding ISO 639-1 codes
def langISO(language:str):
    languages = {
             'english': 'en',
             'spanish': 'es',
             'german': 'de',
             'portuguese': 'pt',
             'russian': 'ru',
             'korean': 'ko',
             'french': 'fr',
             'japanese': 'ja',
             'chinese': 'zh',
             'italian': 'it',
             'turkish': 'tr',
             'polish': 'pl',
             'arabic': 'ar',
             'thai': 'th',
             'czech': 'cs',
             'hungarian': 'hu',
             'dutch': 'nl',
             'finnish': 'fi',
             'swedish': 'sv',
             'danish': 'da',
             'norwegian': 'no',
             'greek': 'el',
             'romanian': 'ro',
             'slovak': 'sk',
             'bulgarian': 'bg',
             'indonesian': 'id',
             'ukrainian': 'uk',
             'tagalog': 'tl',
             'catalan': 'ca',
             'hindi': 'hi',
             'malay': 'ms',
             'vietnamese': 'vi',
             'other': 'other'
            }

    if language.lower() in languages.keys() or language.lower() in languages.values():
        if language.lower() == 'other':
            string = language.lower()
            return string
        
        elif len(language) != 2:
            string = str(languages.get(language.lower()))
        
            return string
        else:
            string = language.lower()
            return string
            
########################################################
  #################  Main Function  ##################
########################################################

# Function that returns Twitch URL 
def randomStream(gamesIncluded=[], gamesExcluded=[], lang='All', top=200, minViewers=0, maxViewers=10000000,
                 FF=False, charity=False, notSponsored=False, vtuber=False, CC=False, tag=''):
    gamesData = games(gamesIncluded, gamesExcluded)
    gameCount = 0
    CLIENT_ID = '---'
    TOKEN = '---'
    
    # If gamesData returns None (because game with , had no "" around title or misspelling)
    if gamesData == None:
        return 'Error occurred. Please check spelling and put "" around any game title that includes a comma(,)'
    else:
        initialSize = len(gamesData['data'])
    
    # Alters value of top for non-default values of gamesIncluded and gamesExcluded
    if len(gamesIncluded) != 0 or len(gamesExcluded) != 0:
        # If user request value for top is less than Games Data length, top becomes user value
        if top <= len(gamesData['data']):
            top = top
        # Else top = length of Games Data json
        else:
            top = len(gamesData['data'])
    
    # Continually searches for stream that meets the search criteria
    while True:
        # If 200-top Games remain in Games Data, function returns None
        if len(gamesData['data']) == initialSize - top:
            print('\nSorry, no matches were found.')
            break
    
        else:
            game = random.randint(0, top - 1 - gameCount)
            gameID = str(gamesData['data'][game]['id'])
            # URL for selected language
            if lang != 'All':
                lang = str(langISO(lang))
                language = '&language=' + lang
                url = 'https://api.twitch.tv/helix/streams?first=100&game_id=' + gameID + language
            # URL for all languages
            else:
                url = 'https://api.twitch.tv/helix/streams?first=100&game_id=' + gameID
                
        PARAMS2 = {
                   "Client-Id": CLIENT_ID,
                   "Authorization": f"Bearer {TOKEN}"
                  }

        r = requests.get(url = url, headers= PARAMS2)
        r.raise_for_status()

        # Streamer Data for randomly selected game
        data = r.json()
        
        # If game has no live streams playing it, returns None
        if len(data['data']) == 0:
            #print('\nSorry, no matches were found.')
            #break
            gamesData['data'].pop(game)
            gameCount += 1
            continue

        ###############################################################################################
        ### Filter variables ###
        
        # Min Viewers
        if minViewers != 0:
            count = 0
            for i in range(len(data['data'])):
                    if data['data'][i - count]['viewer_count'] <= minViewers:
                        data['data'].pop(i - count)
                        count += 1
        
        # Max Viewers
        if maxViewers != 10000000:
            count = 0
            for i in range(len(data['data'])):
                    if data['data'][i - count]['viewer_count'] >= maxViewers:
                        data['data'].pop(i - count)
                        count += 1
        
        # Family-Friendly
        if FF == True:
            count = 0
            length = len(data['data'])
            for i in range(length):
                if data['data'][i - count]['tag_ids'] == None:
                    data['data'].pop(i - count)
                    count += 1
                elif 'e90b5f6e-4c6e-4003-885b-4d0d5adeb580' not in data['data'][i - count]['tag_ids']:
                    data['data'].pop(i - count)
                    count += 1
                    
        # Charity Stream
        if charity == True:
            count = 0
            length = len(data['data'])
            for i in range(length):
                if data['data'][i - count]['tag_ids'] == None:
                    data['data'].pop(i - count)
                    count += 1
                elif 'bb5e7234-380e-48ad-a59c-03e51274e478' not in data['data'][i - count]['tag_ids']:
                    data['data'].pop(i - count)
                    count += 1
        
        # Non-sponsored Streams
        if notSponsored == True:
            count = 0
            for i in range(len(data['data'])):
                if "#ad" in str(data['data'][i - count]['title']).lower():
                    data['data'].pop(i - count)
                    count += 1
                    
        # V-Tuber
        if vtuber == True:
            count = 0
            length = len(data['data'])
            for i in range(length):
                if data['data'][i - count]['tag_ids'] == None:
                    data['data'].pop(i - count)
                    count += 1
                elif '52d7e4cc-633d-46f5-818c-bb59102d9549' not in data['data'][i - count]['tag_ids']:
                    data['data'].pop(i - count)
                    count += 1
                    
        # Closed-Captions
        if CC == True:
            count = 0
            length = len(data['data'])
            for i in range(length):
                if data['data'][i - count]['tag_ids'] == None:
                    data['data'].pop(i - count)
                    count += 1
                elif '8a01ea18-df97-4046-9cff-a9a822bb96e5' not in data['data'][i - count]['tag_ids']:
                    data['data'].pop(i - count)
                    count += 1
        
        # User-Entered Tag
        if tag != '':
            count = 0
            length = len(data['data'])
            for i in range(length):
                if data['data'][i - count]['tag_ids'] == None:
                    data['data'].pop(i - count)
                    count += 1
                elif noSpaces(tag) not in data['data'][i - count]['tag_ids']:
                    data['data'].pop(i - count)
                    count += 1
        
        ###############################################################################################
        
        # If all streams in a game category were popped the game is removed from Games Data and another is chosen
        if len(data['data']) == 0:
            gamesData['data'].pop(game)
            gameCount += 1
            continue
        
        # Else streamer's URL is returned
        else:
            streamer = random.randint(0, (len(data['data']) - 1))
            link = ('https://www.twitch.tv/' + data['data'][streamer]['user_login'])
            return(str(link))