import json

import requests
import valorant
from flask import Flask, g, render_template, request, session, url_for, redirect

app = Flask(__name__)
app.secret_key = '2965096f5a5b435d77794c2ec258289a63cb8274a2eb714af2336f5bfd443b4f'
#print(valorant.get_matchhistory("eu", "81e06dc2-23c7-507e-a684-84475dfed03f", 2))


@app.before_request
def before_request():
    g.id = None
    if 'id' in session:
        g.id = session['id']
    g.match = None
    if 'match' in session:
        g.match.zero = session['match']


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
    mmr_data_by_puuid = valorant.get_mmr_data_by_puuid('v1', g.region, g.puuid)
    g.name = mmr_data_by_puuid['data']['name']
    g.tag = mmr_data_by_puuid['data']['tag']
    g.current_tier = mmr_data_by_puuid['data']['currenttier']
    g.current_tier_patched = mmr_data_by_puuid['data']['currenttierpatched']
    g.ranking_in_tier = mmr_data_by_puuid['data']['ranking_in_tier']
    g.playercard = valorant.get_account_data(g.name, g.tag)["data"]["card"]["wide"]
    g.total = valorant.get_total(g.region, g.puuid)
    for i in range(10):
        i_match = valorant.get_matchhistory(g.region, g.puuid, g.total, (i + 1))
        exec(f'g.match{i + 1}_map = i_match["data"]["metadata"]["map"]')
        exec(f'g.match{i + 1}_mode = i_match["data"]["metadata"]["mode"]')
        exec(f'g.match{i + 1}_rounds_played = i_match["data"]["metadata"]["rounds_played"]')
        players = i_match["data"]["players"]["all_players"]
        for p in players:
            if p["name"] == g.name and p["tag"] == g.tag:
                exec(f'g.match{i + 1}_agent_icon = p["assets"]["agent"]["killfeed"]')
                exec(f'g.match{i + 1}_agent_name = p["character"]')
                exec(f'g.match{i + 1}_score = p["stats"]["score"]')
                exec(f'g.match{i + 1}_kills = p["stats"]["kills"]')
                exec(f'g.match{i + 1}_deaths = p["stats"]["deaths"]')
                exec(f'g.match{i + 1}_assists = p["stats"]["assists"]')
                team = p["team"].lower()
        exec(f'g.match{i + 1}_has_won = i_match["data"]["teams"][team]["has_won"]')
        exec(f'g.match{i + 1}_rounds_won = i_match["data"]["teams"][team]["rounds_won"]')
        exec(f'g.match{i + 1}_rounds_lost = i_match["data"]["teams"][team]["rounds_lost"]')
    return render_template('profile.html')


@app.route('/api/history/<region>/<puuid>')
def history(region, puuid):
    return valorant.raw('matchhistory', region, puuid, "?queue=competitive&startIndex=0&endIndex=20")


@app.route('/api/match/<match_id>')
def match(match_id):
    return valorant.get_match_data(match_id)
