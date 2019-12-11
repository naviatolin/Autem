---
title: "Algorithm"
author: Maya and Navi 
image: images/blog/calender.png
description : "calendar working"
---

When you input a task in Autem, you're telling us four things - what you're calling the task (a summary), when it's due, how long you think it'll take, and how stressed you are about it. The first thing we do is save all that information in a dictionary in a .json file, which we then sort by due date. This allows us to prioritize the tasks that are due sooner when scheduling. Then, we break the task up into "chunks". Each chunk is one hour of uninterrupted work. If you have a task with 8 hours of work, then it's now 8 chunks of one hour work time. We then calculate how many days you have to work on this assignment, and divide the chunks equally amongst those days. If, say, you have 4 days to do those 8 hours of work, then we know you have to work 2 chunks per day to finish on time. 

The next thing we do is pull the events from your google calendar during the time you have to do your task. We do this so we know when you are actually free to work on your task. The day starts at your preferred start time to be (9 am for example) and ends at your preferred end time (5 pm). So we then look from 9:00 to 10:00  to see if you have anything scheduled. If you do, then we shift over to 9:15 to 10:15, and do the same thing. We continue to search every 15 minutes until we find a free hour. When we do, we schedule in your first chunk, then continue for as many chunks as we have for this specific day.



