from bs4 import BeautifulSoup as bs4
import requests #library for making http request in Python
import pandas as pd #for creating dataframes and easy coverting to excel file, csv, other formats

pages=[]
prices=[]
stars=[]
titles=[]
urlss=[]

pages_to_scrape=5

for i in range(1,pages_to_scrape+1):    #for lopping till the given page number
    url = ('http://books.toscrape.com/catalogue/page-{}.html').format(i) #url with page number
    pages.append(url) #appending url with page number to pages list
for item in pages:
    page = requests.get(item)
    soup = bs4(page.text, 'html.parser')
    for i in soup.findAll('h3'):   #find returns the first matching element instead of a list
        ttl=i.getText()
        titles.append(ttl)
    for j in soup.findAll('p', class_='price_color'):
        price=j.getText()
        prices.append(price)
    for s in soup.findAll('p', class_='star-rating'):
        for k,v in s.attrs.items():     #the s here acts as dict we check with print statement
            star =v[1]  #getting the second value as second value is the rating
            stars.append(star)
    divs =soup.findAll('div', class_='image_container')  #finding all the image_container inside div tag
    for thumbs in divs:
        tgs=thumbs.find('img',class_='thumbnail')         #finding thumbnail class inside img tag, always use class_ for findings
        urls='http://books.toscrape.com/'+str(tgs['src']) #merge tgs with site id to get complete url of image, use strings to join
        newurls=urls.replace("../","")                    #replace .. to get actual and correct url
        urlss.append(newurls)
data={'Title': titles, 'Prices': prices, 'Stars':stars, "URLs":urlss} #get all the list in dict 
df=pd.DataFrame(data=data)                    #convert to dataframe using pandas
df.index+=1                                   #incerement index to start the indexing with 1
df.to_excel("~/Desktop/tutorials/BookStoreWS/output.xlsx")           #convert dataframe to excel
