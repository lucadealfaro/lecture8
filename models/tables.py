from datetime import datetime

def get_email():
    if auth.user:
        return auth.user.email
    else:
        return 'None'

db.define_table('board',
    # There is also a column called 'id'. 
    Field('author', default = get_email()), # 512 chars at most
    Field('creation_date', 'datetime', default=datetime.utcnow()),
    Field('post_content', 'text'),
    Field('contact'),         
    )

db.board.author.writable = False
db.board.id.readable = False
db.board.creation_date.writable = False
db.board.contact.requires = IS_EMAIL()
db.board.contact.label = 'Contact email'