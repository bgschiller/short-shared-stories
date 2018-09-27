import datetime
import random
import string
from app import db
from models import Story, Fragment
from sqlalchemy.sql import text

EXPIRY_IN_SECONDS = 60

def rand_num_words():
    return random.randint(6, 21)

user_id_chars = string.ascii_letters + string.digits
def random_user_id():
    return ''.join(random.choices(user_id_chars, k=12))

def get_user_id(session):
    user_id = session.get('user_id')
    if user_id is None:
        user_id = random_user_id()
        session['user_id'] = user_id
    return user_id


def lease_story_for_contribution(user_id):
    """
    Either:
     1. An unexpired lease belonging to this user
     2. Find a still-in-progress story that this user
        hasn't contributed to, or
     3. Create a new story.
    Then, create a new Fragment with a null word
    'created_by' this user. This empty Fragment will
    represent the user's claim of being the next person
    to contribute to that story.
    """
    existing_lease = Fragment.query.filter(
        Fragment.created_by == user_id,
        Fragment.word == None,
        Fragment.created_at >= text("CURRENT_TIMESTAMP - interval '{} second'".format(EXPIRY_IN_SECONDS)),
    ).first()
    if existing_lease is not None:
        story = Story.query.get(existing_lease.story_id)
        return {
            'story_id': story.id,
            'num_words': story.num_words,
            'words': [f.word for f in story.fragments if f.word is not None],
            'expires_at': existing_lease.created_at + datetime.timedelta(seconds=EXPIRY_IN_SECONDS),
        }

    story_id = db.session.execute(
        """
        SELECT MIN(s.id) AS story_id
        FROM story s
        JOIN fragment f ON (f.story_id = s.id)
        GROUP BY s.id
        HAVING
          -- story is incomplete
            s.num_words > COUNT(f.id)
          -- logged in user was not most recent contributor
           AND :user_id <> (ARRAY_AGG(f.created_by))[
               array_upper(ARRAY_AGG(f.created_by), 1)
            ]
          -- no outstanding lease on this story
           AND BOOL_AND(f.word IS NOT NULL)
        """,
        { 'user_id': user_id }).scalar()
    if story_id:
        story = Story.query.get(story_id)
    else:
        story = Story(num_words=rand_num_words())
        db.session.add(story)
    fragment = Fragment(created_by=user_id)
    story.fragments.append(fragment)
    db.session.commit()
    return {
        'story_id': story.id,
        'num_words': story.num_words,
        'words': [f.word for f in story.fragments if f.word is not None],
        'expires_at': fragment.created_at + datetime.timedelta(seconds=EXPIRY_IN_SECONDS),
    }

def clear_out_expired_leases():
    db.session.execute(
        '''
        DELETE FROM fragment
        WHERE word IS NULL
        -- necessary to cast CURRENT_TIMESTAMP to timestamp because
        -- CURRENT_TIMESTAMP is a TIMESTAMP WITH TIMEZONE, and our created_at
        -- column is stored without timezone.
          AND created_at + interval '{} second' < CURRENT_TIMESTAMP::timestamp
        '''.format(EXPIRY_IN_SECONDS)
    )
    db.session.commit()
    db.session.execute(
        '''
        DELETE FROM story
        WHERE NOT id = ANY(
            SELECT story_id FROM fragment
        )
        '''
    )
    db.session.commit()

# sentinel objects to be returned on error
FragmentNotFound = object()
InvalidWord = object()

def add_word(story_id, user_id, word):
    """
    Add `word` to the specified story.

    Throws a FragmentNotFound error if the fragment
    could not be found to be updated.
    """
    if ' ' in word or len(word) > 45 or word == '':
        return InvalidWord
    num_rows_updated = (Fragment.query
        .filter(
            Fragment.story_id == story_id,
            Fragment.created_by == user_id,
            Fragment.word == None,
            Fragment.created_at >= text("CURRENT_TIMESTAMP - interval '{} second'".format(EXPIRY_IN_SECONDS)),
        )
        .update({'word': word}, synchronize_session=False))
    if num_rows_updated == 0:
        # something went wrong.
        # perhaps the fragment doesn't exist, or perhaps it's expired.
        return FragmentNotFound
    db.session.commit()
    return None

StoryNotFound = object()

def retrieve_story_by_id(story_id):
    story = Story.query.get(story_id)
    if story is None:
        return StoryNotFound
    return {
        'story_id': story.id,
        'is_complete': story.num_words == len(story.fragments),
        'words': [f.word for f in story.fragments if f.word is not None],
    }

def recently_completed_stories():
    return db.session.execute('''
        SELECT s.id AS story_id
            , JSON_AGG(f.word) AS words
            , MAX(f.created_at) AS last_edit
            , s.num_words
            , TRUE as is_complete
        FROM story s
        JOIN fragment f ON (f.story_id = s.id)
        GROUP BY s.id
        HAVING s.num_words = COUNT(f.id)
           AND BOOL_AND(f.word IS NOT NULL)
        ORDER BY MAX(f.created_at)
        LIMIT 20
        ''').fetchall()

def retrieve_stories_by_user_id(user_id):
    return db.session.execute('''
        SELECT s.id AS story_id
            , JSON_AGG(f.word) AS words
            , MAX(f.created_at) AS last_edit
            , s.num_words
            , COUNT(f.word) = s.num_words AS is_complete
        FROM story s
        JOIN fragment f ON (f.story_id = s.id)
        WHERE s.id = ANY(
            SELECT story_id FROM fragment
            WHERE created_by = :user_id
        )
        GROUP BY s.id
        HAVING BOOL_AND(f.word IS NOT NULL)
        ORDER BY MAX(f.created_at)
    ''', { 'user_id': user_id },
    ).fetchall()
