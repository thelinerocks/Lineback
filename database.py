from peewee import *
import datetime
import sys

db = SqliteDatabase('data/tagged_posts.db')

class TaggedPost(Model):
    date = DateTimeField(default=datetime.datetime.utcnow())
    social_network = CharField()
    user_name = CharField(default='unknown_user')
    message = TextField()
    profile_pic_url = CharField(null=True)
    image_url = CharField(null=True)
    location = CharField(null=True)
    text_sentiment = DecimalField(null=True)
    image_emotion = DecimalField(null=True)
    json_data = TextField(null=True)
    category = CharField(null=True)
    analysed = BooleanField(default=False)

    class Meta:
        database = db

def save_post(info_dict):
    if db.is_closed():
        db.connect()
    new_post = TaggedPost(**info_dict)
    if "date" not in info_dict:
        new_post.date = datetime.datetime.utcnow()
    new_post.save()
    db.close()

def read_next_post():
    if db.is_closed():
        db.connect()
    try:
        post = TaggedPost.get(TaggedPost.analysed == False)
    except DoesNotExist:
        return None
    except Exception as e:
        print(e)
        pass
    db.close()
    return post

def read_next_n_posts(num):
    if db.is_closed():
        db.connect()
    try:
        posts = TaggedPost.select(TaggedPost.analysed == False).limit(num)
    except:
        pass
    db.close()
    return posts

def get_most_recent(social_network):
    if db.is_closed():
        db.connect()
    recent = None
    try:
        recent = TaggedPost.select().order_by(TaggedPost.date.desc()).get()
    except DoesNotExist:
        return None
    except Exception as e:
        print(e)
    db.close()
    return recent.date

def get_sum_text(category):
    back_to = datetime.datetime.utcnow() - datetime.timedelta(hours=1)
    return TaggedPost.select(fn.sum(TaggedPost.text_sentiment)).where((TaggedPost.category==category) & (TaggedPost.date > back_to)).scalar() or 0

def get_sum_image(category):
    back_to = datetime.datetime.utcnow() - datetime.timedelta(hours=1)
    return TaggedPost.select(fn.sum(TaggedPost.image_emotion)).where((TaggedPost.category==category) & (TaggedPost.date > back_to)).scalar() or 0

def get_mention(category, last_id):
    x = None
    if db.is_closed():
        db.connect()
    try:
        x = TaggedPost.select().where((TaggedPost.category==category) & (TaggedPost.id > last_id)).order_by(TaggedPost.id.desc()).get()
    except DoesNotExist:
        return None
    except Exception as e:
        print(e)
    db.close()
    return x

if __name__=="__main__":
    if sys.argv[1] == "create":
        db.create_tables([TaggedPost])
        db.close()
