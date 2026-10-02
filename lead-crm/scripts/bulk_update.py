from bs4 import BeautifulSoup
from collections import Counter
import re

CRM_FILE = '../crm.html'

def load(path=CRM_FILE):
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    html = re.sub(r'=""([^"]*?)""', r'="\1"', html)
    return BeautifulSoup(html, 'html.parser')

def save(soup, path=CRM_FILE):
    html = str(soup)
    html = re.sub(r'=""([^"]*?)""', r'="\1"', html)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)

def get_tbodies(soup):
    tbodies = soup.find_all('tbody')
    ytc = tbodies[2]
    noans = tbodies[3]
    dead = tbodies[5]
    # Find the main warm tbody by locating the one with the most warm-row elements
    all_warm = soup.find_all('tr', class_='warm-row')
    counts = Counter(id(tr.parent) for tr in all_warm)
    warm = next(tr.parent for tr in all_warm if id(tr.parent) == counts.most_common(1)[0][0])
    return ytc, warm, noans, dead

def update_stats(soup, ytc_n, warm_n, noans_n):
    for div in soup.find_all('div', class_='stat-num'):
        sib = div.find_next_sibling('div', class_='stat-label')
        if not sib:
            continue
        text = sib.get_text()
        if 'Yet To Call' in text:
            div.string = str(ytc_n)
        elif 'No Answer' in text:
            div.string = str(noans_n)
        elif 'Warm' in text:
            div.string = str(warm_n)
    for btn in soup.find_all('button'):
        t = btn.get_text()
        if 'Yet To Call' in t:
            btn.string = f'📞 Yet To Call ({ytc_n})'
        elif 'No Answer' in t:
            btn.string = f'📵 No Answer ({noans_n})'
        elif 'Warm' in t and 'Yet' not in t:
            btn.string = f'⭐ Warm ({warm_n})'
