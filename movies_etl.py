# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 13:22:09 2022

@author: sarns
"""
from extract import Extract_Data
from transform import Transform_Data
from load import Load_DB
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QGridLayout, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt, QEvent, QUrl
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWebEngineWidgets import QWebEngineView #QWebEngineSettings 
from copy import deepcopy


              
class UserInterface(QWidget):
    def __init__(self, video_id, parent=None):
        super().__init__()
        self.parent = parent
        self.video_id = video_id
        self.count = 0 #count to determine whether to clear widgets after search
        self.layout = QVBoxLayout()   #creates a vertical layout 
        self.setLayout(self.layout)   #sets up a vertical layout 
        self.toplayout() 
        
    def search (self):
        self.count +=1
        if self.count > 1: self.clearlayout() #delete all widgets before displaying the new after the second Search click
        self.data = Extract_Data().imdb_api(self.input.text())   #extracts data from IMDb API 
        
        if "Error" in self.data:  # If movie is not found, set self.error = 1
            print (self.data["Error"])
            self.error = 1 
            if self.layout.count() == 6: #adds signature back after every error
                self.signature = QLabel('Sarn Saetern')
                self.layout.addWidget(self.signature, alignment = Qt.AlignBottom | Qt.AlignRight) #bottom signation
            self.count = 0   # count must start over so program does not try to delete widgets if nothing is found as no widgets are produced
            self.input.setText(f"{self.input.text()} NOT FOUND")
        else:
            self.error = 0
            if self.count ==1 and self.layout.count() ==2: #deletes signature after first successful search 
                if self.signature : self.signature .deleteLater() 
        
            #Remaining vertical layout items:
            self.date_label(self.data)        
            self.runtime_label(self.data)
            self.rotten_tomatoe_layout(self.data)
            self.imdb_layout(self.data)
            self.video_id = Extract_Data().youtube_api(self.input.text())  #YouTube Video 
            self.addWebView(self.video_id)
                     
            #creates list of tuples for searches  
            self.timestamp = Extract_Data().timestamp()
            self.title_db = Extract_Data().title(self.data)
            self.tracker = (self.timestamp, self.title_db, self.date, self.run_time, 
                            self.rt, self.imdb, self.video_id, 'API')
            if self.tracker.count('NA') < 2:  #Not to load if two or more NA values
                self.add = deepcopy(self.tracker)
                search_list.append(self.add) 
                #print(f"activities: {search_list}")
                #print("="*40)
            else:
                print(f"Too many NAs: {self.title_db} will NOT be loaded")
                             
    def toplayout(self):
        topLayout = QHBoxLayout()       #create a horizontal layout
        self.layout.addLayout(topLayout)  #sets the horizonal layout as first item on the vertical layout
        self.input = QLineEdit() #creates search textbox:
        self.input.installEventFilter(self)
        title_label = QLabel('Movie Title:')
        topLayout.addWidget(title_label, 1)   #1 = 10% of the horizontal layout
        topLayout.addWidget(self.input,8)   #8 = 80% of the horizontal layout
        buttonSearch = QPushButton('Search', clicked =self.search)
        topLayout.addWidget(buttonSearch,1) #1 = 10% of the horizontal layout
        self.signature = QLabel('Sarn Saetern') #bottom signation
        self.layout.addWidget(self.signature, alignment = Qt.AlignBottom | Qt.AlignRight) 
            
    def clearlayout(self): #clears layout before a new search begin
      for i in range(1,self.layout.count()):    
          if self.layout.itemAt(i).widget() is not None:
              self.layout.itemAt(i).widget().deleteLater() 
          if self.layout.itemAt(i).layout() is not None:
              self.layout.itemAt(i).layout().deleteLater()          
      #ensures all widgets in horizonatal layout are deleted:
      if self.imdb_label: self.imdb_label.deleteLater()     
      if self.rt_label: self.rt_label.deleteLater()   
      if self.rt_logo_label: self.rt_logo_label.deleteLater() 
      if self.imdb_blank_label: self.imdb_blank_label.deleteLater() 
      if self.imdb_logo_label: self.imdb_logo_label.deleteLater() 
      if self.imdb_blank_label: self.imdb_blank_label.deleteLater() 
    
    def date_label(self,data):
        self.date = Extract_Data().year(data) 
        self.layout.addWidget(QLabel(f"{self.date}"))
        
    def runtime_label(self,data):
        self.runtime_mins = Extract_Data().runtime(data) 
        self.run_time = Transform_Data().convert_movie_time(self.runtime_mins)    
        self.layout.addWidget(QLabel(f"{self.run_time}"))
        
    def rotten_tomatoe_layout(self,data):
        #set up rotten tomatoe logo
        self.rt_logo_label = QLabel(self)
        self.rt_pathway = "C:/Users/sarns/Desktop/"+'Personal_Proj/Movies_ETL/Images/Rotten_Tomatoes.png'
        self.pixmap = QPixmap (self.rt_pathway)
        self.rt_logo_label.setPixmap(self.pixmap)
        self.rt_logo_label.resize(self.pixmap.width(),self.pixmap.height())
        self.rt_logo_label.resize(50,50)         
        #rotten tomatoe layout set up:
        rtLayout = QHBoxLayout()       #create a horizontal layout
        self.layout.addLayout(rtLayout)  #sets the horizonal layout as third item on the vertical layout   
        #items on the QHBoxLayout/Horizonal rotten tomatoe Layout: 
        self.rt = Extract_Data().rotten_tomatoes(data)
        self.rt_label = QLabel(f"{self.rt.ljust(120)}")
        self.rt_blank_label = QLabel('')
        rtLayout.addWidget(self.rt_logo_label,1)   #80% = 8
        rtLayout.addWidget(self.rt_label, 1)   #10% = 1 
        rtLayout.addWidget(self.rt_blank_label,8)   #80% = 8
            
    def imdb_layout(self,data):
        #set up IMDb logo:
        self.imdb_logo_label = QLabel(self)
        self.imdb_pathway = "C:/Users/sarns/Desktop/"+'Personal_Proj/Movies_ETL/Images/IMDb.png'
        self.pixmap = QPixmap (self.imdb_pathway)
        self.imdb_logo_label.setPixmap(self.pixmap)
        self.imdb_logo_label.resize(self.pixmap.width(),self.pixmap.height())
        self.imdb_logo_label.resize(50,50)
        #IMDb layout set up:
        imdbLayout = QHBoxLayout()       #create a horizontal layout
        self.layout.addLayout(imdbLayout)  #sets the horizonal layout as third item on the vertical layout
        #items on the QHBoxLayout/Horizonal IMDb Layout:
        self.imdb = Extract_Data().imdb(data)
        self.imdb_label = QLabel(f"{self.imdb.ljust(120)}")
        self.imdb_blank_label = QLabel('')
        imdbLayout.addWidget(self.imdb_logo_label,1)   #10% = 1
        imdbLayout.addWidget(self.imdb_label, 1)   #10% = 1 
        imdbLayout.addWidget(self.imdb_blank_label,8)   #80% = 8
        
    def addWebView(self,video_id):
        self.webview = QWebEngineView()
        self.webview.setUrl(QUrl(f'https://www.youtube.com/embed/{self.video_id}?rel=0'))
        self.layout.addWidget(self.webview)

    def eventFilter(self,source,event): #Enter key to run Search function
        if event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Return:
                self.search()
        return super().eventFilter(source, event)  

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(500,600)        
        self.setWindowTitle("Movie Ratings")
        self.me_pathway = "C:/Users/sarns/Desktop/"+'Personal_Proj/Movies_ETL/Images/me.png'
        self.setWindowIcon(QIcon(self.me_pathway)) 
        
        #video to window below
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.ui = UserInterface('', parent = self)
        self.layout.addWidget(self.ui,2,0)
        
        #set font of widgets
        self.setStyleSheet("""
            QLabel {
                font: bold;
                font-size: 15px;
                color: black;
                }           
                * {
                background-color: skyblue;
                font-size: 20px;
                }          
            QLineEdit {
                background-color: white;
                font-size: 15px;
                }    
            QPushButton {
                background-color: lightgrey;
                font-size: 15px;
                font: bold;
                }  
        """)
        
        
if __name__ == "__main__":
    search_list = []    #list of searches
    app = QApplication(sys.argv) 
    window = Window()
    window.show()
    try:
        sys.exit(app.exec())
    except SystemExit:
        print("Application Closed")
        with Load_DB('movies_etl_db.db') as db: db.load(search_list) #CREATE OR ADD TO DATABASE WHEN CLOSED
            
            
        