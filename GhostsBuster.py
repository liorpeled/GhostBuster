import requests
from requests_html import HTMLSession
from urllib.request import urlparse, urljoin, urlopen
from bs4 import BeautifulSoup
import numpy as np
import colorama

# init the colorama module
colorama.init()
invalidLink = []
visited = []
pathFlow = []
invalid = []


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
        invalidLink.append(url)
        pathFlow.append(url)
        # print("printing path flow from within is_valid*************************************************************")
        # print(pathFlow)
        # invalid.append(pathFlow)
        # pathFlow.clear()
        # print("the last link is not valid!")
        # print(invalid)
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
            elif (len(link.findAll("img")) > 0):
                img = link.findAll("img")[0]
                text = "https:" + img.attrs.get("src")

        href = link.attrs.get("href")
        if href == "" or href is None:
            invalidLink.append(text)
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
        connector = "/hc/en-us"
        correct_path = [path for path in temp if connector in path]
        if(len(correct_path) > 1 and connector in correct_path[-1]):
            temp[0] = correct_path[0].split('/hc/en-us')[0]

        href = ''.join(temp)

        # need to check if link is an img
        item = (text, href)
        if(".html" in href or ".png" in href or "fyber" not in href):
            continue
        if(url not in visited and is_valid(url)):
            visited.append(url)
            # print("printing path flow")
            pathFlow.append(url)
            # print(pathFlow)
        if(href not in visited and href not in urls and is_valid(href)):
            urls.append(href)

    return urls


def crawl(url, max_urls=30):
    """
    Crawls a web page and extracts all links.
    You'll find all links in `external_urls` and `internal_urls` global set variables.
    params:
        max_urls (int): number of max urls to crawl, default is 30.
    """
    # pathFlow.append(url)
    print("currently running url")
    print(url)
    print("\n")
    links = get_all_links_in_webpage(url)
    print("visied before and this page")
    print(visited)
    print("\n")
    print("printing links found in current page")
    print(links)
    print("\n")
    # print("invalid links")
    # print(invalidLink)

    for index, link in enumerate(links):
        # print("printing url to crawl next")
        # print(link)
        # print(index)
        print("printing the number of visited urls")
        print(str(len(visited)))
        print("********************************"+"\n\n")
        if len(visited) > max_urls:
            print("invalid links")
            # print(invalidLink)
            npa = np.asarray(invalidLink)
            print(npa)
            exit()  # will continue another time
        crawl(link, max_urls=max_urls)


if __name__ == "__main__":
    links = []
    links = crawl(
        "https://developer.fyber.com/hc/en-us")

    # print(is_valid("https://developer.fyber.com/hc/en-us/articles/360009975338-Fyber-FairBid/subscription.html"))
    # links = get_all_links_in_webpage(
    # "https://developer.fyber.com/hc/en-us/sections/360002865578-Setting-Up-FairBid")
    for link in links:
        # print(link)
        break
