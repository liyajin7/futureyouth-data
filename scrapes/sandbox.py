from bs4 import BeautifulSoup as bs4
import requests
 
target_website = 'https://achievement.org/achiever/dame-kiri-te-kanawa/#profile'
 
request_headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
 
# Initiate HTTP request, get soup
response = requests.get(target_website, headers=request_headers)
html = response.content
int_soup = bs4(html, 'lxml')


#### for https://achievement.org/achiever/dame-kiri-te-kanawa/
# TBD: could clean up <p> tags




#### FOR https://achievement.org/achiever/dame-kiri-te-kanawa/#interview
# TBD: could clearly label each speaker, remove <figure> tags

# Gets all interview divs
# first_tag = int_soup.find("article", "editorial-article col-md-8")
# interview_divs = first_tag.find_all_next(
#     class_=lambda x : x in ['achiever__interview-copy', 'achiever__interview-video__copy']
# )
# # txt_interview_divs = first_tag.find_all_next(class_='achiever__interview-copy')
# # vid_interview_divs = first_tag.find_all_next(class_='achiever__interview-video__copy')

# interview = ''
# # vid_interview = ''
# for d in interview_divs:
#     print(d)
#     interview = interview + '\n' + str(d)
    # vid_interview = vid_interview + ' ' + str(d)




first_tag = int_soup.find("article", "col-md-8 editorial-article clearfix")
prof_ps = first_tag.find_all('p')

profile = ''
for d in prof_ps:
    print(d)
    # interview = interview + '\n' + str(d)