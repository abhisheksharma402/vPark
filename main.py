from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
import pytesseract
from PIL import Image
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivymd.uix.dialog import MDDialog
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from database import DataBase

Window.size = (300, 500)

# permissions for camera and storage
# plz comment these two lines to compile on desktop
# only for apk development:
# from android.permissions import request_permissions, Permission
# request_permissions([Permission.CAMERA,Permission.WRITE_EXTERNAL_STORAGE,Permission.READ_EXTERNAL_STORAGE])

# Builder string:
screen_helper = """
<LoginScreen>:
    name: "login"

    email: email
    password: password

    FloatLayout:
        Label:
            text: "Login"
            font_size: 20
            color: 0, 0, 0, 1
            size_hint: 0.8, 0.2
            pos_hint: {"x":0.1, "top":1}

        Label:
            text:"Email: "
            color: 0, 0, 0, 1
            font_size: (root.width**2 + root.height**2) / 13**4
            pos_hint: {"x":0.1, "top":0.9}
            size_hint: 0.35, 0.15

        TextInput:
            id: email
            font_size: (root.width**2 + root.height**2) / 13**4
            multiline: False
            pos_hint: {"x": 0.45 , "top":0.85}
            size_hint: 0.4, 0.05

        Label:
            text:"Password: "
            color: 0, 0, 0, 1
            font_size: (root.width**2 + root.height**2) / 13**4
            pos_hint: {"x":0.1, "top":0.7}
            size_hint: 0.35, 0.15

        TextInput:
            id: password
            font_size: (root.width**2 + root.height**2) / 13**4
            multiline: False
            password: True
            pos_hint: {"x": 0.45, "top":0.65}
            size_hint: 0.4, 0.05

        Button:
            pos_hint:{"x":0.35,"y":0.25}
            size_hint: 0.3, 0.1
            font_size: (root.width**2 + root.height**2) / 13**4
            text: "Login"
            on_release:
                root.manager.transition.direction = "up"
                root.loginBtn()

        Button:
            pos_hint:{"x":0.15,"y":0.4}
            size_hint: 0.7, 0.1
            font_size: (root.width**2 + root.height**2) / 13**4
            text: "Don't have an Account? Create One"
            on_release:
                root.manager.transition.direction = "right"
                root.createBtn()



<CreateAccountScreen>:
    name: "create"

    namee: namee
    email: email
    password: passw

    FloatLayout:
        cols:1

        FloatLayout:
            size: root.width, root.height/2

            Label:
                text: "Create an Account"
                color: 0, 0, 0, 1
                size_hint: 0.8, 0.2
                pos_hint: {"x":0.1, "top":1}
    
            Label:
                size_hint: 0.5,0.12
                color: 0, 0, 0, 1
                pos_hint: {"x":0, "top":0.8}
                text: "Name: "

            TextInput:
                pos_hint: {"x":0.5, "top":0.8}
                size_hint: 0.45, 0.1
                id: namee
                multiline: False
                font_size: 13

            Label:
                size_hint: 0.5,0.12
                color: 0, 0, 0, 1
                pos_hint: {"x":0, "top":0.8-0.13}
                text: "Email: "

            TextInput:
                pos_hint: {"x":0.5, "top":0.8-0.13}
                size_hint: 0.45, 0.1
                id: email
                multiline: False
                font_size: 13

            Label:
                size_hint: 0.5,0.12
                color: 0, 0, 0, 1
                pos_hint: {"x":0, "top":0.8-0.13*2}
                text: "Password: "

            TextInput:
                pos_hint: {"x":0.5, "top":0.8-0.13*2}
                size_hint: 0.45, 0.1
                id: passw
                multiline: False
                password: True
                font_size: 13

        Button:
            pos_hint:{"x":0.1,"y":0.25}
            size_hint: 0.8, 0.1
            font_size: 15
            text: "Already have an Account? Log In"
            on_release:
                root.manager.transition.direction = "left"
                root.login()

        Button:
            pos_hint:{"x":0.2,"y":0.05}
            size_hint: 0.6, 0.15
            text: "Submit"
            on_release:
                root.manager.transition.direction = "left"
                root.submit()



<ContentNavigationDrawer>:
    orientation:'vertical'
    Image:
        source:'logo.jpg'
    ScrollView:
        MDList:
            OneLineListItem:
                text: 'Home'                        
                on_release:
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = "home"
            OneLineListItem:
                text: 'Recent Vehicle Searches'                
                on_release: 
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = 'recent'
            OneLineListItem:
                text: 'Settings'                
                on_release: 
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = 'settings'                                    
            OneLineListItem:
                text: 'Help Center'
                on_release:
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = 'help'
            OneLineListItem:
                text: 'Lost Vehicle'                
                on_release: 
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = 'LostVehicle'

<HomeScreen>:
    name: "home"
    MDToolbar:
        pos_hint: {"top": 1}
        elevation: 10
        title: "vPark"
        left_action_items: [["menu", lambda x: root.nav_drawer.set_state("open")]]
        right_action_items: [["face", lambda x: app.ShowProfile()]]
        MDRaisedButton:
            text: 'Alert'
            background_color: 17/255.0, 60/255.0, 216/255.0, 1
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            on_release: app.open_table()
    FloatLayout:
        MDRaisedButton:
            text: 'Start Scanning'
            pos_hint: {'center_x': 0.5, 'center_y': 0.7}
            on_release:
                app.ShowCamera()
    GridLayout:
        cols: 2
        row_default_height: '48dp'
        row_force_default: True
        pos_hint: {'center_x': 0.6, 'center_y': -0.3}
        MDLabel:
            text: 'Insurance Due:'
        MDLabel:
            text: 'Pollution Due:'
        MDLabel:
            text: 'DDMMYYYY'
        MDLabel:
            text: 'DDMMYYYY'
        
<ProfileScreen>:
    name: 'profile'
    n: n
    email: email
    created:created
    MDToolbar:
        pos_hint: {"top": 1}
        elevation: 10
        title: "My Profile"
        left_action_items: [["menu", lambda x: root.nav_drawer.set_state("open")]]
        right_action_items: [['home', lambda x: app.ShowHome()]]
    # BoxLayout:
    #     orientation: 'vertical'
    

    FloatLayout:
        Label:
            id: n
            pos_hint:{"x": 0.1, "top":0.9}
            size_hint:0.8, 0.2
            text: "Account Name: "
            color: 0, 0, 0, 1

        Label:
            id: email
            pos_hint:{"x": 0.1, "top":0.7}
            size_hint:0.8, 0.2
            text: "Email: "
            color: 0, 0, 0, 1

        Label:
            id: created
            pos_hint:{"x": 0.1, "top":0.5}
            size_hint:0.8, 0.2
            text: "Created: "
            color: 0, 0, 0, 1

        Button:
            pos_hint:{"x":0.2, "y": 0.1}
            size_hint:0.6,0.2
            text: "Log Out"
            on_release:
                app.root.current = "login"
                root.manager.transition.direction = "down"
        
<RecentScreen>:
    name: 'recent'
    MDToolbar:
        pos_hint: {"top": 1}
        elevation: 10
        title: "Recent Searches"
        left_action_items: [["menu", lambda x: root.nav_drawer.set_state("open")]]
        right_action_items: [['home', lambda x: app.ShowHome()]]
    BoxLayout:
        orientation: 'vertical'
        MDLabel:
            text: 'Recent Searches'
            halign: 'center'
<HelpScreen>:
    name: 'help'
    MDToolbar:
        pos_hint: {"top": 1}
        elevation: 10
        title: "Help Centre"
        left_action_items: [["menu", lambda x: root.nav_drawer.set_state("open")]]
        right_action_items: [['home', lambda x: app.ShowHome()]]
    BoxLayout:
        orientation: 'vertical'
        MDLabel:
            text: 'Help Centre'
            halign: 'center'
<SettingsScreen>:
    name:'settings'
    MDToolbar:
        pos_hint: {"top": 1}
        elevation: 10
        title: "Settings"
        left_action_items: [["menu", lambda x: root.nav_drawer.set_state("open")]]
        right_action_items: [['home', lambda x: app.ShowHome()]]
    BoxLayout:
        orientation: 'vertical'
        MDLabel:
            text: 'Settings'
            halign: 'center'
<ManualEntryScreen>:
    name: 'MEScreen'
    FloatLayout:
        padding: 50
        orientation: 'vertical'
        Spinner:
            text: '..'
            values: '..','A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
            size_hint: (0.1, 0.05)
            pos_hint: {'center_x': 0.05, 'center_y': 0.5}
        Spinner:
            text: '..'
            values: '..','A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
            size_hint: (0.1, 0.05)
            pos_hint: {'center_x': 0.15, 'center_y': 0.5}
        Spinner:
            text: '..'
            values: '..','0', '1', '2', '3', '4', '5', '6', '7', '8', '9'
            size_hint: (0.1, 0.05)
            pos_hint: {'center_x': 0.25, 'center_y': 0.5}
        Spinner:
            text: '..'
            values: '..','0', '1', '2', '3', '4', '5', '6', '7', '8', '9'
            size_hint: (0.1, 0.05)
            pos_hint: {'center_x': 0.35, 'center_y': 0.5}
        Spinner:
            text: '..'
            values: '..','A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
            size_hint: (0.1, 0.05)
            pos_hint: {'center_x': 0.45, 'center_y': 0.5}
        Spinner:
            text: '..'
            values: '..','A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
            size_hint: (0.1, 0.05)
            pos_hint: {'center_x': 0.55, 'center_y': 0.5}
        Spinner:
            text: '..'
            values: '..','0', '1', '2', '3', '4', '5', '6', '7', '8', '9'
            size_hint: (0.1, 0.05)
            pos_hint: {'center_x': 0.65, 'center_y': 0.5}
        Spinner:
            text: '..'
            values: '..','0', '1', '2', '3', '4', '5', '6', '7', '8', '9'
            size_hint: (0.1, 0.05)
            pos_hint: {'center_x': 0.75, 'center_y': 0.5}
        Spinner:
            text: '..'
            values: '..','0', '1', '2', '3', '4', '5', '6', '7', '8', '9'
            size_hint: (0.1, 0.05)
            pos_hint: {'center_x': 0.85, 'center_y': 0.5}
        Spinner:
            text: '..'
            values: '..','0', '1', '2', '3', '4', '5', '6', '7', '8', '9'
            size_hint: (0.1, 0.05)
            pos_hint: {'center_x': 0.95, 'center_y': 0.5}
        BoxLayout:
            pos_hint:{'center_x':.5}
            spacing: 30
            padding: 30
            MDFlatButton:
                text: 'Cancel'
                on_release: app.ShowCamera()
            MDRaisedButton:
                text: 'Done'
                on_release: app.ManualEntry()
<LostVehicleScreen>:
    name: 'LostVehicle'
    MDToolbar:
        pos_hint: {"top": 1}
        elevation: 10
        title: "Lost Vehicle"
        left_action_items: [["menu", lambda x: root.nav_drawer.set_state("open")]]
        right_action_items: [['home', lambda x: app.ShowHome()]]
    BoxLayout:
        orientation: 'vertical'
        MDLabel:
            text: 'Canvas for Karan ;-)'
            halign: 'center'
<ShowInfoScreen>:
    name: 'InfoScreen'
    MDLabel:
        text: 'Info'
NavigationLayout:
    ScreenManager:
        id: screen_manager
        LoginScreen:
        CreateAccountScreen:
        HomeScreen:
            nav_drawer: nav_drawer
        ProfileScreen:
            nav_drawer: nav_drawer
        RecentScreen:
            nav_drawer: nav_drawer
        HelpScreen:
            nav_drawer: nav_drawer
        SettingsScreen:
            nav_drawer: nav_drawer
        LostVehicleScreen:
            nav_drawer: nav_drawer
        ManualEntryScreen:
        ShowInfoScreen:
        

        Screen:
            name: 'camera'
            FloatLayout:
                MDToolbar:
                    pos_hint: {"top": 1}
                    elevation: 10
                    title: "Camera"
                    left_action_items: [["menu", lambda x: root.ids.nav_drawer.set_state("open")]]
                    right_action_items: [['home', lambda x: app.ShowHome()]]
                Camera:
                    id: cam
                    resolution: (1920,1080)
                    pos_hint : {'center_y':0.5,'center_x':0.5}
                    allow_stretch: True
                MDIconButton:
                    icon: 'camera'
                    text_color: app.theme_cls.primary_color
                    theme_text_color: 'Custom'
                    user_font_size : '40sp'
                    pos_hint : {'center_x':.85,'center_y':.08}
                    on_release:
                        app.OCR()
                MDRaisedButton:
                    text: 'Enter Manually'
                    md_bg_color: app.theme_cls.primary_color
                    pos_hint: {'center_x':0.4,'center_y':0.078}
                    on_release: app.ShowManualEntryScreen()
    MDNavigationDrawer:
        id: nav_drawer
        ContentNavigationDrawer:
            screen_manager: screen_manager
            nav_drawer: nav_drawer

"""
class WindowManager(ScreenManager):
    pass

