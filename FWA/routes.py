from FWA import app
from flask import render_template, flash, redirect,url_for
from flask import request
from fractions import Fraction
from FWA.cocapi import cocapi
from FWA.forms import LoginForm
import sqlite3
from pathlib import Path


@app.route('/')
def index():
    token = Your token
    coc = cocapi(token)
    list = []
    my_file = Path("FWA/fwa.db")
    if my_file.is_file():
        pass
    else:
        conn = sqlite3.connect('FWA/fwa.db')
        c = conn.cursor()
        #c.execute('''CREATE TABLE members ( tag text, role text,name text,donationsReceived text,expLevel text,trophies text, url text,clanRank text, previousClanRank text,donations text,donation_ratio text,init text,cocurl text)''')
        c.execute('''CREATE TABLE inittable ( tag text,init text)''')
        conn.commit()
        conn.close()
    members = coc.clan_members("#PU8J2RQ")
    conn = sqlite3.connect('FWA/fwa.db')
    c = conn.cursor()
    c.execute('''SELECT tag FROM inittable''')
    memb = [item[0] for item in c.fetchall()]
    conn.close()
    for item in members["items"]:
        if item["tag"][1:] in memb:
            pass
        else:
            conn = sqlite3.connect('FWA/fwa.db')
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
        conn = sqlite3.connect('FWA/fwa.db')
        c = conn.cursor()
        c.execute('''select init from inittable where tag = ?''',(item["tag"][1:],))
        init = c.fetchone()[0]
        conn.close()
        url = "http://kuilin.net/cc_n/member.php?tag=%23"+item["tag"][1:]
        cocurl="clashofclans://action=OpenPlayerProfile&tag="+item["tag"][1:]
        list.append({"tag":str(item["tag"]),"name":str(item["name"]),"role":str(item["role"]),"previousClanRank":str(item["previousClanRank"]),"expLevel":str(item["expLevel"]),"trophies":str(item["trophies"]),"url":str(url),"clanRank":str(item["clanRank"]),"donationsReceived":str(item["donationsReceived"]),"donations":str(item["donations"]),"donation_ratio":str(donation_ratio),"init":str(init),"cocurl":str(cocurl)})
        conn.close ()
    title = "FARM AND LIVE"
    return render_template("index.html", title=title, posts=list)

@app.route('/init', methods=['GET', 'POST'])
def init():
    form = LoginForm()
    if form.validate_on_submit():
        if form.password.data=="qwerty":
            conn = sqlite3.connect('FWA/fwa.db')
            c = conn.cursor()
            c.execute(''' UPDATE inittable SET init = 'Yes' WHERE tag = ?''',(form.tag.data[1:],))
            conn.commit()
            c.execute('''SELECT * FROM inittable''')
            print(c.fetchall())
            conn.close()
            return redirect('/')
        else:
            return redirect('/notadmin')
    return render_template('init.html', title='Initiation', form=form)

@app.route('/notadmin')
def wrong():
    return render_template('notadmin.html', title='Incorrect')