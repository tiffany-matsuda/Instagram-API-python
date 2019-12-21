#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Use text editor to edit the script and type in valid Instagram username/password

from InstagramAPI import InstagramAPI, os
import time
from datetime import datetime

media_id = '1477006830906870775_19343908'

# stop conditions, the script will end when first of them will be true
until_date = '2020-03-31'
count = 100
userId = 36183292

API = InstagramAPI("tiffany_matsuda_test", "Qwer1234", False, os.path.dirname(os.path.abspath(__file__)))
API.login()
API.getUsernameInfo(26114367382)
has_more_comments = True
max_id = ''
comments = []

while has_more_comments:
    _ = API.getMediaComments(media_id, max_id=max_id)
    # comments' page come from older to newer, lets preserve desc order in full list
    for c in reversed(API.LastJson['comments']):
        comments.append(c)
    has_more_comments = API.LastJson.get('has_more_comments', False)
    # evaluate stop conditions
    if count and len(comments) >= count:
        comments = comments[:count]
        # stop loop
        has_more_comments = False
        print("stopped by count")
    if until_date:
        older_comment = comments[-1]
        dt = datetime.utcfromtimestamp(older_comment.get('created_at_utc', 0))
        # only check all records if the last is older than stop condition
        if dt.isoformat() <= until_date:
            # keep comments after until_date
            comments = [
                c
                for c in comments
                if datetime.utcfromtimestamp(c.get('created_at_utc', 0)) > until_date
            ]
            # stop loop
            has_more_comments = False
            print("stopped by until_date")
    # next page
    if has_more_comments:
        max_id = API.LastJson.get('next_max_id', '')
        time.sleep(2)
