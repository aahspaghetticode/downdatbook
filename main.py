import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import aria2p
def fetchDownPage(url):
    html = fetchwithurl(url, s)
    soup = BeautifulSoup(html, "html.parser")

    links = []
    for li in soup.select("li.list-disc"):
        a = li.select_one("a.js-download-link")
        if a and MARKER in li.get_text():
            links.append(a["href"])
    return links
def search(q):
    q = f"https://annas-archive.pk/search?q={q}"
    html = fetchwithurl(q, s)
    title_a = soup.select_one("a.js-vim-focus[href^='/md5/']")
    if not title_a:
        return None
    href = title_a["href"]
    title = title_a.get_text(strip=True)
    author = ""
    node = title_a.parent
    while node is not None and node.name != "[document]":
        icon = node.select_one("span[class*='mdi--user-edit']")
        if icon and icon.parent:
            author = icon.parent.get_text(strip=True)
            break
        node = node.parent
    return "{title} {author}", "{BASE}{href}"
#idk i made claude make check bypass and then asked it to smash into function
def fetchwithurl(url, s=None, t=45):
    ch = lambda h: "/.well-known/ddos-guard/js-challenge" in h or "Checking your browser" in h
    if s and not ch(h := s.get(url).text): return h, s  # pre-done session still works -> plain fetch
    with sync_playwright() as p:
        b = p.chromium.launch(headless=False); c = b.new_context(); g = c.new_page(); g.goto(url)
        for _ in range(t):
            if not ch(h := g.content()): break
            g.wait_for_timeout(1000)
        else: b.close(); raise TimeoutError("challenge not cleared")
        s = s or requests.Session(); s.headers["User-Agent"] = g.evaluate("navigator.userAgent")
        [s.cookies.set(k["name"], k["value"], domain=k["domain"], path=k["path"]) for k in c.cookies()]
        h = g.content(); b.close(); return h
search(input("search and i download use isbn or name+title:"))
