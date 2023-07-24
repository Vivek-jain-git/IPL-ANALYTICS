import pickle as pkl
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
with open('final_players.pkl','rb') as f:
    a=pkl.load(f)
    ba=a[(a['work']=='Batter') | (a['work']=='WK Keeper - Batter')]['name'].unique()
    bo = a[a['work'] == 'Bowler']['name'].unique()
    ar = a[a['work'] == 'All-Rounder']['name'].unique()
    a['name']=a['name'].str.replace('\xa0',' ')
    sp=a['name'].unique()
    t=a['team'].str.replace('-',' ').str.title().str.strip().unique()
    a['new_team']=a['team'].str.replace('-',' ').str.title().str.strip()
with open('winners.pkl','rb') as f:
    w=pkl.load(f)
with open('final4.pkl','rb') as f:
    f4=pkl.load(f)
with open('t4.pkl','rb') as f:
    t4=pkl.load(f)
with open('cc.pkl','rb') as f:
    cc=pkl.load(f)
with open('oandp.pkl','rb') as f:
    oandp=pkl.load(f)
    orange=oandp['orange']
    purple=oandp['purple']
with open('max_score.pkl','rb') as f:
    maxs=pkl.load(f)
    maxs['Max_score']=maxs['Max_score'].map(int)
with open('min_score.pkl','rb') as f:
    mins=pkl.load(f)
with open('teamcomp.pkl','rb') as f:
    teamcomp=pkl.load(f)
with open('points_nrr.pkl','rb') as f:
    points_nrr=pkl.load(f)
with open('dept.pkl','rb') as f:
    dept=pkl.load(f)
with open('tvalllabel.pkl','rb') as f:
    comp=pkl.load(f)
with open('team_late.pkl','rb') as f:
    tl=pkl.load(f)
    tl['wickets']=tl['wickets'].astype(np.int16)
with open('deliveries.pkl','rb') as f:
    d=pkl.load(f)
with open('matches_played.pkl','rb') as f:
    mp=pkl.load(f)

from flask import Flask,render_template,url_for,redirect,request,jsonify
app=Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html',msg=list(t))
@app.route('/player-vs-player')
def hi1():
    return render_template('player-vs-player.html',msg=list(sp))
@app.route('/index')
def hi6():
    return render_template('index.html')
@app.route('/s-i-n-g-l-e-p-l-a-y-e-r')
def hi7():
    redirect('/test')
    return render_template('s-i-n-g-l-e-p-l-a-y-e-r.html',msg=list(sp))
@app.route('/s-p-bowling')
def hi8():
    return render_template('s-p-bowling.html')
@app.route('/s-p-batting')
def hi9():
    return render_template('s-p-batting.html')
@app.route('/team-vs-team')
def hi10():
    return render_template('team-vs-team.html',msg=list(t))
@app.route('/team')
def hi11():
    return render_template('team.html',msg=list(t))
@app.route('/team-vs-all')
def hi12():
    return render_template('team-vs-all.html',msg=list(t))
@app.route('/bestteams')
def bestteams():
    return render_template('best-teams.html')

