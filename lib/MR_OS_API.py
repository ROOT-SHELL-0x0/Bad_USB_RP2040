import os
from time import sleep

def stop():
    sleep(1000);
class listbox:
    def __init__(self,type_of_obj,oled,path="/lib/DATA/"):
        self.type=type_of_obj
        self.path=path
        self.oled=oled
        self.index=0
        self.index_page=0
        self.payloads_dict=self.get_dir(path)
        self.get_page_payloads()
        
    
    
    
    
    
    
    
    def get_page_payloads(self):
        if self.payloads_dict[0]=="NODATA":
            return ["NODATA"]
        
        for inde,lista in self.payloads_dict.items():
            if  inde==self.index_page:
                self.page_payloads=lista
    
    def get_dir(self,path="/lib/DATA"):
        payloads=os.listdir(path)
        payloads=sorted(payloads)
        if len(payloads)==0:
            return ["NODATA"]
        payloads_dict={}
        for i in range(0,len(payloads),5):
            payloads_dict[i//5]=payloads[i:i+5]
        return payloads_dict
    
    def get_element(self):
        return self.page_payloads[self.index]
    
    def draw(self):
        if self.payloads_dict[0]=="NODATA":
            self.oled.clear()
            self.oled.text("NO DATA!",30,30,"AA")
            self.oled.show()
            sleep(1)
            self.oled.clear()
            return "NODATA"
            
        self.oled.clear()
        pos_y=10
        for index_en,item in enumerate(self.page_payloads):
            self.oled.text(item,10,pos_y,"AA");
            if index_en==self.index:
                self.oled.circle(80,pos_y+3,3,1)
            pos_y+=10;
            self.oled.text(f"{self.index_page+1}/{len(self.payloads_dict)}",100,5,"AAA")
        self.oled.show()
        return None
    
    
    def down(self):
        self.index+=1
        if self.index >= len(self.page_payloads):
            if self.index_page+1<len(self.payloads_dict):
                self.index_page+=1
                self.get_page_payloads()
            elif self.index_page+1==len(self.payloads_dict):
                self.index_page=0
                self.get_page_payloads()
                
                
            self.index = 0
        
        self.draw()
    
    def up(self):
        self.index-=1
        
        if self.index == -1:
            if self.index_page!=0:
                self.index_page-=1
                self.get_page_payloads()
                self.index=len(self.page_payloads)-1
                
            elif self.index_page==0:
                self.index_page=len(self.payloads_dict)-1
                self.get_page_payloads()
                self.index=len(self.page_payloads)-1
                
                
        
                
        self.draw()



class file_system():
    def __init__(self):
        None
    def get_file_type(self,path):
        f=open(path,"r",encoding="utf-8")
        data=f.readlines()
        try:
            return data[0][5:].strip()
        except:
            return "NO FILE TYPE"
        
        
    def read_file(self,path):
        f=open(path,"r",encoding="utf-8")
        lines=f.readlines()
        data=""
        for line in lines:
            if "type" not in line:
                data+=line
        return data
            
class text:
    def __init__(self,type_of_obj,oled,data):
        self.type=type_of_obj
        self.data=data
        self.oled=oled
    
    
    
    def down(self):
        self.oled.scroll_text_vertical(direction="down")
        self.oled.show()
    def up(self):
        self.oled.scroll_text_vertical(direction="up")
        self.oled.show()
    def draw(self):
        
        self.oled.clear()
        self.oled.text(self.data,1,1)
        self.oled.show()


class Bad_USB:
    def __init__(self,type_of_obj,oled,data,name):
        self.oled=oled
        self.oled.y=1
        self.type=type_of_obj
        self.data_raw=data.split()
        self.data=''
        self.name=name
        
        self.data+=f"File:{name}"+self.get_stub("f'File:{name}'")
        for data in self.data_raw:
            if data != "Тип выбранного файла:bad_usb" and data != "STOP_INFO":
                self.data+=data+self.get_stub(data)
            if data == "STOP_INFO":
                break
        

            
    
    
    
        
        
        
    
    def down(self):
        self.oled.scroll_text_vertical(direction="down")
        self.oled.show()
        
    def up(self):
        self.oled.scroll_text_vertical(direction="up")
        self.oled.show()
    def get_stub(self,data):
        a=15-len(data)
        return " " * (a+15)
    def draw(self):
        print(self.data)
        self.oled.clear()
        self.oled.text(self.data,1,self.oled.y)
        self.oled.show()
    
        
        
        
        
        
        