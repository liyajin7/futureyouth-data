from bs4 import BeautifulSoup as bs4
import requests, sys, time, re, csv, joblib

# Initialized for timing stats
t0 = time.time()

# Flag for input: 0 to write URLs to individual files, 1 for single set
flag = int(sys.argv[1])

# Get HTML from URL
response = requests.get("https://www.olympedia.org/editions/62/result")
# response = requests.get("https://www.olympedia.org/editions/60/result")
html = response.content

# Timing response time
resp_t1 = time.time()

# Create bs4 object
game_soup = bs4(html, 'lxml')

# Given a Game Results Page for a Game, find all Event Result Page URLs
event_urls = list(())
for tag in game_soup.find_all(href=re.compile("/results/\d{6,7}")):
    event_urls.append([tag.string, tag.get("href")])        # 1st dimension will be 1-indexed, 2nd 0-indexed

match flag:
    case 0:
        i = 0

        athls = list()
        urls = list()

        for url in event_urls:
            # Setting up new beautifulsoup for each event page
            curr_url = "https://www.olympedia.org" + url[1]
            curr_response = requests.get(curr_url)
            curr_html = curr_response.content
            curr_event_soup = bs4(curr_html, 'lxml')
            
            # Opening new file to write to
            orig_stdout = sys.stdout
            txt_name = "2018_event_athls/" + re.sub(r'/', r'-', url[0]) + ".txt"
            f = open(txt_name, 'w')
            sys.stdout = f
            
            # Returns True if a given tag contains Athlete Page URL for a ranked athlete
            def is_ranked_athlete(tag):
                if not isinstance(tag.get("href"), str): return None
                else:
                    athl_url = re.compile("/athletes/\d{5,6}")
                    return bool(athl_url.match(tag.get("href"))) and not tag.parent.has_attr("style") and tag.parent.name != 'p'
                
            # Only gets athlete tags in overall rankings, ignoring those in heats/qualifier listings if those exist for that event
            athl_set = []
            if isinstance(curr_event_soup.find("h2"), type(None)):
                athl_set = curr_event_soup.find_all(is_ranked_athlete)
            else:
                athl_set = curr_event_soup.find("h2").find_all_previous(is_ranked_athlete)
                athl_set.reverse()   # @LIYA maybe eventually take this out for speed. could also remove this if just adding all athlete URLs to a set???
                
            for tag in athl_set:
                print(tag.string, "\t", tag.get("href"))

            sys.stdout = orig_stdout
            f.close()
            
            i += 1

    case 1: 
        # # Opening new file to write to
        # orig_stdout = sys.stdout
        
        # # f = open('cum_lists/2018_ALL_IDs.txt', 'w')
        # sys.stdout = f

        unique_athls = set()

        i = 0
        for url in event_urls:
            # Setting up new beautifulsoup for each event page
            curr_url = "https://www.olympedia.org" + url[1]
            curr_response = requests.get(curr_url)
            curr_html = curr_response.content
            curr_event_soup = bs4(curr_html, 'lxml')
                        
            # Returns True if a given tag contains Athlete Page URL for a ranked athlete
            def is_ranked_athlete(tag):
                if not isinstance(tag.get("href"), str): return None
                else:
                    athl_url = re.compile("/athletes/\d{5,6}")
                    return bool(athl_url.match(tag.get("href"))) and not tag.parent.has_attr("style") and tag.parent.name != 'p'
            
            # Only gets athlete tags in overall rankings, ignoring those in heats/qualifier listings if those exist for that event
            athl_set = []
            if isinstance(curr_event_soup.find("h2"), type(None)):
                athl_set = curr_event_soup.find_all(is_ranked_athlete)
            else:
                athl_set = curr_event_soup.find("h2").find_all_previous(is_ranked_athlete)
                athl_set.reverse()   # @LIYA maybe eventually take this out for speed. could also remove this if just adding all athlete URLs to a set???
            
            for tag in athl_set:
                just_id = re.sub('^/athletes/', '', tag.get("href"))

                # @Liya turns out adding IDs as a set results in 20 less athletes (leading zeros)? map with unique names just in case
                unique_athls.add((tag.string, just_id))   
            
            i += 1

        # for el in unique_athl_ids:
        unique_athls = list(unique_athls)

        # with open('cum_lists/2018_ALL_NAMES-IDs.txt', 'w') as f:
        with open('cum_lists/2022_ALL_NAMES-IDs.txt', 'w') as f:
            f.write("[")
            for el in unique_athls:
                f.write(str(el))
                f.write(",\n")
            f.write("]")

        # sys.stdout = orig_stdout
        # f.close()

### file-writing time
t1 = time.time()

resp_total = resp_t1-t0
full_total = t1-t0
print("Response time: ", resp_total, "\nTotal runtime: ", full_total)
