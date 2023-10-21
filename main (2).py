from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from instructions import txt_instruction, txt_test1, txt_test2, txt_test3, txt_sits
from ruffier import test
from seconds import Seconds
from sits import Sits
from runner import Runner

Window.clearcolor = (.54, .37, .17, .92)
btn_color = (.74, .57, .37, .92)

age = 7
name = ""
p1, p2, p3 = 0,0,0

def check_int(str_num):
    try:
        return int(str_num)
    except:
        return False
class InstrScr(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        instr = Label(text = txt_instruction)
        lbl1 = Label(text = "Enter your name: ", halign = 'right')
        lbl2 = Label(text = "Enter your age: ", halign = 'right')
        
        self.in_name = TextInput(multiline=False)
        self.in_age = TextInput(text = "", multiline=False)
        self.btn = Button(text = "Start", size_hint = (0.3,.2), pos_hint= {'center_x': 0.5})
        self.btn.background_color = btn_color
        self.btn.on_press = self.next
        
        line1 = BoxLayout(size_hint = (.8, None), height = "30sp")
        line2 = BoxLayout(size_hint = (.8, None), height = "30sp")
        line1.add_widget(lbl1)
        line1.add_widget(self.in_name)
        line2.add_widget(lbl2)
        line2.add_widget(self.in_age)
        
        outer = BoxLayout(orientation='vertical', padding = 8, spacing = 8)
        outer.add_widget(instr)
        outer.add_widget(line1)
        outer.add_widget(line2)
        outer.add_widget(self.btn)
        self.add_widget(outer)
                
    def next(self):
        global name, age
        name = self.in_name.text
        age = int(self.in_age.text)
        if age == False or age < 7:
            age = 7
            self.in_age.text = str(age)
        else:
            self.manager.current = "pulse1"


class PulseScr(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.next_screen = False
        instr = Label(text = txt_test1)


        self.lbl_sec = Seconds(15)
        self.lbl_sec.bind(done=self.sec_finished)


        line = BoxLayout(size_hint=(.8, None), height="30sp")
        lbl_result = Label(text= "Enter result: ", halign="right")
        self.in_result = TextInput(text="0", multiline=False)
        self.btn = Button(text="Start", size_hint=(
            0.3, .2), pos_hint={'center_x': 0.5})
        self.btn.background = btn_color
        self.btn.on_press = self.next

        self.line3 = BoxLayout(size_hint=(.8, None), height = "80sp", pos_hint = {'center_x':.5})
        self.line3.add_widget(self.btn)
        line.add_widget(lbl_result)
        line.add_widget(self.in_result)
        outer = BoxLayout(orientation='vertical', padding=8, spacing=8)
        outer.add_widget(instr)
        outer.add_widget(self.lbl_sec)
        outer.add_widget(line)
        outer.add_widget(self.line3)
        self.add_widget(outer)

    def sec_finished(self, *args):
        self.next_screen = True
        self.in_result.set_disabled(False)
        self.btn.set_disabled(False)
        self.btn.text = 'Next step'
        self.line3.remove_widget(self.btn)
        self.line3.add_widget(self.btn)

    def next(self):
        if not self.next_screen:
            self.btn.set_disabled(True)
            self.lbl_sec.start()
        else:
            global p1
            p1 = check_int(self.in_result.text)
            if p1 == False or p1 <= 0:
                p1 = 0
                self.in_result.text = str(p1)
            else:
                self.manager.current = "relax"
        


class RelaxScr(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.next_screen = False

        self.lbl_sits = Sits(30)
        self.run = Runner(total = 30, steptime = 1.5, size_hint = (0.4, 1))
        self.run.bind(finished=self.run_finished)

        instr = Label(text = txt_sits, size_hint=(.3, .2))
        self.btn = Button(text = "Continue", size_hint= (.3,.2), pos_hint = {'center_x':0.5})
        self.btn.background = btn_color
        self.btn.on_press = self.next

        line = BoxLayout()
        vlay = BoxLayout(orientation = "vertical", size_hint=(0.3, 1))
        vlay.add_widget(self.lbl_sits)
        line.add_widget(instr)
        line.add_widget(vlay)
        line.add_widget(self.run)


        outer = BoxLayout(orientation='vertical', padding=8, spacing=8)
        outer.add_widget(line)
        outer.add_widget(self.btn)
        self.add_widget(outer)

    def run_finished(self, instance, value):
        self.btn.set_disabled(False)
        self.btn.text = 'Next step'
        self.next_screen = True
    def next(self):
        if not self.next_screen:
            self.btn.set_disabled(True)
            self.run.start()
            self.run.bind(value=self.lbl_sits.next)
        else:
            self.manager.current = "pulse2"

class PulseScr2(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.next_screen = False
        self.stage = 0

        instr = Label(text = txt_test3)
        line = BoxLayout(size_hint=(.8, None), height="30sp")
        line2 = BoxLayout(size_hint=(.8, None), height="30sp") #!

        self.lbl_sec = Seconds(15)
        self.lbl_sec.bind(done=self.sec_finished)
        self.lbl1 = Label(text = 'Count your heart rate')

        lbl_result1 = Label(text= "Enter result after first test: ", halign="right")
        self.in_result1 = TextInput(text="0", multiline=False)
        
        lbl_result2 = Label(text= "Enter result after second test: ", halign="right")
        self.in_result2 = TextInput(text="0", multiline=False)
        
        self.btn = Button(text="Start", size_hint=(
            0.3, .2), pos_hint={'center_x': 0.5})
        self.btn.background_color = btn_color
        self.btn.on_press = self.next

        self.in_result1.set_disabled(True)
        self.in_result2.set_disabled(True)
        
        line.add_widget(lbl_result1)
        line.add_widget(self.in_result1)
        line2.add_widget(lbl_result2) #!
        line2.add_widget(self.in_result2) #!
        
        outer = BoxLayout(orientation='vertical', padding=8, spacing=8)
        outer.add_widget(instr)
        outer.add_widget(line)
        outer.add_widget(self.lbl1)
        outer.add_widget(self.lbl_sec)
        outer.add_widget(line2) #!
        outer.add_widget(self.btn)
        self.add_widget(outer)

    def sec_finished(self, *args):
        if self.lbl_sec.done == True:
            if self.stage == 0:
                self.stage = 1
                self.lbl1.text = "Relax"
                self.lbl_sec.restart(30)
                self.in_result1.set_disabled(False)
            elif self.stage == 1:
                self.stage = 2
                self.lbl1.text = 'Count your heart rate'
                self.lbl_sec.restart(15)
            elif self.stage == 2:
                self.in_result2.set_disabled(False)
                self.btn.text = "Finish"
                self.next_screen = True
    
    def next(self):
        if not self.next_screen:
            self.btn.set_disabled(False)
            self.lbl_sec.start()
        else:
            global p2, p3
            p2 = int(self.in_result1.text)
            p3 = int(self.in_result2.text)
            if p2 == False:
                p2 = 0
                self.in_result1.text = str(p2)
            elif p3 == False:
                p3 = 0
                self.in_result2.text = str(p3)
            else:
                self.manager.current = "result"


class ResultScr(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.outer = BoxLayout(orientation='vertical', padding = 8, spacing= 8)
        self.instr = Label(text = '')
        self.outer.add_widget(self.instr)
        self.add_widget(self.outer)
        self.on_enter = self.before
    def before(self):
        global name
        self.instr.text = name + "\n" + test(p1,p2,p3, age)
        
        
        
class HeartCheck(App): 
    def build(self):
        sm = ScreenManager()
        sm.add_widget(InstrScr(name="instr"))
        sm.add_widget(PulseScr(name="pulse1"))
        sm.add_widget(RelaxScr(name="relax"))
        sm.add_widget(PulseScr2(name="pulse2"))
        sm.add_widget(ResultScr(name="result"))
        return sm
    
HeartCheck().run()