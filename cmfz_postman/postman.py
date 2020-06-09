from cmfz_album.models import Chapter, Album
from cmfz_article.models import Article
from cmfz_carousel.models import Carousel


def album_default(u):
    if isinstance(u, Album):
        return {
            'thumbnail': str(u.img_src),
            'title': u.title,
            'author': u.author,
            'type': '0',
            'set_count': Chapter.objects.filter(album_id=u.id).count(),
            'create_data': u.publish_time.strftime("%Y-%m-%d %H:%M:%S")
        }


def article_default(u):
    if isinstance(u, Article):
        return {
            'thumbnail': '',
            'title': u.title,
            'author': u.author,
            'type': '1',
            'set_count': '',
            'create_data': u.publish_time.strftime("%Y-%m-%d %H:%M:%S")
        }


def carousel_default(u):
    if isinstance(u, Carousel):
        return {
            'thumbnail': str(u.img_url),
            'desc': u.title,
            'id': u.id
        }


def album_intro_default(u):
    if isinstance(u, Album):
        return {
            'thumbnail': str(u.img_src),
            'title': u.title,
            'score': u.score,
            'author': u.author,
            'broadcast': u.broadcast,
            'set_count': Chapter.objects.filter(album_id=u.id).count(),
            'brief': u.content,
            'create_date': u.publish_time.strftime("%Y-%m-%d %H:%M:%S")
        }


def album_chapter_default(u):
    if isinstance(u, Chapter):
        return {
            'title': u.title,
            'download_url': str(u.url),
            'size': str(u.size),
            'duration': u.time_long
        }
