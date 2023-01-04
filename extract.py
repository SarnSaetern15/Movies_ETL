# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 14:18:44 2023

@author: sarns
"""
import requests
from datetime import datetime
import re
from transform import Transform_Data


class Extract_Data:
    """ extracts and formats data from IMBd API"""
    def __init__(self):
        self.imdb_token = 'YOUR IMDb TOKEN HERE'
        self.youtube_token = 'YOUR YOUTUBE TOKEN HERE'
    
    def imdb_api(self,textbox): #extracts data from IMDb API 
        self.movie = Transform_Data().title_validation(textbox) #gets rid of special characters 
        self.movie_plus = re.sub("\s", "+", str(self.movie))
        self.url = f"http://www.omdbapi.com/?t={self.movie_plus}&apikey={self.imdb_token}"
        self.r = requests.get(self.url)
        self.data = self.r.json()
        #print (self.data)
        return self.data
    
    def youtube_api(self,textbox):
        self.query = Transform_Data().title_validation(textbox) #gets rid of special characters 
        self.query = textbox.replace(" ", "").lower()
        self.video_url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&key={self.youtube_token}&type=video&q={self.query}&order=title'
        self.video_r = requests.get(self.video_url)
        self.video_data = self.video_r.json()
        self.video_id = (self.video_data["items"][0]['id']['videoId'])
        #print(self.video_data)
        return self.video_id
        
    def timestamp(self):
        self.date = datetime.now()
        self.date_formatted = datetime.today().strftime('%m/%d/%Y')
        self.current_time = self.date.strftime("%H:%M:%S")
        self.time = Transform_Data().timeConvert(self.current_time)
        self.now = f"{self.date_formatted} {self.time}"
        return self.now
        
    def title(self,data):
        if 'Title' in data: 
            self.title_db = data["Title"]
        else:
            self.title_db = "NA"
        return self.title_db
    
    def year(self,data):
        if 'Year' in data: 
            self.date = data["Year"]
        else:
            self.date = "NA"
        return self.date
    
    def runtime(self,data):
        if 'Runtime' in data: 
            self.runtime = data["Runtime"]
        else:
            self.runtime = "NA"
        return self.runtime
        
    def rotten_tomatoes(self,data):
        if len(data["Ratings"]) > 1 and data["Ratings"][1].get('Source') == 'Rotten Tomatoes': 
            rt_value = (data["Ratings"][1]['Value'])
        else:
            rt_value = 'NA'
        return rt_value
     
    def imdb(self,data):
        if len(data["Ratings"]) > 0 and data["Ratings"][0].get('Source') == 'Internet Movie Database': 
            imdb_dict = (data["Ratings"][0])
            imdb_dict.get('Source')
            if imdb_dict.get('Source') == 'Internet Movie Database':
                imdb_value = (data["Ratings"][0]['Value'])
        else:
            imdb_value = 'NA'
        return imdb_value
    
    def __str__(self,data):
        self.title = data["Title"]
        self.year = data["Year"]
        self.runtime = Extract_Data(data).convert_movie_time()
        self.rt = Extract_Data(data).rotten_tomatoes()
        self.imdb = Extract_Data(data).imdb()
        return f"{self.title}, {self.year}, {self.runtime}, {self.rt}, {self.imdb}"  
