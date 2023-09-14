import pandas as pd
import pickle
import numpy as np

#Load the results
with open('mcr_results.pkl', 'rb') as handle:
    mcr_res = pickle.load(handle)

#Get the first six rows of each competition
mcr_club_sum = pd.DataFrame(columns = ['Umístění', 'Klub']) #Initiate an empty data frame for the summary
for comp in mcr_res: #Loop through all competitions
    mcr_club_sum = pd.concat([mcr_club_sum, comp.loc[:6, ['Umístění', 'Klub']]]) #Add the first six rows of the current competition to the summary

#Adjust the summary
mcr_club_sum = mcr_club_sum.loc[mcr_club_sum['Umístění'].isin(list(range(1, 7)) + [str(i) for i in range(1, 7)]), :] #Filter out ranks 7 and lower
mcr_club_sum['Umístění'] = mcr_club_sum['Umístění'].astype(int) #Convert ranks to integers since some of them are strings

#Get the counts of club/rank combinations
mcr_club_sum['Comb'] = mcr_club_sum['Umístění'].astype(str) + '*' + mcr_club_sum['Klub'] #Concatenate club and rank
mcr_club_sum_final = mcr_club_sum['Comb'].value_counts().reset_index(drop = False) #Count the unique occurences

#Get the final summary
mcr_club_sum_final[['Rank', 'Club']] = mcr_club_sum_final['Comb'].str.split('*', expand = True) #Split to club and rank back again
mcr_club_sum_final.drop('Comb', axis = 1, inplace = True) #Drop the auxiliary column
mcr_club_sum_final.rename(columns = {'count' : 'Count'}, inplace = True) #Rename the count column for aesthetic purposes
mcr_club_sum_final = mcr_club_sum_final.pivot(index = 'Club', columns = 'Rank', values = 'Count') #Convert from long to wide format
mcr_club_sum_final.sort_values([str(i) for i in range(1, 7)], ascending = False, inplace = True) #Sort

#Export the final summary
mcr_club_sum_final.to_excel('MCR_summary.xlsx', index = True)