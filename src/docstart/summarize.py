import os
import asyncio
from crawl4ai import AsyncWebCrawler
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from openai import OpenAI
from dotenv import load_dotenv
import typer
from typing_extensions import Annotated

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

#Initialize OpenAI Client. Use environment variable for API key.
#Input to get url for the documentation. 

#Site Object
class site():
    def __init__(self, mainURL, suburls, contents):
        self.mainURL = mainURL
        self.suburls = suburls
        self.contents = contents
    
    #Uses open AI to crawl through contents of a page and grab all urls relating to quickstart
    async def getSubUrls(mainURL, contents, api_key):
        client = OpenAI(api_key=api_key)
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
        
    #Uses crawl4ai to return the combined html of multiple pages of a site and returns it
    async def crawlFullSite(crawlURL, api_key):
        result = ""
        async with AsyncWebCrawler(verbose=True) as crawler:

            homePageResult = await crawler.arun(url=crawlURL)

        suburls = await site.getSubUrls(crawlURL, homePageResult.cleaned_html, api_key)
        subURLS = str(subURLS).split(",")
        
        async with AsyncWebCrawler(verbose=True) as crawler:
            for i in range(len(suburls)):
                result += (await crawler.arun(url=suburls[i])).cleaned_html


        return result

#Uses open AI to crawl through html file and return a quickstart guide in markdown format
def summarizeHTML(
        api_key: Annotated[str, typer.Argument(help="The OpenAI api key. This is set to the environment variable OPENAI_API_KEY by default")] = OPENAI_API_KEY,
        site_link: Annotated[str, typer.Argument(help="The url of the documentation site you would like to summarize")] = "",
    ):
    client = OpenAI(api_key=api_key)
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": """Analyze the html of a documentation site to create a markdown file that summarizes the main points about 
                what the code is used for and create a quick start guide. It should include example code and bullet points explaining the example code. 
                If the HTML does not look like html and instead says that the documentation was not found please output that text verbatim. 
                The HTML of the documentation site is """ + asyncio.run(site.crawlFullSite(site_link, api_key)) }
        ]
    )
    with open("quickstart.md", "w") as qs:
        qs.write(completion.choices[0].message.content)

#Takes the combined contents of all the markdown files provided and summarizes them into a quickstart page
def summarizeFileDocs(
        api_key: Annotated[str, typer.Argument(help="The OpenAI api key. This is set to the environment variable OPENAI_API_KEY by default")] = OPENAI_API_KEY,
        location: Annotated[str, typer.Argument(help="The location of the document for you wish to summarize. This should be the top level folder.")] = "",
    ):
    client = OpenAI(api_key=api_key)
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": """Analyze the markdown code of a documentation site to create a new markdown file that summarizes the main points about 
                what the code is used for and create a quick start guide. It should include example code and bullet points explaining the example code. 
                If the markdown of the files provided does not look like markdown please say the following verbatim \"Please enter a location that contains the 
                documentation code in markdown format. If you did and you believe this is an error please email luke.shehadeh@gmail.com.\" 
                The markdown code of the documentation is the following: \n""" + asyncio.run(getFileContents(location)) }
        ]
    )
    with open("quickstart.md", "w") as qs:
        qs.write(completion.choices[0].message.content)


#Combines all of markdown of the documentation pages provided to be summarized into a quickstart page
async def getFileContents(location):
    fileContents = ""
    for name in os.listdir(location):
        if name.lower().endswith(".md"):
            print(name)
            with open(os.path.join(location, name), "r", encoding="utf8") as f:
                fileContents += ("\n")
                fileContents += f.read()
    return fileContents
