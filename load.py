# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 14:32:20 2023

@author: sarns
"""
import sqlite3


class Load_DB():
    def __init__(self, db_file = ''):
        self.db_file = db_file
        self.remove_set =set() #set of movies already in database
        self.load_list = [] #list to be loaded into database
        self.title_tracker = set() #to remove duplicate title searches before adding to search list
        self.new_search_list = [] #new search list created without dupes instead of removing dupes from original search list
        
    def __enter__(self):
        self.conn = sqlite3.connect(self.db_file)
        return self
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.conn.close()
        
    def load(self, search_list):
        cursor = self.conn.cursor() #opens a cursor and use that cursor to execute the sql command
        cursor.execute("""CREATE TABLE IF NOT EXISTS movies (
                    timestamp text PRIMARY KEY,
                    movie_title text NOT NULL,
                    year text NOT NULL,
                    length text NOT NULL,
                    rotten_tomatoes text NOT NULL,
                    IMDb text NOT NULL,
                    video_ID text NOT NULL,
                    source text NOT NULL
                    )""")
        cursor.executemany("INSERT INTO movies VALUES (?,?,?,?,?,?,?,?)", self.database_validation(search_list)) 
        for row in cursor.execute ("SELECT * FROM movies"): print(f"db:{row}")
        self.conn.commit()
        cursor.close()
            
    def database_validation(self,search_list): #checks movie already in databae against search_list, loads  not already in database. 
        cursor = self.conn.cursor() 
        for row in search_list: #create new search list without duplicate  titles:
            self.title_tracker.add(row[1])   
        for row in search_list:
            if row[1] in self.title_tracker:
                self.title_tracker.remove(row[1])
                self.new_search_list.append(row)
                 
        i = 0 
        while i < len(self.new_search_list): #ensures movie titles in new search list is not already in database:
            for row in cursor.execute ("SELECT * FROM movies WHERE movie_title=?", (self.new_search_list[i][1],)):
                if row is not None and len(self.new_search_list) > 0: #if movie searched exist in database, add to removal set so it won't be loaded
                     self.remove_set.add(self.new_search_list[i][1])
            i += 1

        for element in self.new_search_list:  #add list of movies from new_search_list to load_list if movie is not already in database
            if element[1] not in self.remove_set:
                self.load_list.append(element)
            else:
                print(f"{element[1]} already in database")   
        cursor.close()
        return self.load_list