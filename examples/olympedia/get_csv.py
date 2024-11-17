from bs4 import BeautifulSoup as bs4
import requests, sys, time, re, ast, datetime
import unicodecsv as csv
from io import BytesIO

# Initialized for timing stats
t0 = time.time()

# Initialize soup & athletes
with open('cum_lists/2018_ALL_NAMES-IDs.txt','r', encoding='utf-8') as f:
   athls_2018 = ast.literal_eval(f.read())

with open('cum_lists/2022_ALL_NAMES-IDs.txt','r', encoding='utf-8') as f1:
   athls_2022 = ast.literal_eval(f1.read())

athls = list(set(athls_2018) | set(athls_2022))
# athls = athls_2018

# TEMP WRITING
# with open('cum_lists/2018+2022_ALL_NAMES-IDs.txt', 'w') as f:
#     f.write("[")
#     for el in athls:
#         f.write(str(el))
#         f.write(",\n")
#     f.write("]")

# Hardcoded
games = {
    '2018': 'PyeongChang',
    '2022': 'Beijing'
}

# CSV variables
header = ["id", "name", "sex", "age", "height", "weight", "team", "noc", "year", "city", "sport", "event", "medal"]
# f = open('2018_games.csv', 'wb')
# f = open('2022_games.csv', 'wb')
f = open('2018+2022_Winter_Olympic_Data.csv', 'wb')
writer = csv.writer(f, dialect='excel', encoding='utf-8')
f.seek(0)
writer.writerow(header)

# Iterate over every athlete in list
for athl in athls:

    # WITH WIFI: Get webpage content
    athl_url = "https://www.olympedia.org/athletes/" + athl[1]
    response = requests.get(athl_url)
    html = response.content
    resp_t1 = time.time()
    athl_soup = bs4(html, 'lxml')

    # Checks whether athlete is just a Coach
    role_tag = athl_soup.find_all('th', string="Roles")[0]
    if not bool(re.compile("^Competed").match(role_tag.parent.find_all('td')[0].string)):
        continue
    
    # FOR LOCAL TESTING. for some reason, bday_str doesn't work...
    # HTMLFile = open("athlete_pages/TEST_athl_bøkko.txt", "r") 
    # index = HTMLFile.read() 
    # athl_soup = bs4(index, 'lxml') 

    # Get sex
    sex = athl_soup.find('table',class_='biodata').find_all('td')[1].text.strip()[0]

    # Get height & weight @LIYA could build smth in for "NA" entries, and make averages for "76-81 kg"
    height = weight = "NA"
    meas_ls = athl_soup.find_all('th', string="Measurements")#.find('table',class_='biodata').find_all('th', string="Measurements")
    
    if len(meas_ls) != 0:
        meas_tr_tag = meas_ls[0].css.closest('tr')
        whole_str = meas_tr_tag.find('td').text
        if ("/" in whole_str):
            [height, weight] = meas_tr_tag.find('td').text.split(" / ")
            [height, weight] = [re.split(r'\D+',height)[0], re.split(r'\D+',weight)[0]]
        else: height = meas_tr_tag.find('td').text.split(" / ")[0].split(' cm')[0]

    # Get affiliations
    aff = athl_soup.find('table',class_='biodata').select('a[href^="/countries"]')[0]
    team = aff.text.strip().split(" in")[0]
    if bool(re.compile("^People's").match(team)):
        team = team.split()[-1]
    noc = aff.get('href')[-3:]

    # Common elements for each row of this athlete's data
    common_els = [athl[1], athl[0], sex, '', height, weight, team, noc]
    
    # Gets tag for current Game in the table
    all_h2s = athl_soup.find_all("h2")[1]
    curr_game_tag = all_h2s.find_all_next('a', string=re.compile('^(:?2018|2022)'))[0]
    
    # Function for determining metal status
    def get_medal(ptag):  # returns a string
        medal_pos = "NA"        
        curr = ptag.parent.find('span', class_=re.compile('^(?:Gold|Silver|Bronze)'))
        if not isinstance(curr, type(None)):
            medal_pos = curr.string

        return medal_pos

    # Initialize for while loops
    next_game = curr_game_tag
    next_sport = curr_game_tag.find_next('a', href=re.compile('^/sports/'))
    next_event = curr_game_tag.find_next('a', href=re.compile('^/results/'))
    next_event_href = next_event.get('href')
    game_pat = re.compile('^/editions/')
    event_pat = re.compile('^/results/')

    # Loops until there are no more games
    while not isinstance(next_game, type(None)):
        switch_game = False
        curr_year = next_game.string[:4]
        curr_city = games.get(curr_year)

        # Get birth string and convert to age based on year of games. Take games date as Feb 5, YEAR.
        birth_tag = athl_soup.find(string=re.compile('^\d{1,2} (?:January|February|March|April|May|June|July|August|September|October|November|December) (?:[0-9][0-9])?[0-9][0-9]'))
        bday_str = birth_tag.text.split(" in")[0]
        bday_dt = datetime.datetime.strptime(bday_str, '%d %B %Y').date()       # td = datetime.datetime.now().date() 
        game_date = datetime.datetime(int(curr_year), 2, 5).date()
        age_years = int((game_date-bday_dt).days/365.25)
        common_els[3] = age_years
        
        # Loops until there are no more sports left for that games
        while not isinstance(next_sport, type(None)):
            
            # Get sport string to store into csv
            curr_sport = next_sport.string

            # Loops until there are no more events left for that games
            while not isinstance(next_event, type(None)) and not switch_game:
                
                # Get name of current athlete's event for sport & game, as appropriate based on format
                curr_event = curr_sport + " "
                event_els = next_event.string.split(", ")
                mf_pat = re.compile('(?:Men|Women)')
                if len(event_els) == 2:
                    if bool(mf_pat.match(event_els[1])):
                        curr_event += event_els[1] + "'s " + event_els[0]
                    else:
                        curr_event += event_els[1] + " " + event_els[0]
                else:
                    curr_event += event_els[2] + "'s " + event_els[0] + ", " + event_els[1]

                # Get medal status
                medal = get_medal(next_event.parent)

                # Write all data as one entry @LIYA need to fix the UTF-8 encoding problem... how to get special chars?
                w_data = common_els + [curr_year, curr_city, curr_sport, curr_event, medal]
                writer.writerow(w_data)            
                
                # Update to next event in list, if there is one
                next_a = next_event.find_next('a')
                next_a_href = next_a.get('href')

                # Determine whether need to move onto next games
                switch_game = bool(game_pat.match(next_a_href))

                # Update to next_event
                if event_pat.match(next_a_href):
                    next_event = next_a
                else:
                    next_event = next_a.find_next('a', href=re.compile('^/results/'))
            
            # Update to next sport in list, if there is one
            if switch_game: break
            else:
                next_sport = next_sport.find_next('a', href=re.compile('^/sports/'))

        next_game = next_game.find_next('a', href=re.compile('^/editions/'))


