from bs4 import BeautifulSoup as bs4
import requests, re, json
 

request_headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
 
# Initiate HTTP request, get soup
target_website = 'https://www.bbc.co.uk/history/historic_figures/a.shtml'
response = requests.get(target_website, headers=request_headers)
soup = bs4(response.content, 'lxml')

# Resolve HTTP response
if response.status_code == 200:
    # View request user agent
    print('\nHTTP response success, 200.')
else:
    print(response, '\nHTTP response failed')

json_list = []

all_pages = soup.find_all('a', href=re.compile(r"/history/historic_figures/[a-zA-Z]\.shtml"))
[print(p.get('href')) for p in all_pages]

## Loops over all pages
for page in all_pages:
    ltr_page_url = 'https://www.bbc.co.uk/' + page.get('href')
    ltr_page_response = requests.get(ltr_page_url, headers=request_headers)
    ltr_page_soup = bs4(ltr_page_response.content, 'lxml')

    # Get list of people
    first_tag = ltr_page_soup.find("div", "a_z_content")
    #### LIYA LEFT OFF HERE
    all_people = first_tag.find_all_next('a', href=re.compile(r"/history/historic_figures/[a-zA-Z_]+\.shtml"))

    for psn in all_people:


    ach_name = t.string
    ach_url = 'https://achievement.org' + t.get('href')

    print('\n\n', ach_name, '\n', ach_url)