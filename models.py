from sqlalchemy.sql import func
from datetime import datetime
from app import db

class Fragment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    story_id = db.Column(db.Integer, db.ForeignKey('story.id'), nullable=False)
    # word may be null, in which case it represents
    # that someone is thinking still. We'll hold their
    # spot for a time.
    word = db.Column(db.String(45))

    # created_at is used for several purposes:
    # 1. It tells us the order to display the Fragments in a completed Story.
    # 2. It tells us, for a null-word Fragment, when a user's lease on the
    #    Fragment has expired (and the Fragment should be given over to some
    #     other person)
    created_at = db.Column(db.DateTime(timezone=False), nullable=False, server_default=func.now())
    # We're not requiring any login credentials, so the
    # created_by value is just going to be a random string
    # of characters to identify a person.
    # We're not too concerned with security. The goal is
    # just to avoid having the same person contribute
    # multiple Fragments to the same story.
    created_by = db.Column(db.String(20), nullable=False)

class Story(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    num_words = db.Column(db.Integer, nullable=False)
    fragments = db.relationship(
        Fragment,
        order_by=Fragment.created_at,
        backref=db.backref('story', lazy=True),
    )
