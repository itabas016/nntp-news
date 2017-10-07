## NNTP News Agent ##

_*First, nntp news is base on nntp(Network News Transfer Protocol), the details please see [wiki](https://en.wikipedia.org/wiki/Network_News_Transfer_Protocol), you can search free nntp source from website [free usenet news](https://www.freeusenetnews.com/)*_

### Sample ###

This sample list week's python announce news from [aioe](news://news.aioe.org)

> output **->** [index](sample/index.html)

### BBC News ###

Currently, bbc nntp server is invaild, using [API](https://newsapi.org) to show the topest bbc news.

```python
agent = NewsAgent()

bbc_news_url = 'https://newsapi.org/v1/articles?source=bbc-news&sortBy=top&apiKey={your-api-key}'
bbc_news = APIJsonSoucre(bbc_news_url)

agent.addSource(bbc_news)
agent.addDestination(HTMLDestination2('news.html'))

agent.distribute()
```

> output **->** [news](news.html)
