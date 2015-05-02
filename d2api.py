#!/usr/bin/env python

import bottle
import MySQLdb as mysql
import datetime
import dateutil.parser

from dota2py import api,data

app = application = bottle.Bottle()
@app.route('/hello/<name:int>')
def hello(name):
	return 'Hello %d'%name

# Finished = 0 for matches that are yet to be done
@app.route('/match/<id:int>')
def match(id):
	parent_dict = {}
	try:
		conn = mysql.connect(host="localhost",user="root",passwd="samidh",db="jdmatches")
		cursor = conn.cursor()
		cursor.execute('SELECT id,teamOne,teamOneCnt,teamTwo,teamTwoCnt,ETA FROM jd_matches WHERE  id > %s AND ETA > UTC_TIMESTAMP()',(id,))
		data_rows = cursor.fetchall()
		
		count = 0
		match_data_list = []
		for row in data_rows:
			child_dict = {}
			child_dict['id'] = row[0]
			child_dict['t1'] = row[1]
			child_dict['t1c'] = row[2]
			child_dict['t2'] = row[3]
			child_dict['t2c'] = row[4]
			child_dict['ETA'] = row[5].strftime('%Y-%m-%d %H:%M:%S')
			match_data_list.append(child_dict)
			count = count + 1
		parent_dict["total"] = count
		parent_dict["matches"] = match_data_list
		parent_dict["success"] = True
	except mysql.Error,e:
		
		parent_dict["success"] = False
	return parent_dict

@app.route('/match/live')
def match_live():
	# parent_dict = {}
	# match_data_list = []
	live_games = api.get_live_league_games()
	# parent_dict["success"] = True
	# for games in live_games["result"]["games"]:
	# 	child_dict = {}
	#     try:                                    
	#         child_dict['radiant_team'] = games["radiant_team"]["team_name"]
	#         child_dict['dire_team'] = games["dire_team"]["team_name"]
	#         child_dict['match_id'] = games["match_id"]
	#         match_data_list.append(child_dict)
	#     except KeyError:
	#         parent_dict["success"] = False
	# parent_dict["matches"] = match_data_list

	return live_games


if __name__ == '__main__':
    app.run(host='localhost',
        port=8000, default=True)



