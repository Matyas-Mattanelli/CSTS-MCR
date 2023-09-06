from kivymd.app import MDApp
from kivy.uix.label import Label 
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivy.uix.screenmanager import NoTransition
from kivy.uix.spinner import Spinner

import pandas as pd
import pickle
import numpy as np

class MCRStatsApp(MDApp):
    '''
    Class representing the application
    '''
    def build(self):
        '''
        Function returning the required widget
        '''
        #Load data
        self.df = pd.read_csv('D:\My stuff\Coding\MČR\MČR results.csv', index_col = 'Osoba', dtype = str) #Results in a table for a quick search
        self.df_links = pd.read_csv('D:\My stuff\Coding\MČR\MČR links.csv')
        with open('D:\My stuff\Coding\MČR\mcr_results.pkl', 'rb') as handle:
            self.mcr_results = pickle.load(handle)

        #Change the theme
        self.theme_cls.theme_style = 'Dark'

        #Change the title
        self.title = 'ČSTS MČR Database'

        #Initiate the screen manager
        self.sm = ScreenManager(transition = NoTransition())

        #Initiate the main screen
        main_screen = Screen(name = 'main_screen')

        #Add a layout
        layout = BoxLayout(orientation = 'vertical')

        #Add a Label
        label = Label(text = 'Are you looking for a person or for a competition?', halign = 'center', font_size = 50) #, size_hint = (1, 0.5)
        label.bind(width = lambda *x: label.setter('text_size')(label, (label.width, None)), texture_size = lambda *x: label.setter('height')(label, label.texture_size[1]))
        layout.add_widget(label)

        #Add a layout for buttons
        butt_layout = BoxLayout()

        #Add a button for person
        butt_person = Button(text = 'Person', background_color = '99CCFF', font_size = 40)
        butt_person.bind(on_press = lambda instance: self.change_screen(instance, 'person_input'))
        butt_layout.add_widget(butt_person)

        #Add a button for competition
        butt_comp = Button(text = 'Competition', background_color = '99CCFF', font_size = 40)
        butt_comp.bind(on_press = lambda instance: self.change_screen(instance, 'comp_input'))
        butt_layout.add_widget(butt_comp)

        #Add the buttons to the main layout
        layout.add_widget(butt_layout)

        #Add a button to cancel the program
        butt_canc = Button(text = 'Cancel', pos_hint = {'center_x' : .5, 'center_y' : .5}, background_color = '99CCFF', font_size = 40)
        butt_canc.bind(on_press = self.stop)
        layout.add_widget(butt_canc)

        #Add the layout to the screen
        main_screen.add_widget(layout)

        #Add the main screen to the manager
        self.sm.add_widget(main_screen)

        #Initiate the person input screen
        person_input_screen = Screen(name = 'person_input')

        #Initiate the layout
        person_input_layout = BoxLayout(orientation = 'vertical')

        #Add a Label
        label_person_input = Label(text = 'Please specify the name of the dancer', halign = 'center', font_size = 50) #, size_hint = (1, 0.5)
        label_person_input.bind(width = lambda *x: label_person_input.setter('text_size')(label_person_input, (label_person_input.width, None)), texture_size = lambda *x: label_person_input.setter('height')(label_person_input, label_person_input.texture_size[1]))
        person_input_layout.add_widget(label_person_input)

        #Add text input
        self.person_input = TextInput(font_size = 40, halign = 'center', hint_text = 'Specify the dancer...', size_hint_y = None, height = 60)
        person_input_layout.add_widget(self.person_input)

        #Add a layout of buttons
        butt_layout_person_input = BoxLayout()

        #Add a button for confirmation
        butt_ok_person_input = Button(text = 'Ok', background_color = '99CCFF', font_size = 40)
        butt_ok_person_input.bind(on_press = lambda instance: self.person(instance))
        butt_layout_person_input.add_widget(butt_ok_person_input)

        #Add a button for returning to the main page
        butt_main_person_input = Button(text = 'Main page', background_color = '99CCFF', font_size = 40)
        butt_main_person_input.bind(on_press = lambda instance: self.change_screen(instance, 'main_screen'))
        butt_layout_person_input.add_widget(butt_main_person_input)

        #Add the buttons to the main layout
        person_input_layout.add_widget(butt_layout_person_input)

        #Add a button to cancel the program
        butt_canc_person_input = Button(text = 'Cancel', pos_hint = {'center_x' : .5, 'center_y' : .5}, background_color = '99CCFF', font_size = 40)
        butt_canc_person_input.bind(on_press = self.stop)
        person_input_layout.add_widget(butt_canc_person_input)

        #Add the layout to the screen
        person_input_screen.add_widget(person_input_layout)

        #Add the screen to the screen manager
        self.sm.add_widget(person_input_screen)

        #Add a screen with the results for person
        person_screen = Screen(name = 'person')
        self.sm.add_widget(person_screen)

        #Initiate the competition input screen
        comp_input_screen = Screen(name = 'comp_input')

        #Initiate the layout
        comp_input_layout = BoxLayout(orientation = 'vertical')

        #Add a Label
        label_comp_input = Label(text = 'Please specify the parameters of the desired competition', halign = 'center', font_size = 50) #, size_hint = (1, 0.5)
        label_comp_input.bind(width = lambda *x: label_comp_input.setter('text_size')(label_comp_input, (label_comp_input.width, None)), texture_size = lambda *x: label_comp_input.setter('height')(label_comp_input, label_comp_input.texture_size[1]))
        comp_input_layout.add_widget(label_comp_input)

        #Add a menu for year
        self.year_menu = Spinner(text = 'Select year', values = self.df_links['Year'].unique().astype(str), font_size = 50)
        comp_input_layout.add_widget(self.year_menu)

        #Add a menu for age group
        self.age_group_menu = Spinner(text = 'Select age group', values = self.df_links['Age group'].unique(), font_size = 50)
        comp_input_layout.add_widget(self.age_group_menu)

        #Add a menu for category
        self.category_menu = Spinner(text = 'Select category', values = self.df_links['Category'].unique(), font_size = 50)
        comp_input_layout.add_widget(self.category_menu)

        #Add a layout of buttons
        butt_layout_comp_input = BoxLayout()

        #Add a button for confirmation
        butt_ok_comp_input = Button(text = 'Ok', background_color = '99CCFF', font_size = 40)
        butt_ok_comp_input.bind(on_press = lambda instance: self.competition(instance))
        butt_layout_comp_input.add_widget(butt_ok_comp_input)

        #Add a button for returning to the main page
        butt_main_comp_input = Button(text = 'Main page', background_color = '99CCFF', font_size = 40)
        butt_main_comp_input.bind(on_press = lambda instance: self.change_screen(instance, 'main_screen'))
        butt_layout_comp_input.add_widget(butt_main_comp_input)

        #Add the buttons to the main layout
        comp_input_layout.add_widget(butt_layout_comp_input)

        #Add a button to cancel the program
        butt_canc_comp_input = Button(text = 'Cancel', pos_hint = {'center_x' : .5, 'center_y' : .5}, background_color = '99CCFF', font_size = 40)
        butt_canc_comp_input.bind(on_press = self.stop)
        comp_input_layout.add_widget(butt_canc_comp_input)

        #Add the layout to the screen
        comp_input_screen.add_widget(comp_input_layout)

        #Add the screen to the screen manager
        self.sm.add_widget(comp_input_screen)

        #Add a screen with the results for competition
        person_screen = Screen(name = 'competition')
        self.sm.add_widget(person_screen)

        return self.sm

    def person(self, instance):
        '''
        Function  rendering the person output screen and putting it into focus
        '''
        #Clear all widgets
        self.sm.get_screen('person').clear_widgets()

        #Initiate the layout
        person_layout = BoxLayout(orientation = 'vertical')

        #Get the input text
        index_check = self.search_index(self.person_input.text)

        if index_check == 'Not found':
            if self.person_input.text == '':
                label_text = 'Please specify a valid name'
            else:
                label_text = f'No results were found for {self.person_input.text}'

            #Add a Label
            label_person = Label(text = label_text, halign = 'center', font_size = 50) #, size_hint = (1, 0.5)
            label_person.bind(width = lambda *x: label_person.setter('text_size')(label_person, (label_person.width, None)), texture_size = lambda *x: label_person.setter('height')(label_person, label_person.texture_size[1]))
            person_layout.add_widget(label_person)

            #Initiate a grid for the buttons
            butt_layout = BoxLayout()

            #Add a button for trying again
            butt_try = Button(text = 'Try again', background_color = '99CCFF', font_size = 40)
            butt_try.bind(on_press = lambda instance: self.change_screen(instance, 'person_input'))
            butt_layout.add_widget(butt_try)

            #Add a button for returning to the main page
            butt_main = Button(text = 'Main page', background_color = '99CCFF', font_size = 40)
            butt_main.bind(on_press = lambda instance: self.change_screen(instance, 'main_screen'))
            butt_layout.add_widget(butt_main)

            #Add the buttons to the main layout
            person_layout.add_widget(butt_layout)

            #Add a button to cancel the program
            butt_canc = Button(text = 'Cancel', pos_hint = {'center_x' : .5, 'center_y' : .5}, background_color = '99CCFF', font_size = 40)
            butt_canc.bind(on_press = self.stop)
            person_layout.add_widget(butt_canc)
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
            res_df = res_df.loc[res_df.index[::-1], :].reset_index(drop = True) #Reversing the order

            #Add a Label
            label_person = Label(text = f'Results for {self.person_input.text}', halign = 'center', font_size = 30, size_hint = (1, 0.1)) #, size_hint = (1, 0.5)
            label_person.bind(width = lambda *x: label_person.setter('text_size')(label_person, (label_person.width, None)), texture_size = lambda *x: label_person.setter('height')(label_person, label_person.texture_size[1]))
            person_layout.add_widget(label_person)

            #Add a table (MDDataTable)
            table = MDDataTable(column_data = [(i, dp(30)) for i in res_df.columns], row_data = [tuple(res_df.loc[i, :].to_list()) for i in res_df.index], rows_num = res_df.shape[0]) #, background_color_cell = 'black', background_color_selected_cell = 'black', background_color_header = 'black'

            #Add the table to the layout
            person_layout.add_widget(table)

            #Initiate a grid for the buttons
            butt_layout = BoxLayout(size_hint = (1, 0.1))

            #Add a button for trying again
            butt_next = Button(text = 'Find next', background_color = '99CCFF', font_size = 40)
            butt_next.bind(on_press = lambda instance: self.change_screen(instance, 'person_input'))
            butt_layout.add_widget(butt_next)

            #Add a button for returning to the main page
            butt_main = Button(text = 'Main page', background_color = '99CCFF', font_size = 40)
            butt_main.bind(on_press = lambda instance: self.change_screen(instance, 'main_screen'))
            butt_layout.add_widget(butt_main)

            #Add the buttons to the main layout
            person_layout.add_widget(butt_layout)

            #Add a button to cancel the program
            butt_canc = Button(text = 'Cancel', pos_hint = {'center_x' : .5, 'center_y' : .5}, size_hint = (1, 0.1), background_color = '99CCFF', font_size = 40)
            butt_canc.bind(on_press = self.stop)
            person_layout.add_widget(butt_canc)

        #Add the layout to the screen
        self.sm.get_screen('person').add_widget(person_layout)

        #Change the screen
        self.sm.current = 'person'

    def competition(self, instance):
        '''
        Function rendering the competiton output screen and putting it into focus
        '''
        #Clear all widgets
        self.sm.get_screen('competition').clear_widgets()

        #Initiate the layout
        comp_layout = BoxLayout(orientation = 'vertical')

        #Get the index of the competition
        year = self.year_menu.text
        age_group = self.age_group_menu.text
        category = self.category_menu.text
        try:
            ind = np.where((self.df_links['Year'] == int(year)) & (self.df_links['Age group'] == age_group) & (self.df_links['Category'] == category))[0][0]
        except IndexError:
            ind = None

        if ind is not None:
            #Get the results
            res_df = self.mcr_results[ind]

            #Add a Label
            label_comp = Label(text = f'Results for year: {year}, age group: {age_group}, and category: {category}', halign = 'center', font_size = 30, size_hint = (1, 0.1)) #, size_hint = (1, 0.5)
            label_comp.bind(width = lambda *x: label_comp.setter('text_size')(label_comp, (label_comp.width, None)), texture_size = lambda *x: label_comp.setter('height')(label_comp, label_comp.texture_size[1]))
            comp_layout.add_widget(label_comp)

            #Add a table (MDDataTable)
            table = MDDataTable(column_data = [(i, dp(30)) for i in res_df.columns], row_data = [tuple(res_df.loc[i, :].to_list()) for i in res_df.index], rows_num = res_df.shape[0], pos_hint = {'center_x' : .5, 'center_y' : .5}, size_hint = {0.9, 0.7}) #, background_color_cell = 'black', background_color_selected_cell = 'black', background_color_header = 'black'

            #Add the table to the layout
            comp_layout.add_widget(table)

            #Initiate a grid for the buttons
            butt_layout = BoxLayout(size_hint = (1, 0.1))

            #Add a button for trying again
            butt_next = Button(text = 'Find next', background_color = '99CCFF', font_size = 40)
            butt_next.bind(on_press = lambda instance: self.change_screen(instance, 'comp_input'))
            butt_layout.add_widget(butt_next)

            #Add a button for returning to the main page
            butt_main = Button(text = 'Main page', background_color = '99CCFF', font_size = 40)
            butt_main.bind(on_press = lambda instance: self.change_screen(instance, 'main_screen'))
            butt_layout.add_widget(butt_main)

            #Add the buttons to the main layout
            comp_layout.add_widget(butt_layout)

            #Add a button to cancel the program
            butt_canc = Button(text = 'Cancel', pos_hint = {'center_x' : .5, 'center_y' : .5}, size_hint = (1, 0.1), background_color = '99CCFF', font_size = 40)
            butt_canc.bind(on_press = self.stop)
            comp_layout.add_widget(butt_canc)
        else:
            #Add a Label
            label_comp = Label(text = f'Results for year: {year}, age group: {age_group}, and category: {category} not found', halign = 'center', font_size = 50) #, size_hint = (1, 0.5)
            label_comp.bind(width = lambda *x: label_comp.setter('text_size')(label_comp, (label_comp.width, None)), texture_size = lambda *x: label_comp.setter('height')(label_comp, label_comp.texture_size[1]))
            comp_layout.add_widget(label_comp)

            #Initiate a grid for the buttons
            butt_layout = BoxLayout()

            #Add a button for trying again
            butt_try = Button(text = 'Try again', background_color = '99CCFF', font_size = 40)
            butt_try.bind(on_press = lambda instance: self.change_screen(instance, 'comp_input'))
            butt_layout.add_widget(butt_try)

            #Add a button for returning to the main page
            butt_main = Button(text = 'Main page', background_color = '99CCFF', font_size = 40)
            butt_main.bind(on_press = lambda instance: self.change_screen(instance, 'main_screen'))
            butt_layout.add_widget(butt_main)

            #Add the buttons to the main layout
            comp_layout.add_widget(butt_layout)

            #Add a button to cancel the program
            butt_canc = Button(text = 'Cancel', pos_hint = {'center_x' : .5, 'center_y' : .5}, background_color = '99CCFF', font_size = 40)
            butt_canc.bind(on_press = self.stop)
            comp_layout.add_widget(butt_canc)

        #Add the layout to the screen
        self.sm.get_screen('competition').add_widget(comp_layout)

        #Change the screen
        self.sm.current = 'competition'
    
    def change_screen(self, instance, name):
        '''
        Function switching to a specifed screen
        '''
        self.sm.current = name
        if name == 'person_input':
            self.person_input.text = ''
        elif name == 'comp_input':
            self.year_menu.text = 'Select year'
            self.age_group_menu.text = 'Select age group'
            self.category_menu.text = 'Select category'
    
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
        
    


MCRStatsApp().run()             