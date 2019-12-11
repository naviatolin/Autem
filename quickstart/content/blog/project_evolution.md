---
title: "Project Evolution"
author: Maya and Navi 
image: images/blog/events.png
description : "Our changed events page"
---

For the most part, our project evolution has been linear. We would finish one task, then move on to the next. One of the areas where we really had to go back and change things was with the events and tasks page. Initially, we had a form on the events page using html form documentation, and requesting that information in routes.py. This worked perfectly well, until we had to implement tasks. The problem was simple - when \task would request information from the form, it would request from events, and not find what it needed. Similarly, \events wasn't routing properly anymore. So we pivoted to using wtf flask forms, which solved all our routing problems immediately. This gave us the ability to receive information from events and tasks, and schedule them accordingly, without mixing the two up. When it came time to implement survey, which had initially been a google form, we knew how to successfully transfer all of it to wtf forms. 



