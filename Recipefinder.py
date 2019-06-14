# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter.font import Font
from urllib.request import urlopen
import json
import csv
from datetime import datetime, date
import pandas as pd


locu_key = 'f4b8c04bd9c4bf5285310b00222943a7'
app_id = '93a4763e'
entry_date = ''
Participant = 'test'
food_inventory_dif = []

inventory = [] #lege lijst
Locatiecsv = ''
Locatiexlsx = ''

Super1= str
Super2= str
Super3= str
Super4= str
Super5= str
Search1= str
Search2= str
Search3= str
Search4= str
Search5= str
Search6= str
Search7= str
Search8= str
Search9= str
Search10= str
#basis inforamtie is geladen




def zoek():
    ingredient_search(Super1)
    ingredient_search(Super2)
    ingredient_search(Super3)
    ingredient_search(Super4)
    ingredient_search(Super5)
    
def zoek2():
    ingredient_search(Search1)
    ingredient_search(Search2)
    ingredient_search(Search3)
    ingredient_search(Search4)
    ingredient_search(Search5)

def zoek3():
    ingredient_search(Search6)
    ingredient_search(Search7)
    ingredient_search(Search8)
    ingredient_search(Search9)
    ingredient_search(Search10)


def ingredient_search(ingredient):
    api_key = locu_key
    application_id = app_id
    new_ingri = ingredient.replace(' ', '%20')
    url = 'https://api.edamam.com/search?q=' + new_ingri +'&app_id=' + application_id + '&app_key=' + api_key + '&from=0&to=3'
    site_json = urlopen(url)
    data = json.loads(site_json.read())
    
    for item in data['hits']:
        recipe = item['recipe']
        tex.insert(tk.END, ('Titel: '+ recipe['label'] + '\n'))
        tex.insert(tk.END, ('Inbegrepen ingrediënten: ' + ingredient+ '\n'))
        tex.insert(tk.END, ('url: ' + recipe['url']+ '\n'))
        tex.insert(tk.END, '\n')

#Defje voor het opvragen van recepten van het internet, op basis van het de ingredieënten die je hem meegeeft. 
#Ingrediënten dienen gescheiden te worden met een '+' teken



