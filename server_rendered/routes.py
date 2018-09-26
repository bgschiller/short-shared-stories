from flask import request, session, render_template, flash, redirect, url_for
from app import app
from actions import (
    recently_completed_stories, lease_story_for_contribution,
    get_user_id, add_word, FragmentNotFound,
    retrieve_story_by_id, StoryNotFound,
    retrieve_stories_by_user_id, InvalidWord,
)

@app.route('/')
def index():
    recent_stories = recently_completed_stories()
    return render_template(
        'stories.html',
        header='Recent Stories',
        stories=recent_stories,
        error_writing_story=request.args.get('error_writing_story'),
        story_not_found=request.args.get('story_not_found'),
    )

@app.route('/yours')
def your_stories():
    stories = retrieve_stories_by_user_id(get_user_id(session))
    return render_template(
        'stories.html',
        header='Your Stories',
        stories=stories,
    )

@app.route('/write')
def write():
    user_id = get_user_id(session)
    leased_story = lease_story_for_contribution(user_id)
    invalid_word_error = request.args.get('invalid_word_error')
    return render_template(
        'write.html',
        story=leased_story,
        invalid_word_error=invalid_word_error,
    )

@app.route('/write/<int:story_id>', methods=['POST'])
def submit_word(story_id):
    result = add_word(story_id, get_user_id(session), request.form['word'])
    if result is FragmentNotFound:
        path = '/?error_writing_story=1'
    elif result is InvalidWord:
        path = '/write?invalid_word_error=1'
    else:
        path = '/story/{}'.format(story_id)
    return redirect(path)

@app.route('/story/<int:story_id>')
def story_permalink(story_id):
    story = retrieve_story_by_id(story_id)
    if story is StoryNotFound:
        return redirect('/?story_not_found=1')
    return render_template('story.html', story=story)
