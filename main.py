from kivy.app import App
from camera import AndroidCamera
from kivy.uix.camera import Camera
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.utils import platform
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from datetime import datetime
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty, StringProperty
from kivy.core.window import Window
from kivy.utils import platform
import base64
import paper_edge_finder
from android.permissions import request_permissions, check_permission, Permission
from kivmob import KivMob, TestIds


class MyCamera(AndroidCamera):
    pass
    
def show_banner_ads():
    seedcounter.ads = KivMob(TestIds.APP)
    seedcounter.ads.new_banner(TestIds.BANNER, top_pos=False)
    seedcounter.ads.request_banner()
    seedcounter.ads.show_banner()

class HomePageBoxLayout(BoxLayout):
    my_camera = ObjectProperty(None)
    image_path = StringProperty('/storage/emulated/0/DCIM/Camera/cactusseedcounter_original.png')

    def go_to_results_page(self, **kwargs):
        seedcounter.screen_manager.transition = SlideTransition(direction="down")
        seedcounter.screen_manager.current = "results"


    def __init__(self, **kwargs):
        super(HomePageBoxLayout, self).__init__()

        self.my_camera = MyCamera()
        #show_banner_ads()
        #self.ads.request_banner()     

    def take_shot(self):
        #try:
        seedcounter.ads.hide_banner()
        self.my_camera._take_picture(self.on_success_shot, self.image_path)
        #except:
        #    ip_pop = InvalidPermissionsPopup()
        #    ip_pop.open()


    def on_success_shot(self, loaded_image_path):
        # converting saved image to a base64 string:
        #image_str = self.image_convert_base64
        number_seeds, uncropped_image_used, seedcounter.contour_path, seedcounter.original_path = paper_edge_finder.count_photo(loaded_image_path)
        seedcounter.output = '[b]The approximate number of seeds is ' + str(number_seeds) + ' seeds.[/b]'
        update_results_page()
        seedcounter.ads.show_banner()
        self.go_to_results_page()
        return True

    def image_convert_base64(self):
        with open(self.image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        if not encoded_string:
            encoded_string = ''
        return encoded_string

    def switch_to_instructionspage(self, **kwargs):
        seedcounter.ads.hide_banner()
        seedcounter.screen_manager.transition = SlideTransition(direction="down")
        seedcounter.screen_manager.current = 'instructionspage'

    def switch_to_takephotopage(self, **kwargs):
        seedcounter.screen_manager.transition = SlideTransition(direction="right")
        seedcounter.screen_manager.current = 'photopage'

    def switch_to_choosefilepage(self, **kwargs):
        seedcounter.screen_manager.transition = SlideTransition(direction="left")
        seedcounter.screen_manager.current = "choosefilepage"


class InstructionsPage(BoxLayout):
    def return_to_homepage(self, **kwargs):
        seedcounter.ads.show_banner()
        seedcounter.screen_manager.transition = SlideTransition(direction="up")
        seedcounter.screen_manager.current = "home"


class FileChooserPage(BoxLayout):
    def __init__(self, **kwargs):
        super(FileChooserPage, self).__init__()
        self.output = "x"
        file_chooser = self.ids.file_chooser
        file_chooser.bind(on_entry_added=self.update_file_list_entry)
        file_chooser.bind(on_subentry_to_entry=self.update_file_list_entry)
        
    def update_file_list_entry(self, file_chooser, file_list_entry, *args):
        file_list_entry.children[0].color = (0, 0, 0, 1)
        file_list_entry.children[1].color = (0, 0, 0, 1)

    def return_to_homepage(self, **kwargs):
        seedcounter.screen_manager.transition = SlideTransition(direction="right")
        seedcounter.screen_manager.current = "home"

    #def display_invalid_filetype(self, **kwargs):


    def go_to_results_page(self, **kwargs):
        seedcounter.screen_manager.transition = SlideTransition(direction="down")
        seedcounter.screen_manager.current = "results"

    def open_popup(self):
        pass

    def selected(self, filename):
        # This is where I'll call the program and run to
        try:
            number_seeds, uncropped_image_used, seedcounter.contour_path, seedcounter.original_path = paper_edge_finder.count_photo(filename[0])
            seedcounter.output = '[b]The approximate number of seeds is ' + str(number_seeds) + ' seeds.[/b]'
            update_results_page()
            self.go_to_results_page()
        except:
            pop = InputPopup()
            pop.open()

def take_photo_from_main():
    seedcounter.homepage.take_shot()

class ContourPopup(Popup):
    img_src = StringProperty('/storage/emulated/0/DCIM/Camera/cactusseedcounter_contours.png')


class OriginalPopup(Popup):
    img_src = StringProperty('/storage/emulated/0/DCIM/Camera/cactusseedcounter_original.png')


class InputPopup(Popup):
    pass
    
class InvalidPermissionsPopup(Popup):
    pass
    
def update_images():
    contour_pop.ids.contours_image.source = seedcounter.contour_path
    original_pop.ids.original_image.source = seedcounter.original_path
    

def update_results_page():
    seedcounter.resultspage.ids.results_text.text = seedcounter.output

class ResultsPage(BoxLayout):
    def update_result_label(self):
        self.results_text.text = seedcounter.output

    def go_to_results_page(self, **kwargs):
        seedcounter.screen_manager.transition = SlideTransition(direction="down")
        seedcounter.screen_manager.current = "results"

    def return_to_homepage(self, **kwargs):
        seedcounter.screen_manager.transition = SlideTransition(direction="up")
        seedcounter.screen_manager.current = "home"

    def switch_to_takephotopage(self, **kwargs):
        seedcounter.screen_manager.transition = SlideTransition(direction="right")
        seedcounter.screen_manager.current = 'photopage'

    def switch_to_choosefilepage(self, **kwargs):
        seedcounter.screen_manager.transition = SlideTransition(direction="left")
        seedcounter.screen_manager.current = "choosefilepage"
        
    def take_another_photo(self, **kwargs):
    	take_photo_from_main()

    def show_contour_popup(self, **kwargs):
        contour_pop = ContourPopup()
        #update_images()
        contour_pop.ids.contours_image.reload()
        contour_pop.open()

    def show_original_popup(self, **kwargs):
        original_pop = OriginalPopup()
        #update_images()
        original_pop.ids.original_image.reload()
        original_pop.open()

class MainWidget(Widget):
    pass

class SeedCounterApp(App):

    def build(self):
        if check_permission('android.permission.READ_EXTERNAL_STORAGE') is False or check_permission('android.permission.CAMERA') is False:
            if check_permission('android.permission.READ_EXTERNAL_STORAGE') is False and check_permission('android.permission.CAMERA') is False:
                request_permissions([Permission.CAMERA, Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
            elif check_permission('android.permission.CAMERA') is False:
                request_permissions([Permission.CAMERA])
            else:
                request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
        
        Window.clearcolor = (0.88235, 0.91765, 0.811765, 1)
        self.screen_manager = ScreenManager()

        self.homepage = HomePageBoxLayout()
        screen = Screen(name='home')
        screen.add_widget(self.homepage)

        self.screen_manager.add_widget(screen)
        show_banner_ads()

        self.instructionspage = InstructionsPage()
        screen = Screen(name='instructionspage')
        screen.add_widget(self.instructionspage)
        self.screen_manager.add_widget(screen)

        self.choosefilepage = FileChooserPage()
        screen = Screen(name='choosefilepage')
        screen.add_widget(self.choosefilepage)
        self.screen_manager.add_widget(screen)

        self.resultspage = ResultsPage()
        screen = Screen(name='results')
        screen.add_widget(self.resultspage)
        self.screen_manager.add_widget(screen)

        return self.screen_manager



seedcounter = SeedCounterApp()
seedcounter.run()

