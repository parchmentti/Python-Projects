I used this API to get 40-day weather forcasting data of over 3000 regions

The process of getting the data is easy, the difficult part is trying to make sure no data is missing
Because sometimes the simple get_page function cannot get the page and due to their engineers, the Interet fluctuations should take the blame.
So I added the robustness of the code by adding multiple iterations

### The procedure:
1. get_page: one url request returns 40-day weather forcasting data of one region
1. write_page: try to write the page into my database, and if previous step failed, return False  
1. pred_weather_40: iterate through all areas and return the areas that failed
1. func: iterate all failed areas until there is none
1. exe_every_day: set the time of day to run the process
1. let it run forever
1. Voila!