@app.route('/playervsplayer', methods=['POST'])
def playervsplayer():
    with open('deliveries.pkl', 'rb') as f:
        d = pkl.load(f)
    player1=  request.form.get('player1')
    player2 = request.form.get('player2')
    msgg1 = (a[a['name'] == player1].sort_values(by='year', ascending=False).head(1)['data'].values[0][0])
    msgg2 = (a[a['name'] == player2].sort_values(by='year', ascending=False).head(1)['data'].values[0][0])
    bdf1 = d[d['batter'] == player1]
    bdf2=  d[d['batter'] == player2]
    # innings_played=str(pdf.groupby(['season','match_no']).count().shape[0])
    # batting
    if bdf1.shape[0] == 0:
        runs1 = ' - '
        avg1 = ' - '
        sr1 = ' - '
        fours1 = ' - '
        sixes1 = ' - '
    else:
        runs1 = str(bdf1['batter_runs'].sum())
        if ((bdf1[bdf1['player_out'] == player1].shape[0])) == 0:
            avg1 = runs1
        else:
            avg1 = str(round((int(runs1) / (bdf1[bdf1['player_out'] == player1].shape[0])), 2))
        sr1 = str(round(((int(runs1) / (bdf1[~(bdf1['extra_type'] == 'wides')].shape[0])) * 100), 2))
        fours1 = str(bdf1[bdf1['batter_runs'] == 4].shape[0])
        sixes1 = str(bdf1[bdf1['batter_runs'] == 6].shape[0])
    if bdf2.shape[0] == 0:
        runs2 = ' - '
        avg2 = ' - '
        sr2 = ' - '
        fours2 = ' - '
        sixes2 = ' - '
    else:
        runs2 = str(bdf2['batter_runs'].sum())
        if ((bdf2[bdf2['player_out'] == player2].shape[0])) == 0:
            avg2 = runs2
        else:
            avg2 = str(round((int(runs2) / (bdf2[bdf2['player_out'] == player2].shape[0])), 2))
        sr2 = str(round(((int(runs2) / (bdf2[~(bdf2['extra_type'] == 'wides')].shape[0])) * 100), 2))
        fours2 = str(bdf2[bdf2['batter_runs'] == 4].shape[0])
        sixes2 = str(bdf2[bdf2['batter_runs'] == 6].shape[0])

        # Return the result as a JSON response
    # bowling
    bodf1 = d[d['bowler'] == player1]
    bodf2=  d[d['bowler'] == player2]
    if bodf1.shape[0] == 0:
        overs1 = ' - '
        wickets1 = ' - '
        economy1 = ' - '
        srt1 = ' - '
        wicket31 = ' - '
    else:
        finaldf_1 = bodf1[bodf1['extra_type'].isin([np.nan, 'byes', 'legbyes', 'penalty'])]
        finaldf2_1 = bodf1[bodf1['extra_type'].isin([np.nan, 'byes', 'legbyes', 'penalty', 'wides', 'noballs'])]
        haulsdf_1 = finaldf_1[finaldf_1['type_of_dismissal'].isin(
            ['stumped', 'caught', 'lbw', 'bowled', 'caught and bowled', 'hit wicket'])]

        overs = int(finaldf_1.shape[0] / 6)
        balls = finaldf_1.shape[0] - (overs * 6)
        overs1 = str(overs) + '.' + str(balls)
        wickets1 = str(int(haulsdf_1['wickets'].sum()))
        if float(overs1)<1.0:
            economy1 = str(round((sum(finaldf2_1['total_runs'])*6 / float(balls)), 2))
        else:
            economy1= str(round((sum(finaldf2_1['total_runs']) / float(overs1)), 2))
        try:
            srt1 = str(round(((float(overs1) * 6) / int(wickets1)), 2))
        except ZeroDivisionError:
            srt1 = 'inf'
        wicket31 = str((haulsdf_1.groupby(['season', 'match_no'])['wickets'].sum() >= 3).values.sum())
    if bodf2.shape[0] == 0:
        overs2 = ' - '
        wickets2 = ' - '
        economy2 = ' - '
        srt2 = ' - '
        wicket32 = ' - '
    else:
        finaldf_2 = bodf2[bodf2['extra_type'].isin([np.nan, 'byes', 'legbyes', 'penalty'])]
        finaldf2_2 = bodf2[bodf2['extra_type'].isin([np.nan, 'byes', 'legbyes', 'penalty', 'wides', 'noballs'])]
        haulsdf_2 = finaldf_2[finaldf_2['type_of_dismissal'].isin(
            ['stumped', 'caught', 'lbw', 'bowled', 'caught and bowled', 'hit wicket'])]

        overs = int(finaldf_2.shape[0] / 6)
        balls = finaldf_2.shape[0] - (overs * 6)
        overs2 = str(overs) + '.' + str(balls)
        wickets2 = str(int(haulsdf_2['wickets'].sum()))
        if float(overs2)<1.0:
            economy2 = str(round((sum(finaldf2_2['total_runs'])*6 / float(balls)), 2))
        else:
            economy2= str(round((sum(finaldf2_2['total_runs']) / float(overs2)), 2))
        try:
            srt2 = str(round(((float(overs2) * 6) / int(wickets2)), 2))
        except ZeroDivisionError:
            srt2 = 'inf'
        wicket32 = str((haulsdf_2.groupby(['season', 'match_no'])['wickets'].sum() >= 3).values.sum())
    # fielding
    fdf1 = d[(d['fielder1'] == player1) | (d['fielder2'] == player1) | (d['fielder3'] == player1)]
    try:
        runout1 = str(fdf1[fdf1['type_of_dismissal'].isin(['caught', 'caught and bowled', 'run out', 'stumped'])][
                         'type_of_dismissal'].value_counts()['run out'])
    except KeyError:
        runout1 = '0'
    try:
        stumped1 = str(fdf1[fdf1['type_of_dismissal'].isin(['caught', 'caught and bowled', 'run out', 'stumped'])][
                          'type_of_dismissal'].value_counts()['stumped'])
    except KeyError:
        stumped1 = '0'
    try:
        catch1_1 = fdf1[fdf1['type_of_dismissal'].isin(['caught', 'caught and bowled', 'run out', 'stumped'])][
            'type_of_dismissal'].value_counts()['caught']
    except KeyError:
        catch1_1 = 0
    catch2_1 = len(d[d['type_of_dismissal'] == 'caught and bowled'][
                     d[d['type_of_dismissal'] == 'caught and bowled']['bowler'] == player1][
                     'type_of_dismissal'])
    catch1 = str(catch1_1 + catch2_1)

    fdf2 = d[(d['fielder1'] == player2) | (d['fielder2'] == player2) | (d['fielder3'] == player2)]
    try:
        runout2 = str(fdf2[fdf2['type_of_dismissal'].isin(['caught', 'caught and bowled', 'run out', 'stumped'])][
                          'type_of_dismissal'].value_counts()['run out'])
    except KeyError:
        runout2 = '0'
    try:
        stumped2 = str(fdf2[fdf2['type_of_dismissal'].isin(['caught', 'caught and bowled', 'run out', 'stumped'])][
                           'type_of_dismissal'].value_counts()['stumped'])
    except KeyError:
        stumped2 = '0'
    try:
        catch1_2 = fdf2[fdf2['type_of_dismissal'].isin(['caught', 'caught and bowled', 'run out', 'stumped'])][
            'type_of_dismissal'].value_counts()['caught']
    except KeyError:
        catch1_2 = 0
    catch2_2 = len(d[d['type_of_dismissal'] == 'caught and bowled'][
                       d[d['type_of_dismissal'] == 'caught and bowled']['bowler'] == player2][
                       'type_of_dismissal'])
    catch2 = str(catch1_2 + catch2_2)
    #Matchup1
    mdf1=d[(d['batter'] == player1) & (d['bowler'] == player2)]
    runs_m1=mdf1['batter_runs'].sum()
    balls_m1 = mdf1[~(mdf1['extra_type'] == 'wides') | (mdf1['extra_type'] == 'noballs')].shape[0]
    if balls_m1 == 0:
        sr_m1 = 0
    else:
        sr_m1 = round((runs_m1 / balls_m1) * 100,2)
    l = ['stumped', 'caught', 'lbw', 'bowled', 'caught and bowled', 'hit wicket']
    d1 = mdf1[mdf1['type_of_dismissal'].isin(l)]
    if d1.shape[0] == 0:
        avg_m1 = runs_m1
    else:
        avg_m1 = round((runs_m1 / d1.shape[0]),2)
    dismissed_m1 = d1.shape[0]
    if balls_m1 == 0:
        economy_m1 = 0
    else:
        economy_m1 = round((runs_m1 * 6 / balls_m1),2)
    if (mdf1[(mdf1['batter_runs'].isin([4, 6]))].shape[0]) == 0:
        balls_per_boundary_m1 = 0
    else:
        balls_per_boundary_m1 = round((balls_m1 / (mdf1[(mdf1['batter_runs'].isin([4, 6]))].shape[0])),2)
    #Matchup2
    mdf2=d[(d['batter'] == player2) & (d['bowler'] == player1)]
    runs_m2=mdf2['batter_runs'].sum()
    balls_m2 = mdf2[~(mdf2['extra_type'] == 'wides') | (mdf2['extra_type'] == 'noballs')].shape[0]
    if balls_m2 == 0:
        sr_m2 = 0
    else:
        sr_m2 = round((runs_m2 / balls_m2) * 100,2)
    l = ['stumped', 'caught', 'lbw', 'bowled', 'caught and bowled', 'hit wicket']
    d2 = mdf2[mdf2['type_of_dismissal'].isin(l)]
    if d2.shape[0] == 0:
        avg_m2 = runs_m2
    else:
        avg_m2 = round((runs_m2 / d2.shape[0]),2)
    dismissed_m2 = d2.shape[0]
    if balls_m2 == 0:
        economy_m2 = 0
    else:
        economy_m2 = round((runs_m2 * 6 / balls_m2),2)
    if (mdf2[(mdf2['batter_runs'].isin([4, 6]))].shape[0]) == 0:
        balls_per_boundary_m2 = 0
    else:
        balls_per_boundary_m2 = round((balls_m2 / (mdf2[(mdf2['batter_runs'].isin([4, 6]))].shape[0])),2)
    mat_played1 = str(mp[mp['players'] == player1]['matches'].values[0])
    mat_played2 = str(mp[mp['players'] == player2]['matches'].values[0])
    return jsonify(result1=msgg1,result2=msgg2,runs1=runs1,avg1=avg1,sr1=sr1,fours1=fours1,sixes1=sixes1
                   ,runs2=runs2,avg2=avg2,sr2=sr2,fours2=fours2,sixes2=sixes2
                   ,overs1=overs1,wickets1=wickets1,economy1=economy1,srt1=srt1,wicket31=wicket31
                   ,overs2=overs2,wickets2=wickets2,economy2=economy2,srt2=srt2,wicket32=wicket32
                   ,runout1=runout1,stumped1=stumped1,catch1=catch1,runout2=runout2,stumped2=stumped2,catch2=catch2
                   ,runs_m1=str(runs_m1),balls_m1=str(balls_m1),sr_m1=str(sr_m1),avg_m1=str(avg_m1),dismissed_m1=str(dismissed_m1),economy_m1=str(economy_m1),balls_per_boundary_m1=str(balls_per_boundary_m1)
                   ,runs_m2=str(runs_m2),balls_m2=str(balls_m2),sr_m2=str(sr_m2),avg_m2=str(avg_m2),dismissed_m2=str(dismissed_m2),economy_m2=str(economy_m2),balls_per_boundary_m2=str(balls_per_boundary_m2),mat_played1=mat_played1,mat_played2=mat_played2)
