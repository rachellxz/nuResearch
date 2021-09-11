### NEED TO RUN IN TERMINAL: pip install feedparser ###
#=====================================================#
import feedparser
import pandas as pd

catalog_path = './assets/catalog.csv' # ADJUST TO DIRECT ASSET DIR

### Helper methods
def get_catalog():
    return pd.read_csv(catalog_path)

def get_channels():
    return list(get_catalog().channel)
    
def get_genres():
    # always 'Medicine', 'Science', 'Life', 'Seasonal', 'Business'
    return list(get_catalog().genre.drop_duplicates())

def get_channel_link(channel):
    df = get_catalog()
    return df[df.channel == channel].url.values[0]

### Function to get top_n research news from a channel (topic)
def get_news(channel, top_n = 20):
    feed = feedparser.parse(get_channel_link(channel))
    num_paper = len(feed.entries)
    # real schema (title, summary, author, published, link, image)
    schema = ['title', 'summary', 'author', 'published', 'link']
    df = pd.DataFrame(list(feed.values())[1])[schema]

    df['image'] = ['' for _ in range(20)]

    for index, row in df.iterrows():
        parts = row['summary'].split('" />')
        row['summary'] = parts[-1]
        row['image'] = parts[0].split('src="')[1] if len(parts) == 2 else ''
    
    return df.head(top_n)

if __name__ == "__main__":
    # get all channels / topics of research (e.g., "Addiction")
    get_channels()
    
    # get the 20 (default) most recent research news in the topic of "Addiction"
    get_news('Addiction')
    
    # get the 5 most recent research news in the topic of "Addiction"
    get_news('Mathematics', 5)
