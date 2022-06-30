import LinkedIn_Scraper
import display_list
import time

LinkedIn_Scraper.linkedin_main("Software Engineering", 50) #Parameters are (Job name, Number of jobs to gather), these will be expanded soon to be more customizable
LinkedIn_Scraper.htmlformatter()
display_list.displaylist()