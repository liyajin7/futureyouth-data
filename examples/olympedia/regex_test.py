import re

ls = ['123','12345', '1234567', '7654321', '3819', '1839']


# for all *event* URLs on [YEAR] Game Results page
str_event = '/results/9000630'
match_event = re.search(r'/results/\d{6,7}', str_event)

# for the 1 *sport* URL on Event Results page
str_sport = '/editions/60/sports/ALP'
match_sport = re.search(r'/editions/\d{2}/sports/\w{3}', str_sport)
# /editions/60/sports/NCB
# /editions/60/sports/ALP

# for all *athlete* URLs on Event Results page
str_athl = '/athletes/110097'
match_athl = re.search(r'/athletes/\d{5,6}', str_athl)

# If-statement after search() tests if it succeeded
if match_athl:
  print('found', match_athl.group()) ## 'found word:cat'
else:
  print('did not find')
