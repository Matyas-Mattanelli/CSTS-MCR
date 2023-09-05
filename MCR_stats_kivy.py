from kivy.app import App
from kivy.uix.label import Label 
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Color, Rectangle
from kivy.uix.textinput import TextInput
  
# Defining a class
class MCRStatsApp(App):
    '''
    Class representing the application
    '''
    def build(self):
        '''
        Function returning the required widget
        '''
        #Change the title
        self.title = 'ČSTS MČR Database'

        #Initiate the screen manager
        sm = ScreenManager()

        #Define a function for changing the screen
        def change_screen(instance, name):
            '''
            Function switching to a specifed screen
            '''
            sm.current = name

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
        butt_person.bind(on_press = lambda instance: change_screen(instance, 'person_input'))
        butt_layout.add_widget(butt_person)

        #Add a button for competition
        butt_comp = Button(text = 'Competition', background_color = '99CCFF', font_size = 40)
        butt_comp.bind(on_press = lambda instance: change_screen(instance, 'comp_input'))
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
        sm.add_widget(main_screen)

        #Initiate the person input screen
        person_input_screen = Screen(name = 'person_input')

        #Initiate the layout
        person_input_layout = BoxLayout(orientation = 'vertical')

        #Add a Label
        label_person_input = Label(text = 'Please specify the name of the dancer', halign = 'center', font_size = 50) #, size_hint = (1, 0.5)
        label_person_input.bind(width = lambda *x: label_person_input.setter('text_size')(label_person_input, (label_person_input.width, None)), texture_size = lambda *x: label_person_input.setter('height')(label_person_input, label_person_input.texture_size[1]))
        person_input_layout.add_widget(label_person_input)

        #Add text input
        person_input = TextInput(font_size = 40, halign = 'center', hint_text = 'Specify the dancer...', size_hint_y = None, height = 80)
        person_input_layout.add_widget(person_input)

        #Add a layout of buttons
        butt_layout_person_input = BoxLayout()

        #Add a button for confirmation
        butt_ok_person_input = Button(text = 'Ok', background_color = '99CCFF', font_size = 40)
        butt_ok_person_input.bind(on_press = lambda instance: change_screen(instance, 'person'))
        butt_layout_person_input.add_widget(butt_ok_person_input)

        #Add a button for returning to the main page
        butt_main_person_input = Button(text = 'Main page', background_color = '99CCFF', font_size = 40)
        butt_main_person_input.bind(on_press = lambda instance: change_screen(instance, 'main_screen'))
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
        sm.add_widget(person_input_screen)

        return sm

MCRStatsApp().run()             