#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 22:18:41 2020

@author: kristinquality
"""

import cbapi
import pandas as pd

RAPIDAPI_KEY  = '52e2eb1c7emsh4d7924f747e446bp1cb4a3jsnc7ed32c3feef'

def mytest():
    cbapi.my_key(RAPIDAPI_KEY)
    test_org = cbapi.orgs_data({'name': 'capital management', 'locations': 'New York'})
    test_people = cbapi.people_data({'name': 'Joe', 'updated_since': cbapi.modify_time(2019, 12, 13)})
    
    assert isinstance(test_org, pd.DataFrame)    
    assert isinstance(test_people, pd.DataFrame)
    
    print("ok")

    
if __name__ == '__main__':
    mytest()
