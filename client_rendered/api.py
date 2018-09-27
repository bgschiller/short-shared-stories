from flask import request, session, jsonify
from app import app
from actions import (
    recently_completed_stories, lease_story_for_contribution,
    get_user_id, add_word, FragmentNotFound,
    retrieve_story_by_id, StoryNotFound,
    retrieve_stories_by_user_id, InvalidWord,
    clear_out_expired_leases,
)

app.before_request(clear_out_expired_leases)

@app.route('/api/recent_stories')
def recent_stories():
    recent_stories = recently_completed_stories()
    return jsonify(recent_stories)

@app.route('/api/your_stories')
def your_stories():
    return jsonify(retrieve_stories_by_user_id(get_user_id(session)))

@app.route('/api/story')
def write():
    return jsonify(lease_story_for_contribution(get_user_id(session)))

@app.route('/api/story/<int:story_id>', methods=['POST'])
def submit_word(story_id):
    data = request.get_json()
    result = add_word(story_id, get_user_id(session), data['word'])
    if result is FragmentNotFound:
        return jsonify({ 'error': 'FragmentNotFound' }), 404
    elif result is InvalidWord:
        return jsonify({ 'error': 'InvalidWord' }), 400
    return jsonify({ 'status': 'success' })

@app.route('/api/story/<int:story_id>')
def get_story(story_id):
    story = retrieve_story_by_id(story_id)
    if story is StoryNotFound:
        return jsonify({ 'error': 'StoryNotFound' }), 404
    return jsonify(story)
