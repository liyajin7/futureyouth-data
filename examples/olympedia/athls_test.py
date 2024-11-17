from bs4 import BeautifulSoup as bs4
import requests, sys, time, re

# Opening the html file 
HTMLFile = open("pprint_2018_1500_wmen.html", "r") 
  
# Reading the file 
index = HTMLFile.read() 
  
# Creating a BeautifulSoup object and specifying the parser 
soup = bs4(index, 'lxml') 

# can go in iterating for loop: takes only the PARENTS of the <a href> tags for EITHER Ranked athletes or Heat athletes
#### NOTE FOR LIYA: NEED TO LOOK AT CSS selectors FOR THE class SHIT.
def get_medal(ptag):  # returns a string
    medal_pos = "N/A"
    
    # IN THE REAL THING, FOR SOME REASON, IT'S contents[8]
    curr = ptag.parent.contents[17].find('span')

    if not isinstance(curr, type(None)):
        # print("MEDAL: ", curr.string)
        # print("MEDAL TYPE: ", type(curr))
        medal_pos = curr.string

    # print(medal_pos)
    return medal_pos

    # print("PARENT TAG OF PTAG: ", ptag.parent)
	# print("PARENT TAG OF PTAG, contents[0]: ", ptag.parent.contents[0])
	# print("PARENT TAG OF PTAG, contents[8]: ", ptag.parent.contents[8])
	# print("SPAN TAG: ", ptag.parent.contents[8].find('span'))
	# print("SPAN TAG STRING: ", ptag.parent.contents[8].find('span').string)


    # if bool(ptag.find_next_sibling("span")):
    #     # FOUND SPAN SIBLING!
    #     # get the next sibling with attribute "span"
    #     print("MEDAL: ", ptag.find_next_sibling("span").string)
    #     medal_pos = ptag.find_next_sibling("span").string

    # return medal_pos

    # for sib in tag.next_siblings.find_all("span", class_="label") and tag.previous_siblings.find_all("span", class_="label"):
    #     if sib.find('class'):
    #         # if contents of class are "gold|silver|bronze" && flag 1
    #             # return gold|silver|bronze string
    #         # if contents of class are NOT "gold|silver|bronze"
    #             # flag 0, return False.
    #             f0_is_not_heat = False
    #         ()
    #     elif :
        
    # return f0_is_not_heat if flag == 0 else f1_medal_pos

        
    # could be elif for more flags


def is_ranked_athlete(tag):
    athl_url = re.compile("/athletes/\d{5,6}")
    if not isinstance(tag.get("href"), str): 
        # print("\n\nIRA, IF NOT A STRING")
        return None
    else:
        
            # SET FINAL BOOL TO TRUE IF NOT HEAT???

        # match_found = bool(athl_url.match(tag.get("href")))
        # if match_found:
            # print("\n\nMATCH FOUND: TRUE")
            # print("TAG!!!!: ", tag)
            # print("TAG PARENT: ", (tag.parent), "<-- should be right here...")
            # print("PARENT el type: ", type(tag.parent))
            # # print("PARENT el size: ", len(str(tag.parent)))
            # # print("TESTING 2ND CONDITION: ", isinstance(tag.parent, type(None)))
            # print("PARENT HAS 'style'?: ", tag.parent.has_attr('style'))
            # print("TESTING 2ND CONDITION: ", not tag.parent.has_attr('style'))
            # print("PARENT.name: ", tag.parent.name)
            # print("PARENT.name: ", type(tag.parent.name))
            # print("TESTING 3RD CONDITION: ", tag.parent.name != 'p')
        return bool(athl_url.match(tag.get("href"))) and not tag.parent.has_attr("style") and tag.parent.name != 'p'
        # and is_not_heat(tag.parent, 0)
        # and isinstance(tag.parent, type(None))
        
    
##### SCRAPS
    # return (isinstance(tag.previous_sibling, class_ = "bib")
    #         and isinstance(tag, href=re.compile("/athletes/\d{5,6}")))
    # return bool(athl_url.match(tag.get("href"))) and len(str(tag.previous_element)) == 1 and tag.previous_element.name == 'td'#tag.get("href") == re.compile("/athletes/\d{5,6}")) and tag.previous_sibling.has_attr('class')
    # return bool(athl_url.match(tag.get("href")))# and tag.previous_sibling.has_attr('class')#tag.get("href") == re.compile("/athletes/\d{5,6}")) and tag.previous_sibling.has_attr('class')
    

# for tag in soup.find_all(href=re.compile("/athletes/\d{5,6}")):
set = []

if isinstance(soup.find("h2"), type(None)):
    set = soup.find_all(is_ranked_athlete)
else:
    stop_at = soup.find("h2")
    set = stop_at.find_all_previous(is_ranked_athlete)

# stop_at = soup if isinstance(soup.find("h2"), type(None)) else soup.find("h2")

for tag in set:
    # NEED TO STORE THESE TWO SOMEHOW
    print(tag.string, ": ", get_medal(tag.parent))
    # print("\n############RUNNING FIND_ALL############")
    # print(tag.get("href"))
    # print()

# print("Number of athletes: ", len(set))
