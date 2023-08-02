import tkinter as tk
from tkinter import ttk
import pandas as pd
import re
import pickle
import numpy as np

class Window:

    def __init__(self):
        #Initiate window
        self.root = tk.Tk()
        self.set_style(self.root, 'awdark')
        self.root.title('MČR database')
        self.center_window(500, 250, self.root)

        #Create a label
        label = ttk.Label(self.root, text = 'Are you looking for a person or for a competition?', justify = 'center', wraplength = 400)
        label.configure(font = (None, 20))
        label.pack(pady = 30)

        #Create a grid for the buttons
        buttframe = ttk.Frame(self.root)
        buttframe.columnconfigure(0, weight = 1)
        buttframe.columnconfigure(1, weight = 1)

        #Button for person search
        butt1 = ttk.Button(buttframe, text = 'Person', command = self.person_window)
        butt1.grid(row = 0, column = 0)

        #Button for competition search
        butt2 = ttk.Button(buttframe, text = 'Competition', command = self.comp_window)
        butt2.grid(row = 0, column = 1)

        #Put frame into the window
        buttframe.pack(expand = True, fill = 'x')

        #Add a button for canceling the window
        butt_cancel = ttk.Button(self.root, text = 'Cancel', command = self.root.destroy)
        butt_cancel.pack(pady = 10)

        self.root.mainloop()

    def person_window(self):
        """
        Function getting a name of the person from the user
        """
        #Create a window
        self.person_root = tk.Tk()
        self.set_style(self.person_root, 'awdark')
        self.center_window(500, 250, self.person_root)
        self.person_root.title('Searching for a person')

        #Add a label
        label = ttk.Label(self.person_root, text = 'Please specify the name of the dancer', justify = 'center', wraplength = 400)
        label.configure(font = (None, 20))
        label.pack(pady = 30)

        #Add a textbox
        self.person_textbox = ttk.Entry(self.person_root, justify = 'center')
        self.person_textbox.pack()

        #Create a grid for the buttons
        buttframe = ttk.Frame(self.person_root)
        buttframe.columnconfigure(0, weight = 1)
        buttframe.columnconfigure(1, weight = 1)

        #Add a button to confirm the input
        butt_person = ttk.Button(buttframe, text = 'OK', command = self.get_person)
        butt_person.grid(row = 0, column = 0)

        #Add a button for returning to the main page
        butt_main_page = ttk.Button(buttframe, text = 'Back', command = self.main_page_person_window)
        butt_main_page.grid(row = 0, column = 1)

        #Put frame into the window
        buttframe.pack(expand = True, fill = 'x')

        self.person_root.mainloop()

    def main_page_person_window(self):
        """
        Function serving as a command for button returning to the main page from the person window
        """
        self.person_root.destroy()
        self.root.lift()

    def get_person(self):
        """
        Function for the OK button in the Person window. Gets the output and closes the window
        """
        #Load data
        self.df = pd.read_csv('D:\My stuff\Coding\CSTS\MČR\MČR results.csv', index_col = 'Osoba', dtype = str)

        #Get the output
        person = self.person_textbox.get()

        #Close the window
        self.person_root.destroy()

        #Create a window for the final output
        self.person_output_root = tk.Tk()
        self.set_style(self.person_output_root, 'awdark')
        self.center_window(500, 500, self.person_output_root)
        self.person_output_root.title(f'Results for {person}')

        #Get the results
        index_check = self.search_index(person)
        if index_check == 'Not found':
            if person == '':
                label_text = 'Please specify a valid name'
            else:
                label_text = f'No results were found for {person}'
            res = ttk.Label(self.person_output_root, text = label_text, justify = 'center', wraplength = 400)
            res.pack(expand = True)

            #Create a grid for the buttons
            buttframe = ttk.Frame(self.person_output_root)
            buttframe.columnconfigure(0, weight = 1)
            buttframe.columnconfigure(1, weight = 1)
            buttframe.columnconfigure(2, weight = 1)

            #Button for continuing the search
            butt_next = ttk.Button(buttframe, text = 'Try again', command = self.person_butt_next)
            butt_next.grid(row = 0, column = 0)

            #Button for returning to the main page
            butt_main_page = ttk.Button(buttframe, text = 'Main page', command = self.main_page_person_output)
            butt_main_page.grid(row = 0, column = 1)

            #Button for canceling
            butt_canc = ttk.Button(buttframe, text = 'Cancel', command = self.cancel_person)
            butt_canc.grid(row = 0, column = 2)

            #Put frame into the window
            buttframe.pack(expand = True, fill = 'x')
        else:
            #Get the results
            res_df = self.df.loc[index_check, :].dropna()

            #Create a Frame
            table_frame = ttk.Frame(self.person_output_root)
            table_frame.pack(pady = 20)

            #Add a scrollbar
            table_scroll = ttk.Scrollbar(table_frame)
            table_scroll.pack(side = tk.RIGHT, fill = tk.Y)

            #Initiate the resulting table
            table = ttk.Treeview(table_frame, yscrollcommand = table_scroll.set)
            table.pack()
            table_scroll.config(command = table.yview)

            #Define the columns
            cols = ['Year', 'Age group', 'Category', 'Rank']
            table['columns'] = cols
            table.column("#0", width = 0,  stretch = tk.NO) #The 0th column
            for i in cols:
                table.column(i, anchor = tk.CENTER, width=80)
            for i in cols:
                table.heading(i, text = i, anchor = tk.CENTER)

            #Add data
            for i in res_df.index:
                table.insert(parent = '', index = 'end', text='', values = re.sub('Do 21let', 'Do\xa021let', i).split(' ') + [res_df[i]])

            #Pack the table
            table.pack()

            #Create a grid for the buttons
            buttframe = ttk.Frame(self.person_output_root)
            buttframe.columnconfigure(0, weight = 1)
            buttframe.columnconfigure(1, weight = 1)
            buttframe.columnconfigure(2, weight = 1)

            #Button for continuing the search
            butt_next = ttk.Button(buttframe, text = 'Find next', command = self.person_butt_next)
            butt_next.grid(row = 0, column = 0)

            #Button for returning to the main page
            butt_main_page = ttk.Button(buttframe, text = 'Main page', command = self.main_page_person_output)
            butt_main_page.grid(row = 0, column = 1)

            #Button for canceling
            butt_canc = ttk.Button(buttframe, text = 'Cancel', command = self.cancel_person)
            butt_canc.grid(row = 0, column = 2)

            #Put frame into the window
            buttframe.pack(expand = True, fill = 'x')

        self.person_output_root.mainloop()
    
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
        self.df_links = pd.read_excel('D:\My stuff\Coding\CSTS\MČR\MČR links.xlsx')
        with open('D:\My stuff\Coding\CSTS\MČR\mcr_results.pkl', 'rb') as handle:
            self.mcr_results = pickle.load(handle)

        #Create a window
        self.comp_root = tk.Tk()
        self.set_style(self.comp_root, 'awdark')
        self.center_window(500, 300, self.comp_root)
        self.comp_root.title('Searching for a competition')

        #Add a label
        label = ttk.Label(self.comp_root, text = 'Please specify the data for the desired competition', justify = 'center', wraplength = 400)
        label.pack(pady = 30)

        #Add a menu for year
        self.year_val = tk.StringVar(self.comp_root) #Default value
        self.year_menu = ttk.OptionMenu(self.comp_root, self.year_val, 'Select Year', *self.df_links['Year'].unique())
        self.year_menu.pack()

        #Add a menu for age group
        self.age_group_val = tk.StringVar(self.comp_root) #Default value
        self.age_group_menu = ttk.OptionMenu(self.comp_root, self.age_group_val, 'Select age group', *self.df_links['Age group'].unique())
        self.age_group_menu.pack()

        #Add a menu for category
        self.category_val = tk.StringVar(self.comp_root) #Default value
        self.category_menu = ttk.OptionMenu(self.comp_root, self.category_val, 'Select category', *self.df_links['Category'].unique())
        self.category_menu.pack()

        #Add an OK button
        butt_comp = ttk.Button(self.comp_root, text = 'OK', command = self.get_comp)
        butt_comp.pack(pady = 10)

        self.comp_root.mainloop()

    def get_comp(self):
        """
        Function for the OK button in the Competition window. Get the output and close the window
        """
        #Create a window for the final output
        self.comp_output_root = tk.Tk()
        self.set_style(self.comp_output_root, 'awdark')
        self.center_window(600, 500, self.comp_output_root)
        self.comp_output_root.title(f'Search results')

        #Find the desired competition
        try:
            #Get the index of the competition
            ind = np.where((self.df_links['Year'] == int(self.year_val.get())) & (self.df_links['Age group'] == self.age_group_val.get()) & (self.df_links['Category'] == self.category_val.get()))[0][0]
            
            #Close the competition window
            self.comp_root.destroy()

            #Get the results
            res_df = self.mcr_results[ind]

            #Create a Frame
            table_frame = ttk.Frame(self.comp_output_root)
            table_frame.pack(pady = 20)

            #Add a scrollbar
            table_scroll = ttk.Scrollbar(table_frame)
            table_scroll.pack(side = tk.RIGHT, fill = tk.Y)

            #Initiate the resulting table
            table = ttk.Treeview(table_frame, yscrollcommand = table_scroll.set)
            table.pack()
            table_scroll.config(command = table.yview)

            #Define the columns
            cols = ['Rank', 'Male partner', 'Female partner', 'Club']
            table['columns'] = cols
            table.column("#0", width = 0,  stretch = tk.NO) #The 0th column
            table.column('Rank', anchor = tk.CENTER, width = 50)
            table.column('Male partner', anchor = tk.CENTER, width = 120)
            table.column('Female partner', anchor = tk.CENTER, width = 120)
            table.column('Club', anchor = tk.CENTER, width = 180)
            for i in cols:
                table.heading(i, text = i, anchor = tk.CENTER)

            #Add data
            for _, i in res_df.iterrows():
                table.insert(parent = '', index = 'end', text = '', values = list(i.values))

            #Pack the table
            table.pack()

            #Create a grid for the buttons
            buttframe = ttk.Frame(self.comp_output_root)
            buttframe.columnconfigure(0, weight = 1)
            buttframe.columnconfigure(1, weight = 1)

            #Button for continuing the search
            butt_next = ttk.Button(buttframe, text = 'Find next', command = self.comp_output_root.destroy)
            butt_next.grid(row = 0, column = 0)

            #Button for canceling
            butt_canc = ttk.Button(buttframe, text = 'Cancel', command = self.cancel_comp)
            butt_canc.grid(row = 0, column = 1)

            #Put frame into the window
            buttframe.pack(expand = True, fill = 'x')

        except IndexError:
            #In case no such competition is found
            res = ttk.Label(self.comp_output_root, text = 'No competition was found for the given combination', justify = 'center', wraplength = 400)
            res.pack(expand = True)
        
        self.comp_output_root.mainloop()

    def cancel_comp(self):
        """
        Function serving as a command for the cancel button in the competition widget
        """
        self.comp_output_root.destroy()
        self.root.destroy()

    def set_style(self, wind, style):
        """
        Function setting a style of the given root
        """
        wind.tk.call('lappend', 'auto_path', 'D:/My stuff/Coding/CSTS/MČR/awthemes-10.4.0')
        wind.tk.call('package', 'require', style)
        wind_style = ttk.Style(wind)
        wind_style.theme_use(style)
        wind.configure(bg = wind_style.lookup('TFrame', 'background'))

Window()