@app.route('/test', methods=['POST'])
def test():
    player = request.form.get('player')
    # Process the variables in Python
    msgg = (a[a['name'] == player].sort_values(by='year', ascending=False).head(1)['data'].values[0][0])
    bdf=d[d['batter']==player]
    #innings_played=str(pdf.groupby(['season','match_no']).count().shape[0])
    #batting
    if bdf.shape[0]==0:
        runs=' - '
        avg=' - '
        sr=' - '
        plus30=' - '
        plus100=' - '
        fours=' - '
        sixes=' - '
    else:
        runs=str(bdf['batter_runs'].sum())
        if ((bdf[bdf['player_out'] == player].shape[0]))==0:
            avg=runs
        else:
            avg=str(round((int(runs)/(bdf[bdf['player_out']==player].shape[0])),2))
        sr=str(round(((int(runs)/(bdf[~(bdf['extra_type']=='wides')].shape[0]))*100),2))
        arr=((bdf.groupby(['season','match_no'])['batter_runs'].sum()).values)
        plus30=len(arr[arr>=30])
        plus100=len(arr[arr>=100])
        fours=str(bdf[bdf['batter_runs']==4].shape[0])
        sixes = str(bdf[bdf['batter_runs'] == 6].shape[0])
    x = np.array(d[d['batter'] == player].groupby('season')['batter_runs'].sum().index)
    y = np.array(d[d['batter'] == player].groupby('season')['batter_runs'].sum().values)
    # Generate the graph
    if len(x)==0 or len(y)==0:
        image_base64="nodata"
    elif len(x)==1 and len(y)==1:
        if y[0]==0:
            y = np.append(y,-1)
        fig, ax = plt.subplots()
        ax.bar(x, y,color='red')

        # Remove additional contents
        ax.patch.set_alpha(0)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        font_family = 'sans-serif'
        ax.tick_params(axis="x", labelsize=25, labelcolor='white', pad=40)
        ax.tick_params(axis="y", labelsize=25, labelcolor='white')
        x_tick_labels = [tick.get_text() for tick in ax.get_xticklabels()]
        y_tick_labels = [tick.get_text() for tick in ax.get_yticklabels()]

        # Set the font weight to bold for x and y tick labels
        ax.set_xticklabels(x_tick_labels, weight='bold', fontfamily=font_family)
        ax.set_yticklabels(y_tick_labels, weight='bold', fontfamily=font_family)
        ax.set_xticks([min(x), max(x)])
        ax.set_yticks([min(y), max(y)])
        ax.set_xticklabels([min(x), max(x)])
        if y[0]==0:
            ax.set_yticklabels([0, max(y)])
        else:
            ax.set_yticklabels([min(y), max(y)])
        plt.subplots_adjust(bottom=0.3)

        # Save the graph to a bytes buffer
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', transparent=True)
        buffer.seek(0)

        # Encode the buffer to base64 string
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    else:
        fig, ax = plt.subplots()
        ax.plot(x, y,'r',linewidth=8,)

        # Remove additional contents
        ax.patch.set_alpha(0)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        font_family='sans-serif'
        ax.tick_params(axis="x", labelsize=25,labelcolor='white',pad=40)
        ax.tick_params(axis="y", labelsize=25,labelcolor='white')
        x_tick_labels = [tick.get_text() for tick in ax.get_xticklabels()]
        y_tick_labels = [tick.get_text() for tick in ax.get_yticklabels()]

        # Set the font weight to bold for x and y tick labels
        ax.set_xticklabels(x_tick_labels, weight='bold',fontfamily=font_family)
        ax.set_yticklabels(y_tick_labels, weight='bold',fontfamily=font_family)
        ax.set_xticks([min(x), max(x)])
        ax.set_yticks([min(y), max(y)])
        ax.set_xticklabels([min(x), max(x)])
        ax.set_yticklabels([min(y), max(y)])

        plt.subplots_adjust(bottom=0.3)


        # Save the graph to a bytes buffer
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png',transparent=True)
        buffer.seek(0)

        # Encode the buffer to base64 string
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    season_bat = []
    runs_bat = []
    sr_bat = []
    opponent_bat = []
    balls_bat = []
    match_no_bat = []
    vk = d[d['batter'] == player]
    g_bat = vk.groupby(['season', 'match_no', 'innings'])
    group_list = [vk.loc[indices] for group, indices in g_bat.groups.items()]
    batdf = pd.DataFrame(columns=['season', 'match_no', 'runs', 'sr', 'balls', 'opponent'])
    for i in group_list:
        match_no_1 = i['match_no'].unique()[0]
        season_1 = i['season'].values[0]
        opponent_1 = i['bowling_team'].unique()[0]
        runs_1 = i['batter_runs'].sum()
        try:
            sr_1 = round(((int(runs_1) / (i[~(i['extra_type'] == 'wides')].shape[0])) * 100),2)
        except ZeroDivisionError:
            sr_1=np.nan
        balls_1 = (i[~(i['extra_type'] == 'wides')].shape[0])
        season_bat.append(season_1)
        runs_bat.append(runs_1)
        sr_bat.append(sr_1)
        opponent_bat.append(opponent_1)
        balls_bat.append(balls_1)
        match_no_bat.append(match_no_1)
    batdf['season'] = season_bat
    batdf['runs'] = runs_bat
    batdf['sr'] = sr_bat
    batdf['opponent'] = opponent_bat
    batdf['balls'] = balls_bat
    batdf['match_no'] = match_no_bat
    f = batdf.sort_values(by=['runs', 'sr'], ascending=[False, False]).head(1)
    try:
        p1=(str(f['runs'].values[0]) +'(' + str(f['balls'].values[0]) + ')' + ' in ' + str(
        f['season'].values[0]) + ' VS ' + str(f['opponent'].values[0]) + '.')
    except IndexError:
        p1=' - '
    print(p1)
        # Return the result as a JSON response
    #bowling
    bodf=d[d['bowler']==player]
    if bodf.shape[0]==0:
        overs=' - '
        wickets=' - '
        economy=' - '
        aveg=' - '
        srt=' - '
        wicket3=' - '
        wicket5=' - '
    else:
        finaldf=bodf[bodf['extra_type'].isin([np.nan,'byes','legbyes','penalty'])]
        finaldf2 = bodf[bodf['extra_type'].isin([np.nan, 'byes', 'legbyes', 'penalty','wides','noballs'])]
        haulsdf=finaldf[finaldf['type_of_dismissal'].isin(['stumped','caught','lbw','bowled','caught and bowled','hit wicket'])]

        overs = int(finaldf.shape[0] / 6)
        balls = finaldf.shape[0] - (overs * 6)
        overs = str(overs) + '.' + str(balls)
        wickets = str(int(haulsdf['wickets'].sum()))
        if float(overs)<1.0:
            economy = str(round((sum(finaldf2['total_runs'])*6 / float(balls)), 2))
        else:
            economy= str(round((sum(finaldf2['total_runs']) / float(overs)), 2))
        try:
            aveg = str(round((sum(finaldf2['total_runs']) / int(wickets)),2))
        except ZeroDivisionError:
            aveg='inf'
        try:
            srt = str(round(((float(overs) * 6) / int(wickets)),2))
        except ZeroDivisionError:
            srt='inf'
        wicket3 = str((haulsdf.groupby(['season','match_no'])['wickets'].sum()>=3).values.sum())
        wicket5 = str((haulsdf.groupby(['season', 'match_no'])['wickets'].sum() >= 5).values.sum())

    e=d[(d['bowler']==player) & (d['type_of_dismissal'].isin(['stumped','caught','lbw','bowled','caught and bowled','hit wicket']))]
    x1 = np.array(e.groupby('season')['wickets'].sum().index)
    y1 = np.array(e.groupby('season')['wickets'].sum().values)
    if len(x1)==0 or len(y1)==0:
        image_base641="nodata"
    elif len(x1)==1 & len(y1)==1:
        fig1, ax1 = plt.subplots()
        ax1.bar(x1, y1,color='red')

        # Remove additional contents
        ax1.patch.set_alpha(0)
        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)
        ax1.spines['bottom'].set_visible(False)
        ax1.spines['left'].set_visible(False)
        font_family = 'sans-serif'
        ax1.tick_params(axis="x", labelsize=25, labelcolor='white', pad=40)
        ax1.tick_params(axis="y", labelsize=25, labelcolor='white')
        x_tick_labels = [tick.get_text() for tick in ax1.get_xticklabels()]
        y_tick_labels = [tick.get_text() for tick in ax1.get_yticklabels()]

        # Set the font weight to bold for x and y tick labels
        ax1.set_xticklabels(x_tick_labels, weight='bold', fontfamily=font_family)
        ax1.set_yticklabels(y_tick_labels, weight='bold', fontfamily=font_family)
        ax1.set_xticks([int(min(x1)), int(max(x1))])
        ax1.set_yticks([int(min(y1)), int(max(y1))])
        ax1.set_xticklabels([int(min(x1)), int(max(x1))])
        ax1.set_yticklabels([int(min(y1)), int(max(y1))])

        plt.subplots_adjust(bottom=0.3)

        # Save the graph to a bytes buffer
        buffer1 = io.BytesIO()
        plt.savefig(buffer1, format='png', transparent=True)
        buffer1.seek(0)

        # Encode the buffer to base64 string
        image_base641 = base64.b64encode(buffer1.getvalue()).decode('utf-8')
    else:
        fig1, ax1 = plt.subplots()
        ax1.plot(x1, y1,'r',linewidth=8,)

        # Remove additional contents
        ax1.patch.set_alpha(0)
        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)
        ax1.spines['bottom'].set_visible(False)
        ax1.spines['left'].set_visible(False)
        font_family='sans-serif'
        ax1.tick_params(axis="x", labelsize=25,labelcolor='white',pad=40)
        ax1.tick_params(axis="y", labelsize=25,labelcolor='white')
        x_tick_labels = [tick.get_text() for tick in ax1.get_xticklabels()]
        y_tick_labels = [tick.get_text() for tick in ax1.get_yticklabels()]

        # Set the font weight to bold for x and y tick labels
        ax1.set_xticklabels(x_tick_labels, weight='bold',fontfamily=font_family)
        ax1.set_yticklabels(y_tick_labels, weight='bold',fontfamily=font_family)
        ax1.set_xticks([int(min(x1)), int(max(x1))])
        ax1.set_yticks([int(min(y1)), int(max(y1))])
        ax1.set_xticklabels([int(min(x1)), int(max(x1))])
        ax1.set_yticklabels([int(min(y1)), int(max(y1))])

        plt.subplots_adjust(bottom=0.3)


        # Save the graph to a bytes buffer
        buffer1 = io.BytesIO()
        plt.savefig(buffer1, format='png',transparent=True)
        buffer1.seek(0)

        # Encode the buffer to base64 string
        image_base641 = base64.b64encode(buffer1.getvalue()).decode('utf-8')

    season_bowl = []
    opponent_bowl = []
    match_no_bowl = []
    overs_bowl = []
    wickets_bowl = []
    runs_bowl = []
    economy_bowl = []
    srt_bowl = []
    jb = d[d['bowler'] == player]
    g_bowl = jb.groupby(['season', 'match_no', 'innings'])
    group_list1 = [jb.loc[indices] for group, indices in g_bowl.groups.items()]
    bowldf = pd.DataFrame(columns=['season', 'opponent', 'match_no', 'overs', 'wickets', 'runs', 'economy', 'srt'])
    for i in group_list1:
        season_2 = i['season'].unique()[0]
        opponent_2 = i['batting_team'].unique()[0]
        match_no_2 = i['match_no'].unique()[0]
        finaldf_2 = i[i['extra_type'].isin([np.nan, 'byes', 'legbyes', 'penalty'])]
        finaldf2_2 = i[i['extra_type'].isin([np.nan, 'byes', 'legbyes', 'penalty', 'wides', 'noballs'])]
        haulsdf_2 = finaldf_2[finaldf_2['type_of_dismissal'].isin(
            ['stumped', 'caught', 'lbw', 'bowled', 'caught and bowled', 'hit wicket'])]
        overs_2 = int(finaldf_2.shape[0] / 6)
        balls_2 = finaldf_2.shape[0] - (overs_2 * 6)
        overs_2 = str(overs_2) + '.' + str(balls_2)
        wickets_2 = int(haulsdf_2['wickets'].sum())
        finaldf3_2 = i[i['extra_type'].isin([np.nan, 'wides', 'noballs'])]
        runs_2 = finaldf3_2['total_runs'].sum()
        if float(overs_2) == 0:
            economy_2 = np.nan
        else:
            economy_2 = round((runs_2 / float(overs_2)), 2)
        try:
            srt_2 = round(((float(overs_2) * 6) / int(wickets_2)), 2)
        except ZeroDivisionError:
            srt_2 = np.nan
        season_bowl.append(season_2)
        opponent_bowl.append(opponent_2)
        match_no_bowl.append(match_no_2)
        overs_bowl.append(overs_2)
        wickets_bowl.append(wickets_2)
        runs_bowl.append(runs_2)
        economy_bowl.append(economy_2)
        srt_bowl.append(srt_2)
    bowldf['season'] = season_bowl
    bowldf['opponent'] = opponent_bowl
    bowldf['match_no'] = match_no_bowl
    bowldf['overs'] = overs_bowl
    bowldf['wickets'] = wickets_bowl
    bowldf['runs'] = runs_bowl
    bowldf['economy'] = economy_bowl
    bowldf['srt'] = srt_bowl
    f1 = bowldf.sort_values(by=['wickets', 'economy', 'srt'], ascending=[False, True, True]).head(1)
    try:
        p2=(str(f1['wickets'].values[0]) + '/' + str(f1['runs'].values[0]) + ' in ' + str(
            f1['overs'].values[0]) + ' overs' + ' VS ' + str(f1['opponent'].values[0]) + ' in '+str(f1['season'].values[0])+'.')
    except IndexError:
        p2=(' -')
    print(p2)

    #fielding
    fdf= d[(d['fielder1']==player) | (d['fielder2']==player) | (d['fielder3']==player)]
    try:
        runout=str(fdf[fdf['type_of_dismissal'].isin(['caught','caught and bowled','run out','stumped'])]['type_of_dismissal'].value_counts()['run out'])
    except KeyError:
        runout='0'
    try:
        stumped=str(fdf[fdf['type_of_dismissal'].isin(['caught','caught and bowled','run out','stumped'])]['type_of_dismissal'].value_counts()['stumped'])
    except KeyError:
        stumped='0'
    try:
        catch1=fdf[fdf['type_of_dismissal'].isin(['caught','caught and bowled','run out','stumped'])]['type_of_dismissal'].value_counts()['caught']
    except KeyError:
        catch1=0
    catch2=len(d[d['type_of_dismissal']=='caught and bowled'][d[d['type_of_dismissal']=='caught and bowled']['bowler']==player]['type_of_dismissal'])
    catch=str(catch1+catch2)

    s = ''
    for i in a[a['name'] == player].sort_values(by='year')['new_team'].unique():
        s += i + '  ,  '
    s=s.rstrip(' ')
    tpf=s.rstrip(',')
    mat_played=str(mp[mp['players']==player]['matches'].values[0])
    return jsonify(result=msgg,player=player,runs=runs,avg=avg,sr=sr,plus30=plus30,plus100=plus100,fours=fours,sixes=sixes,overs=overs,wickets=wickets,economy=economy,aveg=aveg,srt=srt,wicket3=wicket3,wicket5=wicket5,
                   runout=runout,stumped=stumped,catch=catch,image=image_base64,image1=image_base641,p1=p1,p2=p2,tpf=tpf,mat_played=mat_played)
