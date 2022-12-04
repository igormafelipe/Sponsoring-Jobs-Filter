# !/usr/bin/env python3
# Given a excell format file, fetch all company names

import pandas as pd
import search_params as sp
import re

# Given a list of company names, turn them all to lower case, remove all special
# characters, and swap spaces for dashes (-)
def normalize_strings(strs: list[str]):
    normalized = []
    for s in strs:
        if type(s) != str or not s[0].isalpha():
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

def get_company_names():
    companies_data = pd.read_excel(sp.INPUT_FILE_PATH)
    position_regex = "|".join(sp.POSITION_KEYWORDS)
    if sp.FILTER_COL_LABEL != None:
        related_companies = companies_data.loc[companies_data[sp.FILTER_COL_LABEL].str.contains(position_regex, na=False, regex=True)]
    else:
        related_companies = companies_data
            
    companies_list: list = related_companies[sp.COMPANY_COL_LABEL].to_list()
    companies_list = normalize_strings(companies_list)
    companies_list = remove_duplicates(companies_list)
    possible_companies: dict = get_possible_comapany_keywords(companies_list)
    
    return possible_companies