def test():
    global Super1
    global Super2
    global Super3
    global Super4
    global Super5
    global Search1
    global Search2
    global Search3
    global Search4
    global Search5
    global Search6
    global Search7
    global Search8
    global Search9
    global Search10
    
    Participant = myvar.get()
    print (Participant)
    
    inventory = [] #lege lijst
    Locatiecsv = 'Voorraadlijst/' + Participant + '.csv'
    Locatiexlsx = 'Voorraadlijst/' + Participant + '.xlsx'

    with open(Locatiecsv, 'r') as csvfile:
        raw_inventory = csv.reader(csvfile, delimiter=';')
        for row in raw_inventory:
            inventory.append(row)
    #inventory is nu gevuld met de informatie van de participant
    
    
    df = pd.read_excel (r'Voorraadlijst/' + Participant + '.xlsx') #for an earlier version of Excel, you may need to use the file extension of 'xls'
    column1 = df.iloc[:,0]
    nu = column1.dropna()
    nu.drop(df.tail(1).index,inplace=True)
    ned_ingredient = []
        
    for you in nu:
        ned_ingredient.append(you)      
    #Open de inventory van de juiste participant, Hier wordt zowel de nederlandse als de engelse van de vertaling in een 
    #lijst gezet. Deze lijst bevat dus: Artikel(in het nederlands), Artikel (in het engels), houdbaarheidsdatum
        
    for item in inventory:
        if item == ['Voedselproduct', 'geschatte of aangegeven houdbaarheidsdatum ']:
            inventory.remove(item)
        if item == ['', '']:
            inventory.remove(item)
    #de lege velden en het de eerste rij is verwijder        
    for item in inventory:
        if item == ['Voedselproduct', 'geschatte of aangegeven houdbaarheidsdatum ']:
            inventory.remove(item)
        if item == ['', '']:
            inventory.remove(item)
        #de lege velden en het de eerste rij is verwijderd 
        #dit gebeurt 2x, omdat hij in een zeldzaam geval er toch 1 over lijkt te slaan. 
          
    food_inventory = []
    for food_item in inventory:
        if food_item[0] != 'Datum van invullen: ':
            food_inventory.append(food_item)
        
    for a, b in zip(food_inventory, ned_ingredient):
        a.append(b)
            
    for item in food_inventory:
        if item == ('', ''):
            food_inventory.remove(item)
    #de lege velden en het de eerste r
        
    for food, i in enumerate(food_inventory):
        food_inventory[food] = tuple(i)
    
    for item in food_inventory:
        
        if item == ('', ''):
            food_inventory.remove(item)
            
    entry_date1 = inventory[-1][1]
    entry_date = datetime.strptime(entry_date1, '%d-%m-%Y')
    
    hs = ('invuldatum = ' + str(entry_date.strftime('%d-%m-%Y'))) 
    tex.insert(tk.END, hs,)
    tex.insert(tk.END, '\n')
    tex.see(tk.END)   
    
        #entry_date is de variabele die de invuldatum vast houdt. 
        #de food_inventory is nu in tuple's, dit werkt handiger met het opvragen van individuele items. 
        
    food_inventory.sort(key=lambda L: datetime.strptime(L[1], '%d-%m-%Y'))
        
    
    #food inventory is nu geordend op datum (eerst aflopend eerst.) Hij wordt geprint om te checken. 
        
    food_inventory_dif = []
    for x in food_inventory:
        Datum_format = datetime.strptime(x[1], '%d-%m-%Y')
        difference_date = Datum_format - entry_date
        food_inventory_dif.append(x + (difference_date.days,))
        
    x = ('%-35s %-20s %-20s %-s' % ('Product','vertaling','Houdbaarheidsdatum','Aantal dagen houdbaar'))
    tex.insert(tk.END, x)
    tex.insert(tk.END, '\n')
    tex.see(tk.END)  
    for first, second, third, forth in food_inventory_dif:
        s = ('%-35s %-20s %-20s %-s' % (third, first, second, forth))
        tex.insert(tk.END, s)
        tex.insert(tk.END, '\n')
        tex.see(tk.END) 
    tex.insert(tk.END, '\n\n')
    

    #creeëren van een eindoverzicht. Zie het resultaat hieronder.    
    Super1 = food_inventory_dif[0][0] + '+' + food_inventory_dif[1][0] + '+' + food_inventory_dif[2][0] + '+' + food_inventory_dif[3][0] + '+' + food_inventory_dif[4][0]
    Super2 = food_inventory_dif[0][0] + '+' + food_inventory_dif[1][0] + '+' + food_inventory_dif[2][0] + '+' + food_inventory_dif[3][0] 
    Super3 = food_inventory_dif[0][0] + '+' + food_inventory_dif[1][0] + '+' + food_inventory_dif[2][0] + '+' + food_inventory_dif[4][0]
    Super4 = food_inventory_dif[0][0] + '+' + food_inventory_dif[1][0] + '+' + food_inventory_dif[3][0] + '+' + food_inventory_dif[4][0]
    Super5 = food_inventory_dif[0][0] + '+' + food_inventory_dif[2][0] + '+' + food_inventory_dif[3][0] + '+' + food_inventory_dif[4][0] 
        
    Search1 = food_inventory_dif[0][0] + '+' + food_inventory_dif[1][0] + '+' + food_inventory_dif[2][0]
    Search2 = food_inventory_dif[0][0] + '+' + food_inventory_dif[1][0] + '+' + food_inventory_dif[3][0]
    Search3 = food_inventory_dif[0][0] + '+' + food_inventory_dif[2][0] + '+' + food_inventory_dif[3][0]
    Search4 = food_inventory_dif[1][0] + '+' + food_inventory_dif[2][0] + '+' + food_inventory_dif[3][0]
    Search5 = food_inventory_dif[1][0] + '+' + food_inventory_dif[2][0] + '+' + food_inventory_dif[4][0]
        
    Search6 = food_inventory_dif[0][0] + '+' + food_inventory_dif[1][0]
    Search7 = food_inventory_dif[0][0] + '+' + food_inventory_dif[2][0] 
    Search8 = food_inventory_dif[0][0] + '+' + food_inventory_dif[3][0]
    Search9 = food_inventory_dif[1][0] + '+' + food_inventory_dif[2][0]
    Search10 = food_inventory_dif[1][0] + '+' + food_inventory_dif[3][0]



top = tk.Tk()

one = tk.Frame()
one.grid()

myFont = Font(family="Calibri", size=24)
myFont2 = Font(family="Calibri", size=12)
label = tk.Label(one, text='RecipeFinder', font=myFont)
label.grid(row=0, column=0, columnspan=2, sticky=tk.E)

tex = tk.Text(master=top, height=20, width=130)
tex.grid(row= 0, column=1, rowspan=2)


bop = tk.Frame()
bop.grid(row = 1, column=0)

f = tk.Button(bop, text='Recepten1', command=zoek, font=myFont2)
k = tk.Button(bop, text='Recepten2', command=zoek2, font=myFont2)
h = tk.Button(bop, text='Recepten3', command=zoek3, font=myFont2)
g = tk.Button(bop, text='Laad Data', command=test, font=myFont2)


g.grid(sticky=tk.EW)
f.grid(sticky=tk.EW)
k.grid(sticky=tk.EW)
h.grid(sticky=tk.EW)


myvar = tk.StringVar()
def mywarWritten(*args):
    print ("mywarWritten",myvar.get())

myvar.trace("w", mywarWritten)

lab = tk.Label(one, text='Participant')
lab.grid()

text_entry = tk.Entry(one, textvariable=myvar)
text_entry.grid()



tk.Button(bop, text='Delete', command=lambda: tex.delete('1.0', tk.END), font=myFont2).grid(sticky=tk.EW)
tk.Button(bop, text='Exit', command=top.destroy, font=myFont2).grid(sticky=tk.EW)
top.mainloop()

#Het opstellen van de verschillende zoek queries gebasseerd op de Paper. 



