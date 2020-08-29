#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 10:57:36 2020

@author: kristinquality
"""

import pandas as pd
import json
import requests
import threading
from datetime import datetime, date, time, timezone

RAPIDAPI_KEY = ""
max_thread_nums = 4

def my_key(api_key):
    """
    Put into your own api_key

    Parameters
    ----------
    api_key : string

    Returns
    -------
    None.

    """
    global RAPIDAPI_KEY
    RAPIDAPI_KEY = api_key

def trigger_api(info, org_or_people):
    """
    a function for triggering Crunchbase API

    Parameters
    ----------
    info : dict
        the information we want to know
    org_or_people : bool
        true if orgnizations, false if people

    Returns
    -------
    json object

    """
    headers = {'x-rapidapi-host': "crunchbase-crunchbase-v1.p.rapidapi.com",
               'x-rapidapi-key': RAPIDAPI_KEY}
    if org_or_people:
        last = 'organizations'
    else:
        last = 'people'
    url = "https://crunchbase-crunchbase-v1.p.rapidapi.com/odm-" + last
    response = requests.request("GET", url, headers=headers, params=info)
    if(200 == response.status_code):
        return json.loads(response.text)
    else:
        return None

def make_df(info, org_or_people):
    """
    to make the json object be a pd.DataFrame

    Parameters
    ----------
    info : dict
        the information we want to know
    org_or_people : bool
        true if orgnizations, false if people

    Returns
    -------
    data : pd.DataFrame
        the final result of the information we want to know

    """
    raw_data = trigger_api(info, org_or_people)
    page_nums = raw_data['data']['paging']['number_of_pages']
    page_cur = raw_data['data']['paging']['current_page']
    try:
        data = pd.DataFrame(list(pd.DataFrame(raw_data['data']['items'])['properties']))
    except Exception as e:
        print(e)
        return
    # if there are many pages, use multi threading
    if page_nums > 0 and page_cur == 1:
        thread_nums = min(page_nums - 1, max_thread_nums)
        threads = [None] * thread_nums
        pages = [None] * thread_nums
        
        def more_pages(df, index, org_or_people, more_pages_nums=page_nums):
            if more_pages_nums - 1 <= max_thread_nums:
                
                info_page = {**info, 'page': index+2}
                datanew = pd.DataFrame(list(pd.DataFrame(trigger_api(info_page, org_or_people)['data']['items'])['properties']))
                df[index] = datanew
            else:
                nums = more_pages_nums // max_thread_nums
                info_page = {**info, 'page': 2+index*nums}
                df[index] = pd.DataFrame(list(pd.DataFrame(trigger_api(info_page, org_or_people)['data']['items'])['properties']))
                for i in range(2+index*nums+1, 2+index*nums+nums):
                    info_page = {**info, 'page': i}
                    datanew = pd.DataFrame(list(pd.DataFrame(trigger_api(info_page, org_or_people)['data']['items'])['properties']))
                    df[index] = df[index].append(datanew).reset_index(drop=True)
                if index == 3:
                    for i in range(2+3*nums+nums, more_pages_nums+1):
                        info_page = {**info, 'page': i}
                        datanew = pd.DataFrame(list(pd.DataFrame(trigger_api(info_page, org_or_people)['data']['items'])['properties']))
                        df[index] = df[index].append(datanew).reset_index(drop=True)

        for i in range(thread_nums):
            threads[i] = threading.Thread(target=more_pages, args=(pages, i, org_or_people))
            threads[i].start()
        for j in range(thread_nums):
            threads[j].join()
            data = data.append(pages[j])
    return data

def orgs_data(info):
    """
    a function to return the results of orgnizations

    Parameters
    ----------
    **kwargs : dict
        the information we want to know

    Returns
    -------
    pd.DataFrame
        the final result of the information we want to know

    """
    return make_df(info, True)

def people_data(info):
    """
    a function to return the results of people

    Parameters
    ----------
    **kwargs : dict
        the information we want to know

    Returns
    -------
    pd.DataFrame
        the final result of the information we want to know

    """
    return make_df(info, False)


def modify_time(year, month, day, time_zone=timezone.utc):
    """
    modify input time to a timestamp first if we want to put it into info

    Parameters
    ----------
    year : int
    month : int
    day : int
    time_zone : TYPE, optional
        DESCRIPTION. The default is timezone.utc.

    Returns
    -------
    input_timestamp_utc : timestamp
        the timestamp of the input time

    """
    input_time = datetime(year=year, month=month, day=day)
    input_timestamp_utc = int(input_time.replace(tzinfo=time_zone).timestamp())
    return input_timestamp_utc



