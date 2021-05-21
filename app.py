from flask import Flask, request, render_template, session
from flask_debugtoolbar import DebugToolbarExtension
from stories import Story

app = Flask(__name__)

app.config['SECRET_KEY'] = "key"
debug = DebugToolbarExtension(app)

story1 = Story(
    ["place", "noun", "verb", "adjective", "plural_noun"],
    """Once upon a time in a long-ago {place}, there lived a
       large {adjective} {noun}. It loved to {verb} {plural_noun}."""
)

story2 = Story(
    ["noun", "verb", "adjective1", "adjective2"],
    """There once was a {noun} that really loved to {verb}. It was {adjective1} and {adjective2}."""
)

story3 = Story(
    ["verb", "number", "place", "noun"],
    """My favorite thing to do is to {verb}. I do this {number} times each day. 
    I even do ths in the {place} with a {noun}."""
)

stories = {"story1": story1, "story2": story2, "story3": story3}

# story = stories["story1"]

@app.route('/')
def show_home():
    return render_template('index.html', stories=stories)

@app.route('/input')
def show_input():
    story_choice = request.args["story-choice"]
    story = stories[story_choice]
    session['story'] = story_choice
    return render_template('input.html', story=story)

@app.route('/story')
def show_story():
    answers = request.args
    story = stories.get(session.get("story"))
    user_story = story.generate(answers)
    return render_template('story.html', user_story=user_story)