@app.route('/teamlabel',methods=['POST'])
def teamlabel():
    team=request.form.get('team')
    if team not in w.keys():
        msg='No Trophies Yet'
    else:
        msg=w[team].lstrip()
    matches_played = str(f4[f4['Teams']==team]['Matches_played'].values[0])
    matches_won = str(f4[f4['Teams'] == team]['Matches_won'].values[0])
    matches_lost = str(f4[f4['Teams'] == team]['Matches_lost'].values[0])
    matches_no_result = str(f4[f4['Teams'] == team]['No result'].values[0])
    top4=str(t4[t4['index']==team]['Team'].values[0])
    cap=str(cc[cc['team']==team]['name'].values[0])
    maxscoredf=maxs[maxs['Team2']==team]
    maxvalue=maxscoredf['Max_score'].max()
    maxscoreyear=maxscoredf[maxscoredf['Max_score']==maxvalue]['Year'].values[0]
    minscoredf=mins[mins['Team1']==team]
    minvalue=minscoredf['Score'].min()
    minscoreyear=minscoredf[minscoredf['Score']==minvalue]['20Date'].values
    if len(minscoreyear)==1:
        min_score=str(minvalue)+'  in  '+str(minscoreyear[0])
    else:
        s=''
        for i in minscoreyear:
            s+=str(i)+'  ,  '
        s=s[:-3]
        min_score = str(minvalue) + '  in  ' + s
    hrs=str((tl[tl['Team']==team]['Top scorer'].values[0]))+'  ( '+str((tl[tl['Team']==team]['runs'].values[0]))+' )'
    hwt=str((tl[tl['Team']==team]['Top wicket taker'].values[0]))+'  ( '+str((tl[tl['Team']==team]['wickets'].values[0]))+' )'
    max_score=str(maxvalue)+'  in  '+str(maxscoreyear)
    if team not in orange.keys():
        or_cap='No one yet'
    else:
        or_cap=orange[team]+'   '
    if team not in purple.keys():
        pr_cap = 'No one yet'
    else:
        pr_cap = purple[team]+'   '

    return jsonify(hrs=hrs,hwt=hwt,trophies=msg,played=matches_played,won=matches_won,lost=matches_lost,nr=matches_no_result,top4=top4,captain=cap,or_cap=or_cap,pr_cap=pr_cap,max_score=max_score,min_score=min_score)
