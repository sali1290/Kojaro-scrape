import requests
from bs4 import BeautifulSoup
from newspaper import Article
from tqdm import tqdm
import pandas

def crawl (): 
    data = []
    urlList = []
    page = 2041 # step 1

    while True: # step 2
        page = page + 1
        main_url = f"https://www.kojaro.com/page/{page}/"
        html = requests.get(main_url).text
        soup = BeautifulSoup(html, features="lxml")

        links = soup.find_all("h3", {"class": "mrg0B dis-block topicTitle"})

        if repetitive(links , urlList): # step 3
              break

        for link in tqdm(links): # step 4
                sub_url = link.a['href']
                urlList.append(link.a["href"])
                try:
                    article = Article(sub_url)
                    article.download()
                    article.parse()
                    data.append({"url": sub_url, "text": article.text, "title": article.title})
                except:
                    print(f"Failed to load {sub_url}")
    
    df = pandas.DataFrame(data) # step 5
    df.to_csv(f"kojaro crawled.csv")

def repetitive (links, urls):
    for link in links:
        if link.a["href"] in urls:
            return True
    return False


crawl()