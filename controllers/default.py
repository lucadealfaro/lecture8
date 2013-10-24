# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# Author: Luca de Alfaro

def index():
    """
    This generates the home page, or I hope so.
    """
    rows = db(db.board).select()
    return dict(rows=rows)

@auth.requires_login()
def index_nice():
    q = db.board
    grid = SQLFORM.grid(q,
        searchable=True,
        fields=[db.board.id, db.board.author, db.board.post_content, db.board.contact],
        csv=True, 
        details=True, create=True, editable=True, deletable=True,
        links=[
            dict(header=T('View the record'), 
                 body = lambda r: A('Edit', _class='btn', 
                                    _href=URL('default', 'edit', args=[r.id])),
            )],
        )
    # Let's return the results.
    return dict(grid=grid)

@auth.requires_login()
def edit():
    """Edits a my_record of my board."""
    # my_record = db(db.board.id == request.args(0)).select().first()
    # if my_record is None: complain
    # my_record = db.board(request.args(0)) or redirect(URL('default', 'index'))
    my_record = db.board(request.args(0))
    if my_record is None:
        session.flash = "Invalid request"
        redirect(URL('default', 'index'))
    # Hide creation date.
    db.board.creation_date.readable = False
    form = SQLFORM(db.board, record=my_record)
    if form.process().accepted:
        redirect(URL('default', 'index'))
    return dict(form=form)
    

def view():
    my_record = db.board(request.args(0))
    if my_record is None:
        session.flash = "Invalid request"
        redirect(URL('default', 'index'))
    form = SQLFORM(db.board, record=my_record, readonly=True)
    return dict(form=form)

@auth.requires_login()
def add():
    """Adds a post."""
    form = SQLFORM(db.board)
    if form.process().accepted:
        # The form content was valid, and the data is already
        # in the db.
        redirect(URL('default', 'index'))
    # We are here in two cases:
    # - This is a GET, and the form is empty.
    # - This was a POST, and there are errors. 
    # In both cases, we need to display the form, as it contains
    # also any errors.
    return dict(form=form)
    

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