### time file-writing time
t1 = time.time()

resp_total = resp_t1-t0
full_total = t1-t0
print("\nResponse time: ", resp_total, "\nTotal runtime: ", full_total)



####### SCRAPS

# pat = re.compile('^\d{1,2} (?:January|February|March|April|May|June|July|August|September|October|November|December) (?:[0-9][0-9])?[0-9][0-9]')
# born_tag = athl_soup.find('table',class_='biodata').find_all('th', string="Born")[0]
    # print("—————OLD BORN TAG? ", born_tag)
    # birth_tr_tag = born_tag.css.closest('tr')

# aff = athl_soup.find('table',class_='biodata').find_all('a')[2]
# print("Aff: ", aff)
# team = aff.text.strip().split(" in")[0]

# next_sib = meas_tag.next_sibling()
# print("meas_tag: ", meas_tag, "\nnext_sib!", next_sib)

# print("MEASUREMENTS LIST? ", meas_ls)
    # print("MEASUREMENTS LS TYPE? ", type(meas_ls))
    # print("MEASUREMENTS LS LEN? ", len(meas_ls))
    # print("Height: ", height)
    # print("Weight: ", weight)
# [height, weight] = athl_soup.find('table',class_='biodata').find_all('td')[5].text.strip().split(" / ")
# print("—————NEW BIRTHDATE FIND? ", birth_tag)
    # bday_str = birth_tag.find('td').text.split(" in")[0]
    
# find winter olympics area
    # wo2018_tag = athl_soup.find('a',href='biodata').find_all('th', string="Measurements")
    # try1 = athl_soup.find("h3").find_all_previous('a',href=re.compile('^/editions/'))
    # dive1 = try1.select()
    # try2 = athl_soup.find("h3").find_previous('tr',class_="active").find_all('a', href=re.compile('^/editions/'))

            # print("Medal: ", medal)
            # print("\n", common_els[1], ":")
            # print("Sport: ", curr_sport)
            # print("Event: ", curr_event)
            # print("Medal: ", medal)
            # # print("type(common_els): ", type(common_els))
            # print("common_els.extend(curr_sport): ", common_els.extend([curr_sport]))
            
            # print("NEW ENTRY:\n", w_data)

# print(common_els)
            # print("FINAL DATA TO WRITE: ", db_line)

# print("Data for ", athl[0], ": ", common_els)

    ##### NEXT STEPS
    # get all text (href'd) for sports in YEAR Winter Olympics
    # get all text (href'd) for events in YEAR Winter Olympics

        # print("\n———————RUNNING get_medal")

        # print("ptag (tag passed into get_medal): ", ptag)
        
        # IN THE REAL THING, FOR SOME REASON, IT'S contents[8]
        # curr = ptag.parent.contents[17].find('span')


    # NEED TO FIX THIS FOR ATHLETES WITH MULTIPLE SPORTS. while loop while find_next is not empty??
    # sport1 = curr_game_tag.find_next('a', href=re.compile('^/sports/')).string
    # print("FIRST SPORT: ", sport1)

    # find next event. also maybe a while loop
    # event1 = curr_game_tag.find_next('a', href=re.compile('^/results/')).string
    # print("FIRST EVENT: ", event1)

    # sport1 = curr_game_tag.find_next_sibling()
  


# Write to testing file (@LIYA for now)
# orig_stdout = sys.stdout
# f = open('athlete_pages/TEST_athl_bøkko.txt', 'w')
# sys.stdout = f

# PRETTY PRINT
# print(athl_soup.prettify())

# sys.stdout = orig_stdout
# f.close()