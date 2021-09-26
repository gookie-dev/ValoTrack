import requests
import valorant
from flask import Flask, g, render_template, request, session, url_for, redirect

app = Flask(__name__)
app.secret_key = '2965096f5a5b435d77794c2ec258289a63cb8274a2eb714af2336f5bfd443b4f'


@app.before_request
def before_request():
    g.id = None
    if 'id' in session:
        g.id = session['id']


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session.pop('id', None)
        username = request.form['username']
        tagline = request.form['tag']
        region = request.form['region']
        r = valorant.get_account_data(username, tagline)
        if r['status'] == '200':
            try:
                if valorant.get_mmr_data('v1', region, username, tagline)['status'] == '200':
                    session['id'] = region + r['data']['puuid']
                    return redirect(url_for('profile'))
            except:
                pass
        return redirect(url_for('index'))
    return render_template('index.html')


@app.route('/profile')
def profile():
    if not g.id:
        return redirect(url_for('index'))
    g.region = g.id[:2]
    g.puuid = g.id[2:]
    g.name = valorant.get_mmr_data_by_puuid('v1', g.region, g.puuid)['data']['name']
    g.current_tier = valorant.get_mmr_data_by_puuid('v1', g.region, g.puuid)['data']['currenttier']
    g.current_tier_patched = valorant.get_mmr_data_by_puuid('v1', g.region, g.puuid)['data']['currenttierpatched']
    g.ranking_in_tier = valorant.get_mmr_data_by_puuid('v1', g.region, g.puuid)['data']['ranking_in_tier']
    return render_template('profile.html')


@app.route('/api/history/<region>/<puuid>')
def history(region, puuid):
    return valorant.raw('matchhistory', region, puuid, "?queue=competitive&startIndex=0&endIndex=20")


@app.route('/api/match/<match_id>')
def match(match_id):
    return valorant.get_match_data(match_id)
