# from bs4 import BeautifulSoup as bs4
# import requests

# response = requests.get("https://achievement.org/achiever/maya-lin/")
# html = response.content

# soup = bs4(html, 'lxml')

# with open('achievement-pp.txt', 'w') as f:
#     f.write(soup.prettify())


from bs4 import BeautifulSoup as bs4
import requests
 
target_website = 'https://www.bbc.co.uk/history/historic_figures/a.shtml'
 
request_headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
 
# Initiate HTTP request
response = requests.get(target_website, headers=request_headers)
html = response.content
soup = bs4(html, 'lxml')

# Resolve HTTP response
if response.status_code == 200:
    # View request user agent
    with open('britannica/pp_brit_main.txt', 'w') as f:
        f.write(soup.prettify())
    # print(response.request.headers['user-agent'], '\nYAY IT WORKED!')
else:
    print(response, '\nFAILURE.')