from peewee import *

db = SqliteDatabase('data/tagged_posts.db')

class TaggedPost(Model):
    #time_stamp = TimestampField()
    social_network = CharField()
    user_name = CharField()
    message = TextField()
    profile_pic_url = CharField()
    image_url = CharField()
    location = CharField(null=True)
    text_sentiment = DecimalField(null=True)
    image_emotion = CharField(null=True)
    json_data = TextField(null=True)
    category = CharField(null=True)
    analysed = BooleanField(default=False)

    class Meta:
        database = db


if not TaggedPost.table_exists():
    db.create_tables([TaggedPost])
    db.close()

def save_post(info_dict):
    if not db.is_closed():
        db.connect()
    db.connect()
    new_post = TaggedPost(**info_dict)
    new_post.save()
    db.close()

def read_next_post():
    if db.is_closed():
        db.connect()
    try:
        post = TaggedPost.get(TaggedPost.analysed == False)
    except:
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
