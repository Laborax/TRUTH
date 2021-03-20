def c(link):
    import requests 
    import pandas as pd 
    from bs4 import BeautifulSoup 
    import csv
    # link for extract html data 
    def getdata(url): 
        r = requests.get(url) 
        return r.text 

    htmldata = getdata(link) 
    soup = BeautifulSoup(htmldata, 'html.parser') 
    data = '' 
    fdata = ''
    hdata = ''
    for data in soup.find_all("p"): 
        fdata = fdata +" "+ data.get_text()
    for data in soup.find_all("h1"): 
        hdata = hdata +" "+ data.get_text()
    
    return fdata,hdata


#c("https://www.indiatoday.in/technology/news/story/disha-ravi-arrest-puts-privacy-of-all-google-india-users-in-doubt-1769772-2021-02-16")