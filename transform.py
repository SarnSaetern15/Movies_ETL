# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 14:25:09 2023

@author: sarns
"""
import re


class Transform_Data:
    """tranforms the data after extraction and prevents bad data from loading into database"""
    def __init__(self):
        pass

    def timeConvert(self,military):
        hr_min_s = military.split(":")
        hours = int(hr_min_s[0])
        if hours == 0: hours = 12
        minutes = int(hr_min_s[1])
        seconds = int(hr_min_s[2])
        setting = "AM"
        if hours >12:
            setting = "PM"
            hours -= 12
        return f"{hours:02}:{minutes:02}:{seconds:02}{setting}"
    
    def convert_movie_time(self,total_minutes):
        if total_minutes == 'N/A':
            return 'NA'
        else:
            space_pos = total_minutes.rfind(" ")
            total_minutes = int(total_minutes [0:space_pos])
            hours = int(total_minutes)//60
            minutes = int(total_minutes) % 60
            if hours < 1:
                return "NA"
            else:
                return f"{hours}h {minutes}m"   
      
    def title_validation(self,title): #removes selected special characters from title input
        regex = re.compile('[@_#%^*()<>/+=\|}{~$]')
        if(regex.search(title) is not None):
            title = re.sub('[@_#%^*()<>/+=\|}{~$]', "", title)
        return title.strip()
          