@app.route('/teamvsteamlabel',methods=['POST'])
def teamvsteamlabel():
    team1=request.form.get('team1')
    team2 = request.form.get('team2')
    df=((teamcomp[teamcomp['team1'].isin([team1,team2]) & teamcomp['team2'].isin([team2, team1])]))
    total_matches=str(df.shape[0])
    try:
        t1won=str(df['winning_team'].value_counts()[team1])
    except KeyError:
        t1won=0
    try:
        t2won = str(df['winning_team'].value_counts()[team2])
    except KeyError:
        t2won=0
    nr = str(df[df['winning_team'] == 'No result'].shape[0])
    t1winper=str(round((int(t1won)/int(total_matches))*100,2))+'  %'
    t2winper = str(round((int(t2won) / int(total_matches)) * 100, 2))+'  %'
    if team1 not in w.keys():
        msg1='0'
        msg1 = str(msg1) + '  / ' + str(t4[t4['index'] == team1]['Team'].values[0].split('/')[1])
    else:
        msg1=len(w[team1].strip().split())
        msg1=str(msg1)+'  / '+str(t4[t4['index']==team1]['Team'].values[0].split('/')[1])
    if team2 not in w.keys():
        msg2 = '0'
        msg2 = str(msg2) + '  / ' + str(t4[t4['index'] == team2]['Team'].values[0].split('/')[1])
    else:
        msg2 = len(w[team2].strip().split())
        msg2 = str(msg2) + '  / ' +str(t4[t4['index'] == team2]['Team'].values[0].split('/')[1])
    m1=str(t4[t4['index']==team1]['Team'].values[0])
    m2=str(t4[t4['index'] == team2]['Team'].values[0])
    if team1 not in orange.keys():
        or_cap1='0'
    else:
        or_cap1=len(orange[team1].split('     '))
    if team2 not in orange.keys():
        or_cap2 = '0'
    else:
        or_cap2 = len(orange[team2].split('     '))
    if team1 not in purple.keys():
        pur_cap1='0'
    else:
        pur_cap1=len(purple[team1].split('     '))
    if team2 not in purple.keys():
        pur_cap2 = '0'
    else:
        pur_cap2 = len(purple[team2].split('     '))
    nrr1=round(points_nrr[points_nrr['name']==team1]['nrr'].mean(),2)
    nrr2=round(points_nrr[points_nrr['name']==team2]['nrr'].mean(),2)
    d1=str(dept[dept['Team1']==team1]['dept'].values[0])
    d2=str(dept[dept['Team1']==team2]['dept'].values[0])

    return jsonify(total_matches=total_matches,t1won=t1won,t2won=t2won,no_result=nr,t1winper=t1winper,t2winper=t2winper,
                   msg1=msg1,msg2=msg2,m1=m1,m2=m2,or_cap1=or_cap1,or_cap2=or_cap2,pur_cap1=pur_cap1,pur_cap2=pur_cap2,nrr1=nrr1,nrr2=nrr2,d1=d1,d2=d2)
