#!/usr/bin/env python3

import pandas as pd
import os
from tqdm import tqdm
import careerjet_api_client
import search_params as sp
from get_company_names import get_company_names

# information to be fetched from each job post
# >> DO NOT CHANGE << 
FETCH_KEYS = ["locations", "date", "title", "company", "url"]

# Controls max range of exclusion of experience. If a position requests more than
# EXPERIENCE_EXCLUSION years of experience, it will not be filtred out regardless
# of range.
EXPERIENCE_EXCLUSION = 15

def output_excel(pd: object):
    out_file = sp.OUTPUT_FILE_NAME + ".xlsx"
    if os.path.exists(out_file):
        os.remove(out_file)
    pd.to_excel(out_file)

def get_experiences():
    min_exp, max_exp = sp.EXPERIENCE_RANGE
    less_than_min = [str(x) + " years" for x in range(0, min_exp)]
    more_than_max = [str(x) + " years" for x in range(max_exp + 1, EXPERIENCE_EXCLUSION)]
    more_than_max_p = [str(x) + "+ years" for x in range(max_exp + 1, EXPERIENCE_EXCLUSION)]
    return less_than_min + more_than_max + more_than_max_p

def fetch_positions(companies: dict, position: str):
    all_jobs = {}
    positions = set(sp.POSITION_KEYWORDS)
    experience = get_experiences()
    used = set()
    cja = careerjet_api_client.CareerjetAPIClient(sp.LOCATION);
    for company in tqdm(companies):
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
                if (job_key in used or
                    job['company'] == "" or
                    any([x in job['description'] for x in experience]) or
                    any([y.lower() in job['title'].lower() for y in sp.SENIORITY_EXCLUDE])):
                    continue
                
                if (any(job['company'].lower() in x for x in companies) and 
                    any([x in job['title'] for x in positions]) and
                    not any ([y in job['title'] for y in sp.SENIORITY_EXCLUDE])):
                    
                    for key in FETCH_KEYS:
                        if key not in all_jobs:
                            all_jobs[key] = []
                        all_jobs[key].append(job[key])
                    used.add(job_key)

    return all_jobs


def filter():
    print(f"Keywords: {', '.join(sp.POSITION_KEYWORDS)}")
    print(f"Excluded Seniorities: {', '.join(sp.SENIORITY_EXCLUDE)}")
    try:
        possible_companies: dict = get_company_names()
        jobs = fetch_positions(possible_companies, "Software Engineer")
        output_excel(pd.DataFrame.from_dict(jobs))
        print(f"Successfully outputed to {sp.OUTPUT_FILE_NAME}.xlsx")
    except Exception as e:
        print(f"Whoops, something went wrong\n{e}\nAborting...")