# !/usr/bin/env python3
# File controlling the parameters used in the search

############################################################
################ FILTERING VARIABLES #######################
############################################################

# FILE PATH OF EXCELL FORMAT FILE WITH PERMITTED COMPANIES FROM COUNTRY
INPUT_FILE_PATH = "/Users/Igor/Desktop/company_filter/companies_list.xlsx"

# LABEL OF THE COL THAT CONTAINS THE ROLE OF THE JOBS
FILTER_COL_LABEL = 'Occupation'

# LABEL OF THE COL THAT CONTAINS THE COMPANY NAMES
COMPANY_COL_LABEL = 'Employer'

# KEYWORDS TO LOOK FOR POSITION. THE MORE, THE BETTER
POSITION_KEYWORDS = ["Software Engineering", "Software", "Programmer", "Developer"]

# Range of experience for position, in years. 
# Ex: (0, 3) = 0 to 3 years of experience. Excludes anything 3+ years
EXPERIENCE_RANGE = (0, 3)

# Which seniority roles would you like to exclude?
# For roles with level such as Developer III, type only the level (III)
SENIORITY_EXCLUDE = ["Senior", "Staff", "Lead", "III"]

#####################################################
################ FILE CONTROL #######################
#####################################################

OUTPUT_FILE_NAME = "filtered_sheet"