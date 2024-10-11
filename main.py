import os
import json
import asyncio
from crawl4ai import AsyncWebCrawler
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from openai import OpenAI

#Initialize OpenAI Client. Use environment variable for API key.
client = OpenAI(api_key=OPENAI_API_KEY)
#Input to get url for the documentation. 
#TO-DO: Allow for readme file input.
crawlURL = input("Enter Documentation Site: ")
fileName = input("Enter name of file you would like to save the quickstart to, it should end in .md")

#Site Object
class site():
    def __init__(self, mainURL, suburls, contents, fullHTML):
        self.mainURL = mainURL
        self.suburls = suburls
        self.contents = contents
        self.fullHTML = fullHTML
    
    #Uses open AI to crawl through contents of a page and grab all urls relating to quickstart
    async def getSubUrls(mainURL, contents):
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": """Extract all urls on this page of html that lead to another main page of the documentation.  
                 The goal is to grab all urls that may lead to something that can help create a quickstart guide. It shouldn\'t be more than 10 url\'s total. 
                 Examples of pages that are important are quickstart guides, introduction pages, installation pages, home pages, and any pages that may include 
                 important legal information. Extract just the urls and put a comma between them with no spaces. The urls will be in href form in the html. 
                 In order to convert them to full url form you have to add them to the base url, """ + mainURL + 
                 """ if the href has a .. in front of it that means that you have to go back one page, so delete the last page in the url, 
                 it will look like this /examplepage/, and then add the href onto the url. If the html doesn't seem like the home page of documentation site 
                 please output \"Documentation was not found :(. Please enter a url of the home page of a documentation site. 
                 If you did and you believe this is an error, please email luke.shehadeh@gmail.com.\". The html is: \n""" +  contents}
            ]
        )
        return(completion.choices[0].message.content)
        
    #Uses open AI to crawl through html file and return a quickstart guide in markdown format
    async def summarizeToQuickStart(fullHTML):
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": """Analyze the html of a documentation site to create markdown code that summarizes the main points about 
                 what the code is used for and create a quick start guide. It should include example code and bullet points explaining the example code. 
                 If the HTML does not look like html and instead says that the documentation was not found please output that text verbatim. 
                 The HTML of the documentation site is """ + fullHTML }
            ]
        )
        return(completion.choices[0].message.content)

    #Uses crawl4ai to return the combined html of multiple pages of a site and saves that to a text file.
    async def crawlFullSite(suburls):
        async with AsyncWebCrawler(verbose=True) as crawler:

            for i in range(len(suburls)):
                result = await crawler.arun(url=suburls[i])

                with open("FullHTML.txt", "a", encoding="utf-8") as resultFile:
                    resultFile.write(result.html)

async def main():

    #Crawl through the main url and return the homepage
    async with AsyncWebCrawler(verbose=True) as crawler:

        homePageResult = await crawler.arun(url=crawlURL)

    #Get suburls from the homepage
    subURLS = await site.getSubUrls(crawlURL, homePageResult.html)
    subURLS = str(subURLS).split(",")
    
    #Create an text file containing the full html of the site
    await site.crawlFullSite(subURLS)

    fullHTML = open("FullHTML.txt", "r", encoding="utf=8")
    quickstart = open(fileName, "w", encoding="utf=8")

    quickstartContents = await site.summarizeToQuickStart(fullHTML.read())
    quickstartContents = str(quickstartContents)

    quickstart.write(quickstartContents)

    quickstart.close()
asyncio.run(main())