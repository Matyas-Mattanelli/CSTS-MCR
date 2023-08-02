import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import numpy as np
import pickle
import re

#Get all occurences of 'mistrovství' and the associated results
res = {}
for year in range(2001, datetime.datetime.now().year + 1):
    res_year = {}
    for month in range(1, 13):
        req = requests.get(f'https://www.csts.cz/cs/VysledkySoutezi/Souteze?rok={year}&mesic={month}')
        if req.status_code == 200:
            soup = BeautifulSoup(req.content)
        else:
            print(f'Request unsuccessful. Status code: {req.status_code}. Year: {year}. Month: {month}')
            continue
        div = soup.find('div', {'id' : 'content'}) #Get the div containing the relevant data
        divs = div.find_all('div', recursive = False) #Get the divs with the individual competitions
        for j in range(1, len(divs)): #Loop through the competitions
            title = divs[j].find_all('div')[1].text #Save the title
            if ('mistrovství' in title.lower()) | ('mistovství' in title.lower()): #Check if it is a 'Mistrovství' (or a 'mistovství' to account for the typo in 2003)
                ass = divs[j].find_all('a') #If so, save all elements containing the links
                res_year[title] = [tuple([i.text, f'https://www.csts.cz{i["href"]}']) for i in ass] #Save all the links
    res[year] = res_year

#Filter only relevant results
def check_mcr(x):
    """
    Function checking whether a string is a valid title for MČR
    """
    mask = [i in x.lower() for i in ['prahy', 'krkonoš', 'družstev', 'družstva', 'formací', 'otevřené', 'čech', 'kraje', 'moravy', 'brna', 'regionu', 'festival', 'style', 'showdance', 'formace', 'sokolova']]
    return not any(mask)

#Apply the function
res_filt = {}
for i in res:
    year_dict = {}
    for j in res[i]:
        if check_mcr(j):
            year_dict[j] = res[i][j]
    res_filt[i] = year_dict

#Check how many results are available for each year
for i in res_filt:
    print(f'{i}: {len(res_filt[i])}')

#Create a database with the links
all_links = []
for i in res_filt: #Loop through the years
    for j in res_filt[i]: #Loop through the competitions
        for k in res_filt[i][j]: #Loop through the categories within each competition
            all_links.append([i, *k]) #Append a list with the given year, category and link
all_links_df = pd.DataFrame(all_links, columns = ['Year', 'Category', 'Link']) #Convert the results into a data frame     

#Define a function for separating age group and category
def sep_cat(x):
    """
    Function extracting the age group and category from a string
    """
    rev = False #Do not reverse on default
    if 'MČR-' in x:
        x = x.replace('MČR-', '') #Strip irrelevant info (for later years)
        if ('10T' in x) & (x[-3:] != '10T'): #Handling special cases
            rev = True
    splitted = x.split('-')
    if len(splitted) > 2:
        if rev:
            splitted = [splitted[0], '-'.join(splitted[1:])]
        else:
            splitted = ['-'.join(splitted[:-1]), splitted[-1]]
    if rev:
        return splitted[::-1]
    else:
        return splitted
    
#Separate age group and category
cat_map = {'Junioři-I' : 'Jun-I', 'Junioři-II' : 'Jun-II', 'Hlavní' : 'Dospělí', 'Profesional' : 'Profi', '21' : 'Do 21let', 'U21' : 'Do 21let'} #Dictionary for category unification
all_links_df['Age group'] = all_links_df['Category'].apply(lambda x: sep_cat(x)[0]).replace(cat_map)
all_links_df['Category'] = all_links_df['Category'].apply(lambda x: sep_cat(x)[1]).replace({'10 tanců' : '10T'})

#Reorder the columns
all_links_df = all_links_df.loc[:, ['Year', 'Age group', 'Category', 'Link']]

#Export the results
all_links_df.to_excel('MČR links.xlsx', index = False)

#Get results for all links (1min22s)
all_results = []
for link in all_links_df['Link']:
    table = pd.read_html(link, encoding = 'utf-8')[0] #Scrape the table
    mask = np.invert(table.iloc[:, 0].isin(['Finále', 'Semifinále', 'Re-dance'] + [f'{i}. kolo' for i in range(1, 6)])) #Identify invalid rows separating rounds
    table = table.loc[mask, table.columns[[0, 2, 3]]] #Remove invalid rows and columns
    table.columns = ['Umístění', 'Pár', 'Klub'] #Rename the columns
    table['Partner'] = table['Pár'].apply(lambda x: x.split(' & ')[0]) #Extract the male partner
    table['Partnerka'] = table['Pár'].apply(lambda x: x.split(' & ')[1]) #Extract the female partner
    table['Klub'] = table['Klub'].str.replace(' \(.*\)$', '', regex = True) #Remove country from club
    table.drop('Pár', axis = 1, inplace=True) #Drop column with the whole pair
    table = table.loc[:, ['Umístění', 'Partner', 'Partnerka', 'Klub']] #Rearange columns
    all_results.append(table) #Append the table to the results

#Export results 
with open('mcr_results.pkl', 'wb') as out:
    pickle.dump(all_results, out)

#Find all people that ever participated
particips = set(all_results[0]['Partner'].to_list() + all_results[0]['Partnerka'].to_list())
for val in all_results[1:]:
    particips = particips | set(val['Partner'].to_list() + val['Partnerka'].to_list())
particips = set([re.sub('\.|_', ' ', i) for i in particips]) #Unify names

#Create a final data set
cols = (all_links_df['Year'].astype(str) + ' ' + all_links_df['Age group'] + ' ' + all_links_df['Category']).values
final_df = pd.DataFrame(columns = cols, index = list(particips))

#Fill in the data set
for idx, val in enumerate(all_results):
    final_df.loc[val['Partner'].str.replace('\.|_', ' ', regex = True).values, cols[idx]] = val['Umístění'].values
    final_df.loc[val['Partnerka'].str.replace('\.|_', ' ', regex = True).values, cols[idx]] = val['Umístění'].values

#Export the final data set
final_df.to_excel('MČR results.xlsx', index = True, index_label = 'Osoba')
final_df.to_csv('MČR results.csv', index = True, index_label = 'Osoba')