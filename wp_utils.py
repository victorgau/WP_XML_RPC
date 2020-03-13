from wordpress_xmlrpc import Client
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, posts
from wordpress_xmlrpc import WordPressPost

# url = [wordpress網站的網址] + /xmlrpc.php
_url = ''
_username = ''
_password = ''

_client = Client(_url, _username, _password)

def upload_image(filename):
    try:
        # prepare metadata
        data = {
                'name': filename,
                'type': 'image/jpeg',  # mimetype
        }

        # read the binary file and let the XMLRPC library encode it into base64
        with open(filename, 'rb') as img:
                data['bits'] = xmlrpc_client.Binary(img.read())

        response = _client.call(media.UploadFile(data))
        return response
    except Exception as e:
        print(e.args)
        return None

def post_article(title, content, thumbnail_id = None, excerpt='', tags=[], categories=[], comment_status='open', post_status='publish'):
    article = WordPressPost()
    article.title = title
    article.content = content
    article.excerpt = excerpt
    article.terms_names = {
        "post_tag": tags,
        "category": categories
        }
    article.comment_status = comment_status
    if thumbnail_id:
        article.thumbnail = thumbnail_id
    article.post_status = post_status
    article.id = _client.call(posts.NewPost(article))
    return article.id


if __name__=="__main__":
    post_article('Test','This is a test!')