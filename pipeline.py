import requests
import json
from openai import OpenAI

# defining endpoint
OPENAI_API_KEY = "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"
API_URL = "https://api.openai.com/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {OPENAI_API_KEY}",
}

# function to get inflection points from bio

# ach_url:
# {
#     "name": ach_name,
#     "biography": ach_bio,
#     "interview": ach_interview,
#     "person_overview": ach_profile, # bio of the person?
#     "html": ach_html # interview HTML
# }
def get_inflections(url, person_name, person_overview, bio_data, interview_data):
    # request payload
    request_body = {
        "model": "gpt-4o-mini",
        "messages":
        [
            {
                "role": "system",
                "content": #"return some text, and a JSON object! end your output with a cute texticon emoji"
                    f"""
                    you will be analyzing a provided biography for {person_name} and an interview transcript with
                    {person_name}, originally from {url}, to extract significant inflection points from their life.

                    by inflection points, i mean:
                    - significant turning points in life caused by external/world events
                    - significant turning points in life caused by personal decision
                    - significant turning points in life caused by other reasons
                    - significant low points in life
                    - significant challenges in life
                    
                    you should return a JSON object of {person_name}'s major life inflection points, based on the information in their biography and interview transcript. each single inflection point should have the following JSON format:
                    
                    {{
                        {person_name}:                      // change all instances of "{person_name}" to be the value {person_name}
                        {{
                            "inflection_id:" 0,              // change this number to a single integer ID, unique for each person's inflection point. start from 0 and increment by 1.
                            "inflection_label:" str,         // a 1-4 word string describing the inflection point. create the label based on the summary of the specific inflection point.
                            "person_age": 0,                 // change this number to the age of the person during the inflection point
                            "inflection_summary": str,       // a detailed summary of the specific inflection point, at least 3-5 sentences
                            "inflection_quotes": list[str],   // a list of strings of direct, relevant quotes from the interview transcript that directly address the information in the inflection_summary. these quotes must be takend directly from the text below "and here is the interview transcript:" below, and must be relevant to the inflection point. the quotes can be anywhere from 1-5 sentences long and you should not cut off any sentences.
                            "year": 0,                       // change this number to the year this inflection point would have taken place. make sure this is accurate based on the person's birth year and age
                            "historical_events": list[str]   // a list of strings of relevant national/global historical events that took place that year which reasonably could have affected the person's experience at this inflection point.
                        }},
                        {{
                            "inflection_id:" 1,              // same details as above
                            "inflection_label:" str,          
                            "person_age": 0,                  
                            "inflection_summary": str,        
                            "inflection_quotes": list[str]
                            "year": 0,                      
                            "historical_events": list[str]  
                            
                        }}
                        // continue for as many significant inflection points you can identify.
                    }}

                    the inflection points should be in chronological order and non-overlapping.

                    analyze the following overview, biography, and interview transcript for {person_name} in order to populate the information in the JSON.

                    here is the overview:
                    \"
                    {person_overview}
                    \"

                    here is the biography:
                    \"
                    {bio_data}
                    \"

                    and here is the interview transcript:
                    \"
                    {interview_data}
                    \"

                    return a string. do not include "```json" at the beginning of the response, and do not include "```" at the end.

                    """
                
            }
        ],
        "temperature": 0.7,
        "max_tokens": 2048
    }

    # send API request
    response = requests.post(API_URL, headers=headers, json=request_body)
    print("RESPONSE SUCCESSFULLY SENT")
    response.raise_for_status() # Raise an error if the request fails
    # print("in-func response type: ", type(response))
    return response.json()


with open('scrapes/achievement-org/achievement_transcript_no-html.json', 'r') as file:
    dataset = json.load(file)

# ach_url = 'https://achievement.org/achiever/wole-soyinka/'
# ach_url2 = 'https://goog.com'
# dataset = [
#     {
#         ach_url:
#         {
#             "name": 'Soyinka Whatever',
#             "biography": 'bio bio bio biob io',
#             "person_overview": 'profile profile profile profile', # bio of the person?
#             "interview": 'interview interview interview interview interview '
#             # "interview_html": ach_html # interview HTML
#         }
#     },
#     {
#         ach_url2:
#         {
#             "name": 'Second Person',
#             "biography": 'bio bio bio biob io',
#             "person_overview": 'profile profile profile profile', # bio of the person?
#             "interview": 'interview interview interview interview interview '
#             # "interview_html": ach_html # interview HTML
#         }
#     }
# ]

# dataset = json.dumps(set_dataset, indent=4)
# print("dataset type: ", type(dataset))
# print("dataset: ", dataset)

 # insert JSON processing here

### dataset schema
# "name": ach_name,
# "biography": ach_bio,
# "person_overview": ach_profile, # bio of the person?
# "interview": ach_interview,
# "interview_html": ach_html # interview HTML

results = []
for person in dataset:
    for scrape_url, scrape_data in person.items():
        person_name = scrape_data["name"]
        person_overview = scrape_data["person_overview"]
        bio_data = scrape_data["biography"]
        interview_data = scrape_data["interview"]
        # print("\n\nFOR LOOP DATASET: ", scrape_url, "\n", person_name, "\n", person_overview, "\n", bio_data, "\n", interview_data)

        response = get_inflections(scrape_url, person_name, person_overview, bio_data, interview_data)['choices'][0]['message']['content'] #.choices[0].message.content #.choices[0].message.content()
        # print("\n\nresponse content: ", response)
        # print("\n\nresponse type: ", type(response))
        response_json = json.loads(response)
        # print("\n\nresponse type jsonified: ", type(response_json))

        results.append(response_json)
        print("ran inflections for ", person_name)


    # need to figure out output data formation
    # person_results[]

# print("\n\nresults:", results)
# print("results type:", type(results))

with open("achievement_inflections.json", "w") as file:
    json.dump(results, file)

### testing OpenAI endpoint
# client = OpenAI(api_key=OPENAI_API_KEY)

# response = client.chat.completions.create(
#     messages=[{
#         "role": "user",
#         "content": "Say this is a test",
#     }],
#     model="gpt-4o-mini"
# )

# print(response.choices[0].message.content) # where response is the JSON from the API response (see docs!)


# # function to analyze user input
# def analyze_dataset()