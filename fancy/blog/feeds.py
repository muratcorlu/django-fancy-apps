from django.contrib.syndication.views import Feed
from models import Post
import markdown
import settings

class LatestEntriesFeed(Feed):
    title = settings.FEED_TITLE
    link = settings.FEED_LINK
    description = settings.FEED_DESCRIPTION

    def items(self):
        return Post.objects.order_by('-date')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return markdown.markdown(item.content)