from bs4 import BeautifulSoup as bs4
import requests, re, json
 
target_website = 'https://achievement.org/achiever/'
 
request_headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
 
# Initiate HTTP request, get soup
response = requests.get(target_website, headers=request_headers)
html = response.content
soup = bs4(html, 'lxml')

# Resolve HTTP response
if response.status_code == 200:
    # View request user agent
    print('\nHTTP response success, 200.')
else:
    print(response, '\nHTTP response failed')

json_list = []
all_people = soup.find_all("a", "text-brand-primary achiever-list__name")

# Loops over all achievers on page
for t in all_people:
    
    # if test_counter == 1: break
    
    ach_name = t.string
    ach_url = 'https://achievement.org' + t.get('href')

    print('\n\n', ach_name, '\n', ach_url)


    ## Soup for achiever mainpage
    # TBD @Liya: could clean up <p> tags
    ach_response = requests.get(ach_url, headers=request_headers)
    ach_soup = bs4(ach_response.content, 'lxml')
    
    # Bio info from achiever mainpage
    first_tag_kids = ach_soup.find("article", "editorial-article col-md-8").children

    # Converts to string
    ach_bio = ''
    for kid in first_tag_kids:
        if kid.name == 'p': ach_bio = ach_bio + ' ' + str(kid)
    # print(ach_bio)


    ## Soup for achiever interview
    # TBD @Liya: could clearly label each speaker, remove <figure> tags
    ach_int_url = ach_url + '#interview'
    ach_int_response = requests.get(ach_int_url, headers=request_headers)
    ach_int_soup = bs4(ach_int_response.content, 'lxml')

    # Gets all interview tags
    first_tag = ach_int_soup.find("article", "editorial-article col-md-8")
    interview_divs = first_tag.find_all_next(
        class_=lambda x : x in ['achiever__interview-copy', 'achiever__interview-video__copy']
    ) # txt_interview_divs = first_tag.find_all_next(class_='achiever__interview-copy')

    # Convert to string
    ach_interview = ''
    for d in interview_divs:
        # print(d)
        ach_interview = ach_interview + '\n' + str(d)


    ## Soup for achiever profile
    ach_prof_url = ach_url + '#profile'
    ach_prof_response = requests.get(ach_prof_url, headers=request_headers)
    ach_prof_soup = bs4(ach_prof_response.content, 'lxml')

    first_tag = ach_prof_soup.find("article", "col-md-8 editorial-article clearfix")
    prof_ps = first_tag.find_all('p')

    # Convert to string
    ach_profile = ''
    for d in prof_ps:
        # print(d)
        ach_profile = ach_profile + ' ' + str(d)

    ach_html = str(ach_int_response.content)
    # aligned Joel's current code: title, article_summary, html
    ach_json = {
        ach_url:
        {
            "name": ach_name,
            "biography": ach_bio,
            "person_overview": ach_profile, # bio of the person?
            "interview": ach_interview
            # "interview_html": ach_html # interview HTML
        }
    }

    json_list.append(ach_json)

    # test_counter += 1


with open('achievement_transcript_no-html.json', 'w') as f:     
    # print("\n\n\nRUNNING JSON DUMP:")
    # print(json_list)
    # print(type(json_list))
    json.dump(json_list, f)


# <a class="text-brand-primary achiever-list__name" href="/achiever/kareem-abdul-jabbar/">
