from bs4 import BeautifulSoup as bs4
import requests, sys, time, re

t0 = time.time()


# REWRITE FOR EFFICIENCY INTO WHILE LOOP
response = requests.get("https://www.olympedia.org/results/9001072")
if response.status_code != 200:
	print("Error fetching page")
	exit()
elif response.status_code == 404:
	print("ERROR CODE 404")
	# exit into next URL in the loop
else:
	html = response.content


### timing response time
resp_t1 = time.time()


# create bs4 object
soup = bs4(html, 'lxml')
# links = soup.find_all("a") #####


### timing creation of bs4 shit
soup_t1 = time.time()


# Opens file to write to
orig_stdout = sys.stdout
f = open('event_pages/athls_2018_masstart_wmen.txt', 'w')
sys.stdout = f

##### FIND ALL URLs on page, period
# for link in links:
# 	print("Link: ", link.get("href"), "\nText: ", link.string, "\n")

##### PRETTY PRINT EVERYTHING ON PAGE
# print(soup.prettify())

##### [YEAR] Results Page: FIND ALL EVENT URLs 
# for tag in soup.find_all(href=re.compile("/results/\d{6,7}")):
#     print(tag.get("href"))
#     print(tag.string)
#     print()


##### Event Page: FINDS ALL ATHLETE TAGS: 
# for tag in soup.find_all(href=re.compile("/athletes/\d{5,6}")):

##### Event Page: FINDS 1 SPORT URL
# print("\n\nHERE'S THE SPORT: ")
# soup.find(href=re.compile("/editions/\d{2}/sports/\w{3}")).string

##### Event Page: FINDS 1 YEAR URL
# soup.find(href=re.compile("/editions/\d{2}")).string[:4]

##### Event Page: FIND ALL ATHLETE URLs NOT in a paragraph or as course setter
def is_ranked_athlete(tag):
	if not isinstance(tag.get("href"), str): return None
	else:
		athl_url = re.compile("/athletes/\d{5,6}")
		return bool(athl_url.match(tag.get("href"))) and not tag.parent.has_attr("style") and tag.parent.name != 'p'
	# <td> parent tag of <a href></a> can't have style attribute

def get_medal(ptag):  # returns a string
	# print("\n\n\n——————RUNNING get_medal: ", tag)
	medal_pos = "NA"    

	# Checks whether there's a medal for that athlete: if so, sets medal_pos appropriately; if not, keeps N/A
	for sib in ptag.find_next_siblings():
		curr = sib.find('span')
		if bool(curr):
			# print("Found sibling with span tag!! It's:\n", sib.find('span'))

			if bool(re.search("^[GSB]", curr.string)):
				# print("———Match for a medal!!! ", curr.string)
				medal_pos = curr.string
	
	# curr = ptag.parent.contents[8].find('span')
	# if not isinstance(curr, type(None)):
	# 	medal_pos = curr.string
	# print("Medal position: ", medal_pos)
	return medal_pos


##### GETS ATHLETE TAGS BEFORE heats/qualifier listings, if those exist.
athl_set = []
if isinstance(soup.find("h2"), type(None)):
    athl_set = soup.find_all(is_ranked_athlete)
else:
	stop_at = soup.find("h2")
	athl_set = stop_at.find_all_previous(is_ranked_athlete)
	athl_set.reverse()   # NOTE FOR LIYA maybe eventually take this out for speed:

for tag in athl_set:
# 	# print("————RUNNING for loop for tags in athl_set")
	print(tag.string)
# 	# print("CURRENT TAG: ", tag)
# 	# print("CURRENT PTAG: ", tag.parent)
	print(get_medal(tag.parent), "\n")

## OLD method of doing this with sets:
# athl_set = {""}
# for tag in soup.find_all(is_ranked_athlete):
	###### NOTE FOR LIYA: make sure when you put this into main code, you're adding ALL the info you need to the set.
	# print(tag.get("href"))
	# print(tag.string)
	# athl_set.add(tag.string)
# Getting rid of duplicates: this works!!! might be slower tho than checking medals.
# new_athl_set = list(athl_set)
# print(*new_athl_set, sep = "\n")

sys.stdout = orig_stdout
f.close()



### time file-writing time
write_t1 = time.time()

# performance testing
resp_total = resp_t1-t0
soup_total = soup_t1-resp_t1
write_total = write_t1-soup_t1
full_total = write_t1-t0

print("Response time: ", resp_total, "\nBeautifulSoup link-find: ", soup_total, "\nWriting to file: ", write_total, "\nTOTAL: ", full_total)




####### ON EACH EVENT RESULTS PAGE, https://www.olympedia.org/results/[*******] ######

# ORIG FIELD HEADERS: id	name	sex	age	height	weight	team	noc	year	city	sport	event	medal

# same from event to event:

# ✅ go through each URL on the page that takes the form "/results/[*******]" where 7 *'s are ints.
# these are the EVENT URLs.

# ON EACH EVENT URL PAGE, 
    #### each ATHLETE in each EVENT has the same YEAR, SPORT, EVENT, CITY. ####

    # EVENT_COMMON = common list of elements for each EVENT

    ## SPORT - DONE
    # store the link.string for the link.get("href") that's of the form /editions/[**]/sports/[***].

    ## YEAR
    # the link.string for the link.get("href") that's of the form /editions/[**] and ends there. (the first 4 chars to get just the year)

	## CITY
	# don't need to scrape: not on page!!!!!!!! can manually add it back in.
	
	###

	# go through each URL on the page that _____________. these are the ATHLETE URLs.

# SPORT: 