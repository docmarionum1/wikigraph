import pywikibot as pwb
import pandas as pd
import networkx as nx

langs = [
    ('en', 'English'), 
    ('de', 'German'),
    ('es', 'Spanish'),
    ('fr', 'French'),
    ('ja', 'Japanese'),
    ('ru', 'Russian'),
    ('it', 'Italian'),
    ('pt', 'Portuguese'),
    ('zh', 'Chinese'),
    ('nl', 'Dutch'),
    ('pl', 'Polish'),
    ('ar', 'Arabic'),
    ('tr', 'Turkish'),
    ('sv', 'Swedish'),
    ('ko', 'Korean'),
    ('fa', 'Persian'),
    ('uk', 'Ukrainian'),
    ('he', 'Hebrew'),
    ('id', 'Indonesian'),
    ('cs', 'Czech'),
]

lang_codes = [i[0] for i in langs]

cities = [
    u'Shanghai',
    u'Karachi',
    u'Lagos',
    u'Delhi',
    u'Istanbul',
    u'Tokyo',
    u'Tianjin',
    u'Guangzhou',
    u'Mumbai',
    u'Moscow',
    u'São Paulo',
    u'Beijing',
    u'Shenzhen',
    u'Seoul',
    u'Jakarta',
    u'Lahore',
    u'Kinshasa',
    u'Cairo',
    u'Mexico City',
    u'Lima',
    u'New York City',
    u'Bangalore',
    u'London',
    u'Bangkok',
    u'Dongguan',
    u'Chongqing',
    u'Nanjing',
    u'Tehran',
    u'Shenyang',
    u'Bogotá',
    u'Ho Chi Minh City',
    u'Ningbo',
    u'Hong Kong',
    u'Baghdad',
    u'Changsha',
    u'Dhaka',
    u'Wuhan',
    u'Hyderabad',
    u'Hanoi',
    u'Faisalabad',
    u'Rio de Janeiro',
    u'Foshan',
    u'Santiago',
    u'Riyadh',
    u'Ahmedabad',
    u'Singapore',
    u'Shantou',
    u'Yangon',
    u'Saint Petersburg',
    u'Ankara'
]

# Queue to process pages
# Keep tuples of (title,depth)
# Where depth is the current depth, don't go past depth
queue = []
queued = {}

def scrapeCity(graph,lang,city,cities,max_depth=3):
    if max_depth < 1:
        return
    
    site = pwb.Site(lang, 'wikipedia')
    
    queue.append((pwb.Page(site, city),0))
    queued[city] = None
    
    while queue:
        page, depth = queue.pop()
        title = page.title()
        
        #if depth < max_depth:
        for p in page.linkedPages():
            t = p.title()

            graph.add_edge(title,t)

            # If we haven't queued/processed the page yet
            # And it isn't one of the cities.
            if t not in queued and t not in cities:
                if depth < (max_depth - 1):
                    queued[t] = None
                    queue.append((pwb.Page(site,t), depth+1))

en = nx.DiGraph()
    
scrapeCity(en, 'en', 'New York City', cities, max_depth=2)
print len(en), en.size()
nx.write_gpickle(en,'en.pickle')