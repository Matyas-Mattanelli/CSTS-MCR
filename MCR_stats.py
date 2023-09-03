import customtkinter as ctk
from CTkTable import CTkTable
import pandas as pd
import re
import pickle
import numpy as np

class Window:

    def __init__(self):
        #Initiate window
        self.root = ctk.CTk()
        self.root.title('ČSTS MČR database')
        self.center_window(500, 250, self.root)
        self.root.wm_iconbitmap('cstslogo.ico')

        #Create a label
        label = ctk.CTkLabel(self.root, text = 'Are you looking for a person or for a competition?', justify = 'center', wraplength = 400)
        label.grid(row = 0, column = 0, padx = 20, pady = 20)

        #Create a grid for the buttons
        buttframe = ctk.CTkFrame(self.root, fg_color = self.root.cget('fg_color'))
        buttframe.columnconfigure(0, weight = 1)
        buttframe.columnconfigure(1, weight = 1)

        #Button for person search
        butt1 = ctk.CTkButton(buttframe, text = 'Person', command = self.person_window)
        butt1.grid(row = 0, column = 0, padx = 20, pady = 20)

        #Button for competition search
        butt2 = ctk.CTkButton(buttframe, text = 'Competition', command = self.comp_window)
        butt2.grid(row = 0, column = 1, padx = 20, pady = 20)

        #Put frame into the window
        buttframe.grid(row = 1, column = 0, padx = 20, pady = 20)

        #Add a button for canceling the window
        butt_cancel = ctk.CTkButton(self.root, text = 'Cancel', command = self.root.destroy)
        butt_cancel.grid(row = 2, column = 0, padx = 20)

        #Center everything
        self.root.grid_columnconfigure(0, weight = 1)

        self.root.mainloop()

    def person_window(self):
        """
        Function getting a name of the person from the user
        """
        #Create a window
        self.person_root = ctk.CTkToplevel(self.root)
        self.center_window(500, 250, self.person_root)
        self.person_root.title('ČSTS MČR database')
        self.person_root.after(250, lambda: self.person_root.iconbitmap('cstslogo.ico'))

        #Add a label
        label = ctk.CTkLabel(self.person_root, text = 'Please specify the name of the dancer', justify = 'center', wraplength = 400)
        label.grid(row = 0, column = 0, padx = 20, pady = 20)

        #Add a textbox
        self.person_textbox = ctk.CTkEntry(self.person_root, justify = 'center', width = 300)
        self.person_textbox.grid(row = 1, column = 0, padx = 20, pady = 20)

        #Create a grid for the buttons
        buttframe = ctk.CTkFrame(self.person_root, fg_color = self.root.cget('fg_color'))
        buttframe.columnconfigure(0, weight = 1)
        buttframe.columnconfigure(1, weight = 1)

        #Add a button to confirm the input
        butt_person = ctk.CTkButton(buttframe, text = 'OK', command = self.get_person)
        butt_person.grid(row = 0, column = 0, padx = 20, pady = 20)

        #Add a button for returning to the main page
        butt_main_page = ctk.CTkButton(buttframe, text = 'Back', command = self.person_root.destroy)
        butt_main_page.grid(row = 0, column = 1, padx = 20, pady = 20)

        #Put frame into the window
        buttframe.grid(row = 2, column = 0, padx = 20, pady = 20)

        #Center everything
        self.person_root.grid_columnconfigure(0, weight = 1)

        #Put in focus
        self.person_root.grab_set()

    def get_person(self):
        """
        Function for the OK button in the Person window. Gets the output and closes the window
        """
        #Load data
        self.df = pd.read_csv('D:\My stuff\Coding\MČR\MČR results.csv', index_col = 'Osoba', dtype = str) #Results in a table for a quick search
        self.df_links = pd.read_csv('D:\My stuff\Coding\MČR\MČR links.csv')
        with open('D:\My stuff\Coding\MČR\mcr_results.pkl', 'rb') as handle:
            self.mcr_results = pickle.load(handle)

        #Get the output
        person = self.person_textbox.get()

        #Close the window
        self.person_root.destroy()

        #Get the results
        index_check = self.search_index(person)

        #Create a window for the final output
        self.person_output_root = ctk.CTkToplevel(self.root)
        self.center_window(500 if index_check == 'Not found' else 700, 200 if index_check == 'Not found' else 500, self.person_output_root)
        self.person_output_root.title('ČSTS MČR database')
        self.person_output_root.after(250, lambda: self.person_output_root.iconbitmap('cstslogo.ico'))

        
        if index_check == 'Not found':
            if person == '':
                label_text = 'Please specify a valid name'
            else:
                label_text = f'No results were found for {person}'
            res = ctk.CTkLabel(self.person_output_root, text = label_text, justify = 'center', wraplength = 400)
            res.grid(row = 0, column = 0, padx = 20, pady = 20)

            #Create a grid for the buttons
            buttframe = ctk.CTkFrame(self.person_output_root, fg_color = self.root.cget('fg_color'))
            buttframe.columnconfigure(0, weight = 1)
            buttframe.columnconfigure(1, weight = 1)
            buttframe.columnconfigure(2, weight = 1)

            #Button for continuing the search
            butt_next = ctk.CTkButton(buttframe, text = 'Try again', command = self.person_butt_next)
            butt_next.grid(row = 0, column = 0, padx = 20, pady = 20)

            #Button for returning to the main page
            butt_main_page = ctk.CTkButton(buttframe, text = 'Main page', command = self.person_output_root.destroy)
            butt_main_page.grid(row = 0, column = 1, padx = 20, pady = 20)

            #Button for canceling
            butt_canc = ctk.CTkButton(buttframe, text = 'Cancel', command = self.cancel_person)
            butt_canc.grid(row = 0, column = 2, padx = 20, pady = 20)

            #Put frame into the window
            buttframe.grid(row = 1, column = 0, padx = 20, pady = 20)
        else:
            #Get the results
            res_df = self.df.loc[index_check, :].dropna().reset_index() #Find the person, keep only relevant competitions and make the index a column
            res_df['index'] = res_df['index'].str.replace('Do 21let', 'Do\xa021let') #Replace a space with a special character so a split can be done
            res_df[['Year', 'Age group', 'Category']] = res_df['index'].str.split(' ', expand = True) #Split the index into columns
            res_df.drop('index', axis = 1, inplace = True) #Drop the obsolete index
            res_df['Age group'] = res_df['Age group'].str.replace('Do\xa021let', 'Do 21let')
            res_df.rename(columns = {index_check : 'Rank'}, inplace = True) #Rename the column with the rank
            res_df = res_df.loc[:, ['Year', 'Age group', 'Category', 'Rank']] #Rearrange the columns
            res_df['Partner'] = '' #Prepare a column for the partner in each competition
            for i in res_df.index:  #Loop through all competitions
                comp_id = self.df_links.loc[(self.df_links['Year'].astype(str) == res_df.loc[i, 'Year']) & (self.df_links['Age group'] == res_df.loc[i, 'Age group']) & (self.df_links['Category'] == res_df.loc[i, 'Category']), :].index[0] #Find the competition
                comp = self.mcr_results[comp_id] #Get the competition table
                if index_check in comp['Partner'].values:
                    partner = comp.loc[comp['Partner'] == index_check, 'Partnerka'].values[0] #Get the partner (female)
                else:
                    partner = comp.loc[comp['Partnerka'] == index_check, 'Partner'].values[0] #Get the partner (male)
                res_df.loc[i, 'Partner'] = partner #Store the partner
            res_df = np.vstack([res_df.columns, res_df.values]).tolist() #Add columns as a first row and convert to numpy array

            #Add label
            label = ctk.CTkLabel(self.person_output_root, text = f'Results for {person}', justify = 'center', wraplength = 400)
            label.grid(row = 0, column = 0, padx = 20, pady = 20)

            #Create a scrollable frame
            frame = ctk.CTkScrollableFrame(self.person_output_root, width = 600, height = 300, fg_color = self.root.cget('fg_color'))
            frame.columnconfigure(0, weight = 1)

            #Create the table
            table = CTkTable(frame, row = len(res_df), column = len(res_df[0]), values = res_df, header_color = ['#3B8ED0', '#1F6AA5'])
            table.pack(expand=True, fill="both")

            #Add the frame
            frame.grid(row = 1, column = 0)

            #Create a grid for the buttons
            buttframe = ctk.CTkFrame(self.person_output_root, fg_color = self.root.cget('fg_color'))
            buttframe.columnconfigure(0, weight = 1)
            buttframe.columnconfigure(1, weight = 1)
            buttframe.columnconfigure(2, weight = 1)

            #Button for continuing the search
            butt_next = ctk.CTkButton(buttframe, text = 'Find next', command = self.person_butt_next)
            butt_next.grid(row = 0, column = 0, padx = 20, pady = 20)

            #Button for returning to the main page
            butt_main_page = ctk.CTkButton(buttframe, text = 'Main page', command = self.main_page_person_output)
            butt_main_page.grid(row = 0, column = 1, padx = 20, pady = 20)

            #Button for canceling
            butt_canc = ctk.CTkButton(buttframe, text = 'Cancel', command = self.cancel_person)
            butt_canc.grid(row = 0, column = 2, padx = 20, pady = 20)

            #Put frame into the window
            buttframe.grid(row = 2, column = 0, padx = 20, pady = 20)

        #Center everything
        self.person_output_root.grid_columnconfigure(0, weight = 1)

        #Put in focus
        self.person_output_root.grab_set()

    
    def person_butt_next(self):
        """
        Function serving as a command for the Find next button of the Person output window. Destroys the output window and puts the input window forward
        """
        self.person_output_root.destroy()
        self.person_window()
    
    def search_index(self, x):
        """
        Function attempting to find a name in the index given the user input
        """
        x = x.strip() #Remove trailing spaces
        if x in self.df.index:
            return x
        elif ' '.join(x.split(' ')[::-1]) in self.df.index:
            return ' '.join(x.split(' ')[::-1])
        else:
            return 'Not found'
        
    def center_window(self, width, height, wind):
        """
        Function used to make a window appear in the middle of the screen
        """
        #Get screen width and height
        screen_width = wind.winfo_screenwidth()
        screen_height = wind.winfo_screenheight()

        #Calculate position x and y coordinates
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)

        #Specify the position
        wind.geometry(f'{width}x{height}+{int(x)}+{int(y)}')

    def main_page_person_output(self):
        """
        Function serving as a command for button returning to the main page from the person window
        """
        self.person_output_root.destroy()
        self.root.lift()
    
    def cancel_person(self):
        """
        Function serving as a command for the cancel button in the person widget
        """
        self.person_output_root.destroy()
        self.root.destroy()

    def comp_window(self):
        """
        Function getting competition information from the user
        """
        #Load data
        self.df_links = pd.read_csv('D:\My stuff\Coding\MČR\MČR links.csv')
        with open('D:\My stuff\Coding\MČR\mcr_results.pkl', 'rb') as handle:
            self.mcr_results = pickle.load(handle)
        
        #Create a window
        self.comp_root = ctk.CTkToplevel(self.root)
        self.center_window(500, 300, self.comp_root)
        self.comp_root.title('ČSTS MČR Database')
        self.comp_root.after(250, lambda: self.comp_root.iconbitmap('cstslogo.ico'))

        #Add a label
        label = ctk.CTkLabel(self.comp_root, text = 'Please specify the data for the desired competition', justify = 'center', wraplength = 400)
        label.grid(row = 0, column = 0, padx = 20, pady = 20)

        #Add a menu for year
        self.year_menu = ctk.CTkOptionMenu(self.comp_root, values = self.df_links['Year'].unique().astype(str))
        self.year_menu.grid(row = 1, column = 0, padx = 20, pady = 10)
        self.year_menu.set('Select year')

        #Add a menu for age group
        self.age_group_menu = ctk.CTkOptionMenu(self.comp_root, values = self.df_links['Age group'].unique())
        self.age_group_menu.grid(row = 2, column = 0, padx = 20, pady = 10)
        self.age_group_menu.set('Select age group')

        #Add a menu for category
        self.category_menu = ctk.CTkOptionMenu(self.comp_root, values = self.df_links['Category'].unique())
        self.category_menu.grid(row = 3, column = 0, padx = 20, pady = 10)
        self.category_menu.set('Select category')

        #Create a grid for the buttons
        buttframe = ctk.CTkFrame(self.comp_root, fg_color = self.root.cget('fg_color'))
        buttframe.columnconfigure(0, weight = 1)
        buttframe.columnconfigure(1, weight = 1)
        buttframe.columnconfigure(2, weight = 1)

        #Add an OK button
        butt_comp = ctk.CTkButton(buttframe, text = 'OK', command = self.get_comp)
        butt_comp.grid(row = 0, column = 0, padx = 10)

        #Add a main page button
        butt_main = ctk.CTkButton(buttframe, text = 'Main page', command = self.comp_root.destroy)
        butt_main.grid(row = 0, column = 1, padx = 10)

        #Add a cancel button
        butt_canc = ctk.CTkButton(buttframe, text = 'Cancel', command = self.cancel_comp_root)
        butt_canc.grid(row = 0, column = 2, padx = 10)

        #Put the frame in the window
        buttframe.grid(row = 4, column = 0, pady = 20)

        #Center everything
        self.comp_root.grid_columnconfigure(0, weight = 1)

        #Put in focus
        self.comp_root.grab_set()
    
    def cancel_comp_root(self):
        '''
        Function serving as a command for the cancel button in the comp window
        '''
        self.comp_root.destroy()
        self.root.destroy()

    def get_comp(self):
        """
        Function for the OK button in the Competition window. Get the output and close the window
        """
        #Get the index of the competition
        year = self.year_menu.get()
        age_group = self.age_group_menu.get()
        category = self.category_menu.get()
        try:
            ind = np.where((self.df_links['Year'] == int(year)) & (self.df_links['Age group'] == age_group) & (self.df_links['Category'] == category))[0][0]
        except IndexError:
            ind = None

        #Close the competition window
        self.comp_root.destroy()
        
        #Create a window for the final output
        self.comp_output_root = ctk.CTkToplevel(self.root)
        self.center_window(700 if ind is not None else 500, 500 if ind is not None else 200, self.comp_output_root)
        self.comp_output_root.title('ČSTS MČR Database')
        self.comp_output_root.after(250, lambda: self.comp_output_root.iconbitmap('cstslogo.ico'))

        if ind is not None:
            #Get the results
            res_df = self.mcr_results[ind]
            res_df = np.vstack([res_df.columns, res_df.values]).tolist() #Add columns as a first row and convert to numpy array

            #Add label
            label = ctk.CTkLabel(self.comp_output_root, text = f'Results for year: {year}, age group: {age_group}, and category: {category}', justify = 'center', wraplength = 500)
            label.grid(row = 0, column = 0, padx = 20, pady = 20)

            #Create a scrollable frame
            frame = ctk.CTkScrollableFrame(self.comp_output_root, width = 600, height = 300, fg_color = self.root.cget('fg_color'))
            frame.columnconfigure(0, weight = 1)

            #Create the table
            table = CTkTable(frame, row = len(res_df), column = len(res_df[0]), values = res_df, header_color = ['#3B8ED0', '#1F6AA5'])
            table.pack(expand = True, fill="both")

            #Add the frame
            frame.grid(row = 1, column = 0, padx = 20, pady = 20)

            #Create a grid for the buttons
            buttframe = ctk.CTkFrame(self.comp_output_root, fg_color = self.root.cget('fg_color'))
            buttframe.columnconfigure(0, weight = 1)
            buttframe.columnconfigure(1, weight = 1)
            buttframe.columnconfigure(2, weight = 1)

            #Button for continuing the search
            butt_next = ctk.CTkButton(buttframe, text = 'Find next', command = self.try_again)
            butt_next.grid(row = 0, column = 0, padx = 10)

            #Button for returning to the main page
            butt_main = ctk.CTkButton(buttframe, text = 'Main page', command = self.comp_output_root.destroy)
            butt_main.grid(row = 0, column = 1, padx = 10)

            #Button for canceling
            butt_canc = ctk.CTkButton(buttframe, text = 'Cancel', command = self.cancel_comp)
            butt_canc.grid(row = 0, column = 2, padx = 10)

            #Put frame into the window
            buttframe.grid(row = 2, column = 0, padx = 20, pady = 20)
        
        else:   
            #In case no such competition is found
            res = ctk.CTkLabel(self.comp_output_root, text = 'No competition was found for the given combination', justify = 'center', wraplength = 400)
            res.grid(row = 0, column = 0, padx = 20, pady = 20)

            #Add a frame for the buttons
            buttframe = ctk.CTkFrame(self.comp_output_root, fg_color = self.root.cget('fg_color'))
            buttframe.columnconfigure(0, weight = 1)
            buttframe.columnconfigure(1, weight = 1)
            buttframe.columnconfigure(2, weight = 1)

            #Create a try again button
            butt_next = ctk.CTkButton(buttframe, text = 'Try again', command = self.try_again)
            butt_next.grid(row = 0, column = 0, padx = 10)

            #Create a main page button
            butt_main = ctk.CTkButton(buttframe, text = 'Main page', command = self.comp_output_root.destroy)
            butt_main.grid(row = 0, column = 1, padx = 10)

            #Create a cancel button
            butt_canc = ctk.CTkButton(buttframe, text = 'Cancel', command = self.cancel_comp)
            butt_canc.grid(row = 0, column = 2, padx = 10)

            #Put frame into the window
            buttframe.grid(row = 1, column = 0, padx = 20, pady = 20)

        #Center everything
        self.comp_output_root.grid_columnconfigure(0, weight = 1)

        #Put in focus
        self.comp_output_root.grab_set()

    def cancel_comp(self):
        """
        Function serving as a command for the cancel button in the competition widget
        """
        self.comp_output_root.destroy()
        self.root.destroy()

    def try_again(self):
        '''
        Function serving as a command for the try again and find next buttons in the competition window
        '''
        self.comp_output_root.destroy()
        self.comp_window()

Window()