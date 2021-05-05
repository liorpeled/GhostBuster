import requests
from requests_html import HTMLSession
from urllib.request import urlparse, urljoin, urlopen
from bs4 import BeautifulSoup
import colorama

# init the colorama module
colorama.init()
invalidUrl = []
visited = []


def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    OK = False
    try:
        if urlopen(url).getcode() == 200:
            OK = True
    except:
        OK = False
        invalidUrl.append(url)
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme) and OK


def get_all_links_in_webpage(url):
    urls = []
    # domain name of the URL without the protocol
    domain_name = urlparse(url).netloc
    # initialize an HTTP session
    session = HTMLSession()
    # make HTTP request & retrieve response
    response = session.get(url)
    # execute Javascript
    try:
        response.html.render()
    except:
        pass
    soup = BeautifulSoup(response.html.html, "html.parser")
    for link in soup.findAll("a"):
        if(len(link.findAll(text=True)) > 0):
            if link.findAll(text=True)[0] != '\n':
                text = link.findAll(text=True)[0]
            else:
                img = link.findAll("img")[0]
                text = "https:" + img.attrs.get("src")

        href = link.attrs.get("href")
        if href == "" or href is None:
            # href empty tag
            continue
        # join the URL if it's relative (not absolute link)
        href = urljoin(url, href)
        parsed_href = urlparse(href)

        # remove URL GET parameters, URL fragments, etc.
        if(str(parsed_href.netloc) == "fyberhelp.zendesk.com"):
            home = "developer.fyber.com"
        else:
            home = parsed_href.netloc
        href = parsed_href.scheme + "://" + home + parsed_href.path
        temp = href.split()
        href = ''.join(href.split())
        print(href)
        #print(text + " / " + href)
        # need to check if link is an img
        item = (text, href)

        if(url not in visited):
            visited.append(url)
        if(href not in visited):
            urls.append(href)

    return urls


def crawl(url, max_urls=50):
    """
    Crawls a web page and extracts all links.
    You'll find all links in `external_urls` and `internal_urls` global set variables.
    params:
        max_urls (int): number of max urls to crawl, default is 30.
    """
    print(url)
    links = get_all_links_in_webpage(url)
    print("inital visited")
    print(visited)
    print("printing links")
    print(links)
    for link in links:
        print("printing url to crawl")
        print(link)
        print("printing the number of visited urls")
        print(len(visited))
        if len(visited) > max_urls:
            break
        crawl(link, max_urls=max_urls)


if __name__ == "__main__":
    links = []
    links = crawl(
        "https://developer.fyber.com/hc/en-us")

    # links = get_all_links_in_webpage(
    #  "https://developer.fyber.com/hc/en-us")
    for link in links:
        # print(link)
        break
