import sys
import re

for line in sys.stdin:
    # filter out dates, post type only questions (not answers)
    if ((re.search('^  <row Id=.*CreationDate="2023-05-27', line) or re.search('^  <row Id=.*CreationDate="2023-05-28', line) or re.search('^  <row Id=.*CreationDate="2023-05-29', line) or re.search('^  <row Id=.*CreationDate="2023-05-30', line) or re.search('^  <row Id=.*CreationDate="2023-05-31', line) or re.search('^  <row Id=.*CreationDate="2023-06', line) or re.search('^  <row Id=.*CreationDate="2023-07', line) or re.search('^  <row Id=.*CreationDate="2023-08', line) or re.search('^  <row Id=.*CreationDate="2023-09', line) or re.search('^  <row Id=.*CreationDate="2023-10', line)) 
        and re.search('^  <row Id=.*PostTypeId="1"', line)):
        print(f'{line}')
print("Done")

# run using or command below: cat txt1.txt | python3 scrapeSO.py > so.txt
# or use: 7z e -so stackoverflow.com-Posts.7z | python3 scrape.py > so.txt

# useful for viewing data
# 7z e -so stackoverflow.com-Posts.7z |head -10000 > txt1.txt
# 7z e -so stackoverflow.com-Posts.7z |more
# need to brew install p7zip

#so.txt is filtered dates and post type