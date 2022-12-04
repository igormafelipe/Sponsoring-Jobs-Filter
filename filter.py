#!/usr/bin/env python3

import pandas as pd
import os, re
import careerjet_api_client

#Which positions you want to check for
OCCUPATIONS = ["2171-Computer analysts and consultants", 
               "2175-Web Designers and Developers",
               "2173-Software engineers and designers"]

FILTER_ROW_LABEL = ' Occupation'
COMPANY_COL_LABEL = 'Employer'

INPUT_FILE_PATH = "/Users/Igor/Desktop/company_filter/companies_list.xlsx"
OUTPUT_FILE = "filtered_sheet.xlsx"

BASE_URL = "https://www.linkedin.com/company/"

def output_excel(pd: object):
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)
    pd.to_excel(OUTPUT_FILE)

# Given a list of company names, turn them all to lower case, remove all special
# characters, and swap spaces for dashes (-)
def normalize_strings(strs: list[str]):
    normalized = []
    for s in strs:
        if not s[0].isalpha():
            continue
        
        s = s.lower()
        
        #removing all special characters besides space
        s = re.sub(r"[^a-zA-Z0-9]+", ' ', s)
        
        s = s.strip()

        normalized.append(s)
    
    return normalized

#Given a list of strs, removes all duplicate entries
def remove_duplicates(strs: list[str]):
    unique = []
    for s in strs:
        if s in unique:
            continue
        unique.append(s)
            
    return unique
  

# Given a list of strs, populate a dictionary where keys are the str, and values
# are all permutations of the words separated by "-" in that string. Ex:
# "ubisoft-entertainment-inc" -> ["ubisoft", "ubisoft-entertainment", "ubisoft-entertainment-inc"]
def get_possible_comapany_keywords(strs: list[str]):
    possible_urls = {}
    for s in strs:
        if s not in possible_urls:
            possible_urls[s] = []
        
        words = s.split(" ")
        curr_url = ""
        for i in range(min(2, len(words))):
            curr_url = words[i] if curr_url == "" else curr_url + " " + words[i]
            possible_urls[s].append(curr_url)

    return possible_urls

companies_data = pd.read_excel(INPUT_FILE_PATH)

#Filtering based on OCCUPATIONS
swe_related_companies = companies_data.loc[companies_data[FILTER_ROW_LABEL].isin(OCCUPATIONS)]
    
companies_list: list = swe_related_companies[COMPANY_COL_LABEL].to_list()
companies_list = normalize_strings(companies_list)
companies_list = remove_duplicates(companies_list)

# Get a list of possible Linkedin URLS based on company names.
possible_companies: dict = get_possible_comapany_keywords(companies_list)

#Getting job infos from CareerJet
cja  =  careerjet_api_client.CareerjetAPIClient("en_CA");

def fetch_positions(companies: dict, position: str):
    all_jobs = {}
    keys = ["locations", "date", "title", "company", "url"]
    positions = set(["Software", "Programmer", "Developer"])
    experience_a = [str(x) + " years" for x in range(3, 11)]
    experience_b = [str(x) + "+ years" for x in range(3, 11)]
    experience = experience_a + experience_b
    used = set()
    for company in companies:
        for company_possible_name in companies[company]:
            result_json = cja.search({
                            'keywords'    : position + " " + company_possible_name,
                            'affid'       : '069f8b7ca985d7c45f58ba3cfdf773da',
                            'user_ip'     : '130.64.225.4',
                            'url'         : 'https://igormafelipe.github.io/igormfe/',
                            'user_agent'  : 'Chrome'
                        });

            if 'jobs' not in result_json:
                continue
            
            for job in result_json['jobs']:
                job_key = job['title'] + job['date'] + job['company']
                if job_key in used:
                    continue
                
                if any(x in job['description'] for x in experience):
                    continue
                
                if (any(job['company'].lower() in x for x in companies) and 
                    any([x in job['title'] for x in positions])):
                    for key in keys:
                        if key not in all_jobs:
                            all_jobs[key] = []
                        
                        all_jobs[key].append(job[key])
                    
                    used.add(job_key)
        
    return all_jobs

jobs = fetch_positions(possible_companies, "Software Engineer")

companies_fetched = set([])
for c in jobs["company"]:
    companies_fetched.add(c.lower())     

output_excel(pd.DataFrame.from_dict(jobs))