import MR_OS_API
import thisbutton as tb
import board
import os

from time import sleep
class System:
    def __init__(self,oled,path="/lib/DATA"):
        self.debug_on=True
        
        os.chdir("/lib/DATA")
        self.window_type="listbox"
        self.file_system=MR_OS_API.file_system()
        self.oled=oled
        self.path=os.getcwd()
        self.main_interface=MR_OS_API.listbox("listbox",oled,path)
        
        self.Bt1=tb.thisButton(board.GP19,False)
        self.Bt2=tb.thisButton(board.GP20,False)
        self.Bt3=tb.thisButton(board.GP21,False)
        
        
        self.Bt1.assignClick(lambda: self.b_handler("up"))
        self.Bt2.assignClick(lambda: self.b_handler("down"))
        self.Bt3.assignClick(lambda: self.b_handler("select"))
        
        
        self.Bt3.assignLongPressStart(lambda: self.b_handler("escape"))
        
        self.debug(f"Dir:{os.getcwd()}")
        self.debug("System inited!")
        
        self.stack=[]
        self.run()
    
    
    def b_handler(self,com):
#         try:
#            #print(self.main_interface.page_payloads)
#             #print(os.getcwd())
#         except Exception as e:
#             None
        if com == "down":
            self.main_interface.down()
        elif com == "up":
            self.main_interface.up()
        elif com == "select" and self.main_interface.type == "listbox":
            self.select()
        elif com == "select" and self.main_interface.type == "bad_usb":
            self.main_interface.select()
        elif com == "escape":
            self.escape()

    
            
        
    def select(self):
        element=self.main_interface.get_element()
        try:
            typefile=self.file_system.get_file_type(os.getcwd()+"/"+element)
            self.debug("Тип выбранного файла:"+typefile)

            if typefile:
                self.window_type=typefile
                self.window_set_and_view(os.getcwd()+"/"+element,element)
                
        except Exception as e:
            os.chdir(element)
            self.path=os.getcwd()
            self.stack.append(self.main_interface)
            self.main_interface=MR_OS_API.listbox("listbox",self.oled,self.path)
            code=self.main_interface.draw()
            if code=="NODATA":
                self.escape()
            
    
    def escape(self):
        if self.main_interface.type == "text" or self.main_interface.type == "bad_usb":
            None
        else:
            if len(self.stack)>0:
                os.chdir("..")
        try:
            self.debug(f"Был переход \n Новая:{os.getcwd()}\n")
            self.main_interface=self.stack.pop()
            self.path=self.main_interface.path
            self.main_interface.draw()
        except  IndexError:
            None
                
                

    
    def window_set_and_view(self,path_to_file,element):
        if self.window_type=="text":
            self.stack.append(self.main_interface)
            data=self.file_system.read_file(path_to_file)
            file_obj=MR_OS_API.text("text",self.oled,data)
            self.main_interface=file_obj
            self.main_interface.draw()
            self.debug('Отправлено на отрисовку')
        
        if self.window_type=="bad_usb":
            self.stack.append(self.main_interface)
            data=self.file_system.read_file(path_to_file)
            file_obj=MR_OS_API.Bad_USB("bad_usb",self.oled,data,element)
            self.main_interface=file_obj
            self.main_interface.draw()
            self.debug('Отправлено на отрисовку')
            
            
            
        elif self.window_type=="NO FILE TYPE":
            self.error("NO FILE TYPE")
            self.main_interface.draw()
            
            
            
    
    def error(self,text):
        self.oled.clear()
        self.oled.text(text,10,30,"AA")
        self.oled.show()
        sleep(2)
        self.oled.clear()
        
    def debug(self,text):
        if self.debug_on==True:
            print(text)
        
        
    def run(self):
        self.main_interface.draw()
        while True:
            self.Bt1.tick()
            self.Bt2.tick()
            self.Bt3.tick()
            
    
        
        