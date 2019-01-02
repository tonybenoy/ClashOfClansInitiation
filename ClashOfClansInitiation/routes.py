from ClashOfClansInitiation import app
from flask import render_template, flash, redirect,url_for
from flask import request
from fractions import Fraction
from cocapi import CocApi
from ClashOfClansInitiation.forms import LoginForm, initform, searchclan
import sqlite3
from pathlib import Path
#Enter Your token Below
token = ""
coc = CocApi(token)

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", title="My apps")

@app.route('/clan/<tag>')
def clan(tag):
    lists = []
    my_file = Path("ClashOfClansInitiation/fwa.db")
    if my_file.is_file():
        pass
    else:
        conn = sqlite3.connect('ClashOfClansInitiation/fwa.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE inittable ( tag text,init text)''')
        conn.commit()
        conn.close()
    members = coc.clan_members("#"+tag)
    print (members)
    conn = sqlite3.connect('ClashOfClansInitiation/fwa.db')
    c = conn.cursor()
    c.execute('''SELECT tag FROM inittable''')
    memb = [item[0] for item in c.fetchall()]
    conn.close()
    for item in members["items"]:
        if item["tag"][1:] in memb:
            pass
        else:
            conn = sqlite3.connect('ClashOfClansInitiation/fwa.db')
            c = conn.cursor()
            c.execute('''INSERT INTO inittable (tag,init) VALUES(?,?)''',(item["tag"][1:],"New Member"))
            conn.commit()
            conn.close()
        if(int(item["donationsReceived"])!=0):
            donation_ratio=int(item["donations"])/int(item["donationsReceived"])
        else:
            donation_ratio = 0
        if donation_ratio>=0.5:
            donation_ratio = "Maintained"
        else:
            donation_ratio = "Not Maintained"
        if (item["role"]=="admin"):
            item["role"] = "Elder"
        elif(item["role"]=="coLeader"):
            item["role"] = "Co Leader"
        elif (item["role"]=="leader"):
            item["role"] = "Leader"
        elif (item["role"]=="member"):
            item["role"] = "Member"
        conn = sqlite3.connect('ClashOfClansInitiation/fwa.db')
        c = conn.cursor()
        c.execute('''select init from inittable where tag = ?''',(item["tag"][1:],))
        init = c.fetchone()[0]
        conn.close()
        url = "http://kuilin.net/cc_n/member.php?tag=%23"+item["tag"][1:]
        cocurl="clashofclans://action=OpenPlayerProfile&tag="+item["tag"][1:]
        lists.append({"clantag":tag,"tag":str(item["tag"]),"name":str(item["name"]),"role":str(item["role"]),"previousClanRank":str(item["previousClanRank"]),"expLevel":str(item["expLevel"]),"trophies":str(item["trophies"]),"url":str(url),"clanRank":str(item["clanRank"]),"donationsReceived":str(item["donationsReceived"]),"donations":str(item["donations"]),"donation_ratio":str(donation_ratio),"init":str(init),"cocurl":str(cocurl)})
        conn.close ()
    title = "FARM AND LIVE"
    return render_template("clan.html", title=title, posts=lists)

@app.route('/init', methods=['GET', 'POST'])
def init():
    form = LoginForm()
    if form.validate_on_submit():
        a=coc.players(form.tag.data)
        print(a["name"])
        return redirect(url_for('start',tag=form.tag.data[1:],post=a["name"]))
    return render_template('init.html', title='Initiation', form=form)

@app.route('/clans', methods=['GET', 'POST'])
def clans():
    form = searchclan()
    if form.validate_on_submit():
        return redirect(url_for('clan',tag=form.clantag.data[1:]))
    return render_template('clans.html', title='Find Clan', form=form)

@app.route('/start/<tag>/<post>',methods=['GET', 'POST'])
def start(tag,post):
    initForm = initform()
    print(initForm.validate_on_submit())
    if initForm.validate_on_submit():
        print("Inside")
        if str(initForm.mindon.data)=="1200" and str(initForm.donwar.data)=="0":
            conn = sqlite3.connect('ClashOfClansInitiation/fwa.db')
            c = conn.cursor()
            c.execute(''' UPDATE inittable SET init = 'Yes' WHERE tag = ?''',(tag,))
            conn.commit()
            c.execute('''SELECT * FROM inittable''')
            print(c.fetchall())
            conn.close()
            return render_template('initq.html', title='Initiate',post="1")
        else:
            print("No")
            return render_template('initq.html', title='Initiate',post="0")
    return render_template('start.html', title='Initiate',form=initForm)
