#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   pyGenTree.py
@Time    :   2024-10-05 00:06:20
@Author  :   Alberto Donazzan 
@Desc    :   None
'''
#%% ----------------------------------------------------------- INITIALIZE --- #
import sys, os
# change working folder to the position of THIS .py file
thisDirPath = os.path.abspath(os.path.dirname(__file__))
os.chdir(thisDirPath)

import numpy as np
import random
from datetime import datetime
import matplotlib as mpl
mpl.use('Qt5Agg')           # graphics backend (ex. TkAgg, Qt5Agg), shows figures in separate windows
import matplotlib.pyplot as plt
plt.ion()                   # interactive mode ON: show plot changes immediately
import addcopyfighandler    # requires: pip install addcopyfighandler
import pandas as pd
pd.set_option('display.max_rows', None, 'display.max_columns', None, 'display.width', 200)

#%%

def dateParser(date):
    for fmt in ('%Y-%m-%d', '%d.%m.%Y', '%d/%m/%Y', '%Y-%m', '%m.%Y', '%m/%Y', '%Y'):
        try:
            return datetime.strptime(date, fmt), fmt
        except ValueError:
            pass
    raise ValueError('no valid date format found')

class Person:
    """This class represents a person.
	"""

    def __init__(self, parents=[None, None],
                 name=None, surname=None, nickname=None, sex=None,
                 birthDate=None, birthDetails=None, birthPlus=None,
                 deathDate=None, deathDetails=None, deathPlus=None,
                 work=None, workDetails=None, 
                 comment=None):
        
        self.parents      = parents
        self.name         = name
        self.surname      = surname
        self.nickname     = nickname
        self.sex          = sex
        
        self.birthDate    = birthDate
        self.birthDetails = birthDetails
        self.birthPlus    = birthPlus
        self.deathDate    = deathDate
        self.deathDetails = deathDetails
        self.deathPlus    = deathPlus
        
        self.work         = work
        self.workDetails  = workDetails
        self.comment      = comment
        
        # Compute Age
        if birthDate:
            startAge, startFormat = dateParser(birthDate)
            if deathDate:
                endAge, endFormat = dateParser(deathDate)
            else:
                endAge, endFormat = datetime.now(), 'Ymd'
            deltaYears = endAge.year-startAge.year
            if 'd' in startFormat and 'd' in endFormat:
                deltaMonths = endAge.month-startAge.month
                deltaDays = endAge.day-startAge.day
                self.age = str(int(deltaYears + deltaMonths/12 + deltaDays/365))
            elif 'm' in startFormat and 'm' in endFormat:
                deltaMonths = endAge.month-startAge.month
                if deltaMonths<0:
                    self.age = str(deltaYears-1)
                elif deltaMonths>0:
                    self.age = str(deltaYears)
                else:
                    self.age = f'{deltaYears-1}-{deltaYears}'
            else:
                self.age = f'{deltaYears-1}-{deltaYears}'
        else:
            self.age = None

        # Build Person ID (fill with random if data are missing)
        if not name:
            name = '.na'+''.join(chr(random.randrange(65,90)) for i in range(6))+'.'
        if not surname:
            surname = '.na'+''.join(chr(random.randrange(65,90)) for i in range(6))+'.'
        if not birthDate:
            birthDate = '.na'+str(random.randint(100000, 999999))+'.'
        self.id = surname+name+birthDate
        
        
    def __str__(self):
        return self.id
    
    def printLaTeX(self):
        
        # Convert object content into printable content
        sex = self.sex+',' if self.sex else ''
        name = self.name if self.name else '?'
        surname = f'\surn{{{self.surname}}}' if self.surname else '\surn{?}'
        nickname = f'\\nick{{{self.nickname}}} ' if self.nickname else ''
        ageInBirth = f' [{self.age}]' if (self.age and not self.deathDate) else ''
        birthVar = 'birth+' if self.birthPlus else 'birth'
        birthDate = f'{{{self.birthDate}{ageInBirth}}}' if self.birthDate else '{?}'
        birthDetails = f'{{{self.birthDetails}}}' if self.birthDetails else '{?}'
        birthPlus = f'{{{self.birthPlus}}}' if self.birthPlus else ''
        ageInDeath = f' [{self.age}]' if (self.age and self.deathDate) else ''
        deathVar = 'death+' if self.deathPlus else 'death'
        deathDate = f'{{{self.deathDate}{ageInDeath}}}' if self.deathDate else '{?}'
        deathDetails = f'{{{self.deathDetails}}}' if self.deathDetails else '{?}'
        deathPlus = f'{{{self.deathPlus}}}' if self.deathPlus else ''
        
        # Print LaTeX code
        p = sex + '\n'
        p+= 'name = {' + name + ' ' + nickname + surname + '}\n'
        p+= birthVar + ' = ' + birthDate + birthDetails + birthPlus + '\n'
        p+= deathVar + ' = ' + deathDate + deathDetails + deathPlus + '\n'
        return p
    
# child[id=donazzanSebastianoFam]{
#     g{male, 
#         name = {Sebastiano \surn{Donazzan}},
#         birth = {1884-06-19}{\pove, \\ 
#             \hfill contrada Piazza 200, ore 16.00 \\
#             \hfill \register{Pove}{Nascite 1884}{I}{30} % Reg. Pove, Nascite 1884, I #30
#         }, 
#         marriage = {1913-03-02}{\pove, ore 10.50 \\
#             \hfill \register{Pove}{Matrimoni 1913}{}{6} % Reg. Pove, Matrimoni 1902, I #3
#         }, 
#         death = {1952-09-17}{\pove},
#         profession = {\work{Tagliapietra}},
#         comment = {Alla morte ha ceduto i seguenti immobili: \\
#             Pove, sez.U, f.10, mapp.771-152, campo \\
#             Pove, sez.U, f.10, mapp.153, casa con porzione corte n.1229, 
#             2piani, 2vani, via Fusari. \\
#             \hfill \register{Pove}{Successioni 1952}{Vol.249}{54} % Indice Successioni, Vol.249 #54
#         },
#     }




        
# %%
    
gianni = Person(parents=[None, None],
                name='Gianni', surname='Armani', nickname='Capusso', sex='male',
                birthDate='2000', birthDetails=None, birthPlus=None,
                deathDate='3/03/2100', deathDetails=None, deathPlus=None,
                work=None, workDetails=None, 
                comment=None)
carlo = Person(parents=[None, None],
                name=None, surname=None, nickname=None, sex='male',
                birthDate='1971', birthDetails=None, birthPlus=None,
                deathDate='1981', deathDetails=None, deathPlus=None,
                work=None, workDetails=None, 
                comment=None)

print(gianni.printLaTeX())
print(carlo.printLaTeX())
# %%
