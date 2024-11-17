import json

ach_url = "https://something.com"

json_list = []

j1 = {
    ach_url:
    {
        "name": 'name',
        "biography": "ach_bio",
        "interview": "ach_interview",
        "html": "ach_int_response.content",
        "person_overview": "ach_profile" # bio of the person?
    }
}

json_list.append(j1)

j2 = {
    ach_url:
    {
        "name": 'name2',
        "biography": "ach_bio2",
        "interview": "ach_interview2",
        "html": "ach_int_response.content2",
        "person_overview": "ach_profile2" # bio of the person?
    }
}

json_list.append(j2)

with open('test.json', 'w') as f:     
    json.dump(json_list, f)