@app.route('/teamvsalllabel',methods=['POST'])
def teamvsalllabel():
    team=request.form.get('team')
    team_df=comp[comp['Team1']==team]
    try:
        l1 = str(team_df[team_df['Team2']=='Sunrisers Hyderabad']['Matches_played'].values[0])
        l2 = str(team_df[team_df['Team2'] == 'Sunrisers Hyderabad']['Team1won'].values[0])
        l3 = str(team_df[team_df['Team2'] == 'Sunrisers Hyderabad']['Team2won'].values[0])
        l4 = str(team_df[team_df['Team2'] == 'Sunrisers Hyderabad']['Team1Tro'].values[0])
        l5 = str(team_df[team_df['Team2'] == 'Sunrisers Hyderabad']['Team2Tro'].values[0])
    except IndexError:
        l1 = str(team_df[team_df['Team2'] == 'Chennai Super Kings']['Matches_played'].values[0])
        l2 = str(team_df[team_df['Team2'] == 'Chennai Super Kings']['Team1won'].values[0])
        l3 = str(team_df[team_df['Team2'] == 'Chennai Super Kings']['Team2won'].values[0])
        l4 = str(team_df[team_df['Team2'] == 'Chennai Super Kings']['Team1Tro'].values[0])
        l5 = str(team_df[team_df['Team2'] == 'Chennai Super Kings']['Team2Tro'].values[0])
    try:
        l6 = str(team_df[team_df['Team2'] == 'Delhi Capitals']['Matches_played'].values[0])
        l7 = str(team_df[team_df['Team2'] == 'Delhi Capitals']['Team1won'].values[0])
        l8 = str(team_df[team_df['Team2'] == 'Delhi Capitals']['Team2won'].values[0])
        l9 = str(team_df[team_df['Team2'] == 'Delhi Capitals']['Team1Tro'].values[0])
        l10 = str(team_df[team_df['Team2'] == 'Delhi Capitals']['Team2Tro'].values[0])
    except IndexError:
        l6 = str(team_df[team_df['Team2'] == 'Sunrisers Hyderabad']['Matches_played'].values[0])
        l7 = str(team_df[team_df['Team2'] == 'Sunrisers Hyderabad']['Team1won'].values[0])
        l8 = str(team_df[team_df['Team2'] == 'Sunrisers Hyderabad']['Team2won'].values[0])
        l9 = str(team_df[team_df['Team2'] == 'Sunrisers Hyderabad']['Team1Tro'].values[0])
        l10 = str(team_df[team_df['Team2'] == 'Sunrisers Hyderabad']['Team2Tro'].values[0])
        l1 = str(team_df[team_df['Team2'] == 'Chennai Super Kings']['Matches_played'].values[0])
        l2 = str(team_df[team_df['Team2'] == 'Chennai Super Kings']['Team1won'].values[0])
        l3 = str(team_df[team_df['Team2'] == 'Chennai Super Kings']['Team2won'].values[0])
        l4 = str(team_df[team_df['Team2'] == 'Chennai Super Kings']['Team1Tro'].values[0])
        l5 = str(team_df[team_df['Team2'] == 'Chennai Super Kings']['Team2Tro'].values[0])
    try:
        l11 = str(team_df[team_df['Team2'] == 'Gujarat Titans']['Matches_played'].values[0])
        l12 = str(team_df[team_df['Team2'] == 'Gujarat Titans']['Team1won'].values[0])
        l13 = str(team_df[team_df['Team2'] == 'Gujarat Titans']['Team2won'].values[0])
        l14 = str(team_df[team_df['Team2'] == 'Gujarat Titans']['Team1Tro'].values[0])
        l15 = str(team_df[team_df['Team2'] == 'Gujarat Titans']['Team2Tro'].values[0])
    except IndexError:
        l11 = str(team_df[team_df['Team2'] == 'Sunrisers Hyderabad']['Matches_played'].values[0])
        l12 = str(team_df[team_df['Team2'] == 'Sunrisers Hyderabad']['Team1won'].values[0])
        l13 = str(team_df[team_df['Team2'] == 'Sunrisers Hyderabad']['Team2won'].values[0])
        l14 = str(team_df[team_df['Team2'] == 'Sunrisers Hyderabad']['Team1Tro'].values[0])
        l15 = str(team_df[team_df['Team2'] == 'Sunrisers Hyderabad']['Team2Tro'].values[0])
        l1 = str(team_df[team_df['Team2'] == 'Chennai Super Kings']['Matches_played'].values[0])
        l2 = str(team_df[team_df['Team2'] == 'Chennai Super Kings']['Team1won'].values[0])
        l3 = str(team_df[team_df['Team2'] == 'Chennai Super Kings']['Team2won'].values[0])
        l4 = str(team_df[team_df['Team2'] == 'Chennai Super Kings']['Team1Tro'].values[0])
        l5 = str(team_df[team_df['Team2'] == 'Chennai Super Kings']['Team2Tro'].values[0])
    try:
        l16 = str(team_df[team_df['Team2'] == 'Kolkata Knight Riders']['Matches_played'].values[0])
        l17 = str(team_df[team_df['Team2'] == 'Kolkata Knight Riders']['Team1won'].values[0])
        l18 = str(team_df[team_df['Team2'] == 'Kolkata Knight Riders']['Team2won'].values[0])
        l19 = str(team_df[team_df['Team2'] == 'Kolkata Knight Riders']['Team1Tro'].values[0])
        l20 = str(team_df[team_df['Team2'] == 'Kolkata Knight Riders']['Team2Tro'].values[0])
    except IndexError:
        l16 = str(team_df[team_df['Team2'] == 'Sunrisers Hyderabad']['Matches_played'].values[0])
        l17 = str(team_df[team_df['Team2'] == 'Sunrisers Hyderabad']['Team1won'].values[0])
        l18 = str(team_df[team_df['Team2'] == 'Sunrisers Hyderabad']['Team2won'].values[0])
        l19 = str(team_df[team_df['Team2'] == 'Sunrisers Hyderabad']['Team1Tro'].values[0])
        l20 = str(team_df[team_df['Team2'] == 'Sunrisers Hyderabad']['Team2Tro'].values[0])
        l1 = str(team_df[team_df['Team2'] == 'Chennai Super Kings']['Matches_played'].values[0])
        l2 = str(team_df[team_df['Team2'] == 'Chennai Super Kings']['Team1won'].values[0])
        l3 = str(team_df[team_df['Team2'] == 'Chennai Super Kings']['Team2won'].values[0])
        l4 = str(team_df[team_df['Team2'] == 'Chennai Super Kings']['Team1Tro'].values[0])
        l5 = str(team_df[team_df['Team2'] == 'Chennai Super Kings']['Team2Tro'].values[0])
    try:
        l21 = str(team_df[team_df['Team2'] == 'Lucknow Super Giants']['Matches_played'].values[0])
        l22 = str(team_df[team_df['Team2'] == 'Lucknow Super Giants']['Team1won'].values[0])
        l23 = str(team_df[team_df['Team2'] == 'Lucknow Super Giants']['Team2won'].values[0])
        l24 = str(team_df[team_df['Team2'] == 'Lucknow Super Giants']['Team1Tro'].values[0])
        l25 = str(team_df[team_df['Team2'] == 'Lucknow Super Giants']['Team2Tro'].values[0])
    except IndexError:
        l21 = str(team_df[team_df['Team2'] == 'Sunrisers Hyderabad']['Matches_played'].values[0])
        l22 = str(team_df[team_df['Team2'] == 'Sunrisers Hyderabad']['Team1won'].values[0])
        l23 = str(team_df[team_df['Team2'] == 'Sunrisers Hyderabad']['Team2won'].values[0])
        l24 = str(team_df[team_df['Team2'] == 'Sunrisers Hyderabad']['Team1Tro'].values[0])
        l25 = str(team_df[team_df['Team2'] == 'Sunrisers Hyderabad']['Team2Tro'].values[0])
        l1 = str(team_df[team_df['Team2'] == 'Chennai Super Kings']['Matches_played'].values[0])
        l2 = str(team_df[team_df['Team2'] == 'Chennai Super Kings']['Team1won'].values[0])
        l3 = str(team_df[team_df['Team2'] == 'Chennai Super Kings']['Team2won'].values[0])
        l4 = str(team_df[team_df['Team2'] == 'Chennai Super Kings']['Team1Tro'].values[0])
        l5 = str(team_df[team_df['Team2'] == 'Chennai Super Kings']['Team2Tro'].values[0])
    try:
        l26 = str(team_df[team_df['Team2'] == 'Mumbai Indians']['Matches_played'].values[0])
        l27 = str(team_df[team_df['Team2'] == 'Mumbai Indians']['Team1won'].values[0])
        l28 = str(team_df[team_df['Team2'] == 'Mumbai Indians']['Team2won'].values[0])
        l29 = str(team_df[team_df['Team2'] == 'Mumbai Indians']['Team1Tro'].values[0])
        l30 = str(team_df[team_df['Team2'] == 'Mumbai Indians']['Team2Tro'].values[0])
    except IndexError:
        l26 = str(team_df[team_df['Team2'] == 'Sunrisers Hyderabad']['Matches_played'].values[0])
        l27 = str(team_df[team_df['Team2'] == 'Sunrisers Hyderabad']['Team1won'].values[0])
        l28 = str(team_df[team_df['Team2'] == 'Sunrisers Hyderabad']['Team2won'].values[0])
        l29 = str(team_df[team_df['Team2'] == 'Sunrisers Hyderabad']['Team1Tro'].values[0])
        l30 = str(team_df[team_df['Team2'] == 'Sunrisers Hyderabad']['Team2Tro'].values[0])
        l1 = str(team_df[team_df['Team2'] == 'Chennai Super Kings']['Matches_played'].values[0])
        l2 = str(team_df[team_df['Team2'] == 'Chennai Super Kings']['Team1won'].values[0])
        l3 = str(team_df[team_df['Team2'] == 'Chennai Super Kings']['Team2won'].values[0])
        l4 = str(team_df[team_df['Team2'] == 'Chennai Super Kings']['Team1Tro'].values[0])
        l5 = str(team_df[team_df['Team2'] == 'Chennai Super Kings']['Team2Tro'].values[0])
    try:
        l31 = str(team_df[team_df['Team2'] == 'Punjab Kings']['Matches_played'].values[0])
        l32 = str(team_df[team_df['Team2'] == 'Punjab Kings']['Team1won'].values[0])
        l33 = str(team_df[team_df['Team2'] == 'Punjab Kings']['Team2won'].values[0])
        l34 = str(team_df[team_df['Team2'] == 'Punjab Kings']['Team1Tro'].values[0])
        l35 = str(team_df[team_df['Team2'] == 'Punjab Kings']['Team2Tro'].values[0])
    except IndexError:
        l31 = str(team_df[team_df['Team2'] == 'Sunrisers Hyderabad']['Matches_played'].values[0])
        l32 = str(team_df[team_df['Team2'] == 'Sunrisers Hyderabad']['Team1won'].values[0])
        l33 = str(team_df[team_df['Team2'] == 'Sunrisers Hyderabad']['Team2won'].values[0])
        l34 = str(team_df[team_df['Team2'] == 'Sunrisers Hyderabad']['Team1Tro'].values[0])
        l35 = str(team_df[team_df['Team2'] == 'Sunrisers Hyderabad']['Team2Tro'].values[0])
        l1 = str(team_df[team_df['Team2'] == 'Chennai Super Kings']['Matches_played'].values[0])
        l2 = str(team_df[team_df['Team2'] == 'Chennai Super Kings']['Team1won'].values[0])
        l3 = str(team_df[team_df['Team2'] == 'Chennai Super Kings']['Team2won'].values[0])
        l4 = str(team_df[team_df['Team2'] == 'Chennai Super Kings']['Team1Tro'].values[0])
        l5 = str(team_df[team_df['Team2'] == 'Chennai Super Kings']['Team2Tro'].values[0])

    try:
        l36 = str(team_df[team_df['Team2'] == 'Royal Challengers Bangalore']['Matches_played'].values[0])
        l37 = str(team_df[team_df['Team2'] == 'Royal Challengers Bangalore']['Team1won'].values[0])
        l38 = str(team_df[team_df['Team2'] == 'Royal Challengers Bangalore']['Team2won'].values[0])
        l39 = str(team_df[team_df['Team2'] == 'Royal Challengers Bangalore']['Team1Tro'].values[0])
        l40 = str(team_df[team_df['Team2'] == 'Royal Challengers Bangalore']['Team2Tro'].values[0])
    except IndexError:
        l36 = str(team_df[team_df['Team2'] == 'Sunrisers Hyderabad']['Matches_played'].values[0])
        l37 = str(team_df[team_df['Team2'] == 'Sunrisers Hyderabad']['Team1won'].values[0])
        l38 = str(team_df[team_df['Team2'] == 'Sunrisers Hyderabad']['Team2won'].values[0])
        l39 = str(team_df[team_df['Team2'] == 'Sunrisers Hyderabad']['Team1Tro'].values[0])
        l40 = str(team_df[team_df['Team2'] == 'Sunrisers Hyderabad']['Team2Tro'].values[0])
        l1 = str(team_df[team_df['Team2'] == 'Chennai Super Kings']['Matches_played'].values[0])
        l2 = str(team_df[team_df['Team2'] == 'Chennai Super Kings']['Team1won'].values[0])
        l3 = str(team_df[team_df['Team2'] == 'Chennai Super Kings']['Team2won'].values[0])
        l4 = str(team_df[team_df['Team2'] == 'Chennai Super Kings']['Team1Tro'].values[0])
        l5 = str(team_df[team_df['Team2'] == 'Chennai Super Kings']['Team2Tro'].values[0])
    try:
        l41 = str(team_df[team_df['Team2'] == 'Rajasthan Royals']['Matches_played'].values[0])
        l42 = str(team_df[team_df['Team2'] == 'Rajasthan Royals']['Team1won'].values[0])
        l43 = str(team_df[team_df['Team2'] == 'Rajasthan Royals']['Team2won'].values[0])
        l44 = str(team_df[team_df['Team2'] == 'Rajasthan Royals']['Team1Tro'].values[0])
        l45 = str(team_df[team_df['Team2'] == 'Rajasthan Royals']['Team2Tro'].values[0])
    except IndexError:
        l41 = str(team_df[team_df['Team2'] == 'Sunrisers Hyderabad']['Matches_played'].values[0])
        l42 = str(team_df[team_df['Team2'] == 'Sunrisers Hyderabad']['Team1won'].values[0])
        l43 = str(team_df[team_df['Team2'] == 'Sunrisers Hyderabad']['Team2won'].values[0])
        l44 = str(team_df[team_df['Team2'] == 'Sunrisers Hyderabad']['Team1Tro'].values[0])
        l45 = str(team_df[team_df['Team2'] == 'Sunrisers Hyderabad']['Team2Tro'].values[0])
        l1 = str(team_df[team_df['Team2'] == 'Chennai Super Kings']['Matches_played'].values[0])
        l2 = str(team_df[team_df['Team2'] == 'Chennai Super Kings']['Team1won'].values[0])
        l3 = str(team_df[team_df['Team2'] == 'Chennai Super Kings']['Team2won'].values[0])
        l4 = str(team_df[team_df['Team2'] == 'Chennai Super Kings']['Team1Tro'].values[0])
        l5 = str(team_df[team_df['Team2'] == 'Chennai Super Kings']['Team2Tro'].values[0])

    try:
        l46 = str(team_df[team_df['Team2'] == 'Chennai Super Kings']['Matches_played'].values[0])
        l47 = str(team_df[team_df['Team2'] == 'Chennai Super Kings']['Team1won'].values[0])
        l48 = str(team_df[team_df['Team2'] == 'Chennai Super Kings']['Team2won'].values[0])
        l49 = str(team_df[team_df['Team2'] == 'Chennai Super Kings']['Team1Tro'].values[0])
        l50 = str(team_df[team_df['Team2'] == 'Chennai Super Kings']['Team2Tro'].values[0])
    except IndexError:
        pass


    return jsonify(l1=l1,l2=l2,l3=l3,l4=l4,l5=l5,l6=l6,l7=l7,l8=l8,l9=l9,l10=l10,l11=l11,l12=l12,l13=l13,l14=l14,l15=l15,l16=l16,l17=l17,l18=l18,l19=l19,l20=l20,l21=l21,l22=l22,l23=l23,l24=l24,l25=l25
                   ,l26=l26,l27=l27,l28=l28,l29=l29,l30=l30,l31=l31,l32=l32,l33=l33,l34=l34,l35=l35,l36=l36,l37=l37,l38=l38,l39=l39,l40=l40,l41=l41,l42=l42,l43=l43,l44=l44,l45=l45)


if __name__=='__main__':
    app.run(debug=True)