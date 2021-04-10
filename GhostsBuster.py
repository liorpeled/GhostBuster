import requests
from urllib.request import urlparse, urljoin, urlopen
from bs4 import BeautifulSoup
import colorama

# init the colorama module
colorama.init()
invalidUrl = []


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

    domain_name = urlparse(url).netloc
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    for link in soup.findAll("a"):
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
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        item = (text, href)
        urls.append(item)
    return urls


def search(vals):
    for i in vals.values():
        newLinks = get_all_links_in_webpage(i[1])
    return newLinks


if __name__ == "__main__":
    links_in_page = get_all_links_in_webpage(
        "https://developer.fyber.com/hc/en-us")
    print(links_in_page)