sm = ScreenManager()
sm1 = WindowManager()

class LoginScreen(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def loginBtn(self):
        if db.validate(self.email.text, self.password.text):
            ProfileScreen.current = self.email.text
            self.reset()
            sm.current = "home"
        else:
            invalidLogin()

    def createBtn(self):
        self.reset()
        sm1.current = "create"

    def reset(self):
        self.email.text = ""
        self.password.text = ""

class CreateAccountScreen(Screen):
    namee = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def submit(self):
        if self.namee.text != "" and self.email.text != "" and self.email.text.count("@") == 1 and self.email.text.count(".") > 0:
            if self.password != "":
                db.add_user(self.email.text, self.password.text, self.namee.text)

                self.reset()

                sm.current = "home"
            else:
                invalidForm()
        else:
            invalidForm()

    def login(self):
        self.reset()
        sm.current = "home"

    def reset(self):
        self.email.text = ""
        self.password.text = ""
        self.namee.text = ""



class HomeScreen(Screen):
    pass


class ProfileScreen(Screen):
    pass


class RecentScreen(Screen):
    pass


class HelpScreen(Screen):
    pass


class SettingsScreen(Screen):
    pass


class ManualEntryScreen(Screen):
    pass


class LostVehicleScreen(Screen):
    pass


class ShowInfoScreen(Screen):
    pass


class ContentNavigationDrawer(BoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()

def invalidLogin():
    pop = Popup(title='Invalid Login',
                content=Label(text='Invalid username or password.'),
                size_hint=(None, None), size=(220, 220))
    pop.open()


def invalidForm():
    pop = Popup(title='Invalid Form',
                content=(Label(text='Please fill in all inputs with valid information.'), Button(text="Go Back")),
                size_hint=(None, None), size=(220, 220))

    pop.open()

db = DataBase("users.txt")


# Create the screen manager

screens = [LoginScreen(name="login"), CreateAccountScreen(name="create")]
for screen in screens:
    sm1.add_widget(screen)

sm.add_widget(HomeScreen(name='home'))
sm.add_widget(ProfileScreen(name='profile'))
sm.add_widget(RecentScreen(name='recent'))
sm.add_widget(HelpScreen(name='help'))
sm.add_widget(ManualEntryScreen(name='MEScreen'))
sm.add_widget(ManualEntryScreen(name='LostVehicle'))
sm.add_widget(ShowInfoScreen(name='InfoScreen'))
# sm.add_widget(CreateAccountScreen(name='create'))

# sm.add_widget(MainScreen(name='main'))


# Main function:
class vParkApp(MDApp):

    def build(self):
        screen = Builder.load_string(screen_helper)
        self.data_tables = MDDataTable(
            size_hint=(0.9, 0.6),
            # name column, width column
            column_data=[
                ("Particulars", dp(20)),
                ("Days Left", dp(20))
            ],
            row_data=[
                ("1. Insurance", ""),
                ("2. Pollution", ""),
                ("3. Service", ""),
                ("4. Driving Licence", "")
            ]
        )
        return screen
    def open_table(self):
        self.data_tables.open()

    # Functions to change screens:
    def ShowProfile(self):
        self.root.ids.screen_manager.current = 'profile'

    def ShowHome(self):
        self.root.ids.screen_manager.current = 'home'

    def ShowCamera(self):
        self.root.ids.screen_manager.current = 'camera'

    def ShowManualEntryScreen(self):
        self.root.ids.screen_manager.current = 'MEScreen'

    def ShowInfo(self):
        self.root.ids.screen_manager.current = 'InfoScreen'
    
    def ShowCreateAccount(self):
        self.root.ids.screen_manager.current = 'create'
    
    def ShowLogin(self):
        self.root.ids.screen_manager.current = 'login'
    
    # def on_start(self):
    #     self.root.ids.screen_manager.current = 'login'

    # Function for OCR (bare for now, needs optimisations, work on it after successful apk build)
    def OCR(self):
        # create a camera variable
        camera1 = self.root.ids['cam']
        # capture a shot and export to png
        camera1.export_to_png("IMG.png")
        # open image in PIL(basically storing image in a variable)
        img = Image.open('IMG.png')
        # OCR using pytesseract stored in a variable named 'data'
        data = pytesseract.image_to_string(img)
        # Create a dialog to show the 'data' on screen and open the dialog
        self.ShowInfo(data)

    # Manual entry function:
    def ManualEntry(self):
        pass


vParkApp().run()
