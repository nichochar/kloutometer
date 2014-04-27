import os
import json
from flask import Flask, request, session, g, redirect, url_for, abort, \
        render_template, flash

from klout import KloutHTTPError
from utils import get_klout_score


# Create app
app = Flask(__name__)
app.config.from_object(__name__)

# Load default config
app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='pipicaca',
    ))

app.config.from_envvar('FLASKR_SETTINGS', silent=True)

@app.route('/', methods=['GET','POST'])
def menu():
    return render_template('menu.html')

@app.route('/chart')
def show_chart():
    handlers = request.args.get('handles', None)

    if handlers:
        # Strip eventual spaces
        handlers = handlers.replace(" ","")

        # Split at comma
        handle_list = handlers.split(',')
        handle_scores = {}
        for handle in handle_list:
            try:
                score = get_klout_score(handle)
                handle_scores[handle] = score
            except KloutHTTPError, e:
                # Assume this is a handle typo
                #@TODO: flash a message to the user with all the mistakes there
                pass

        # We now need to serialize it to json so the highcharts can read
        json_data = json.dumps(handle_scores)
        return render_template('chart.html', json_data=json_data)

    else:
        return render_template('error.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html')

if __name__ == '__main__':
    app.run()
