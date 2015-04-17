#!/usr/bin/env python

import optparse, os, pdb, json,urllib2,sys,time,pytz,sys
from datetime import datetime
from tzlocal import get_localzone
reload(sys);
#os.system('clear')
sys.setdefaultencoding("utf8")


local_tz = get_localzone()

try:
	p = optparse.OptionParser()
except:
	p = []


year=time.localtime()[0]
month=time.localtime()[1]
day=time.localtime()[2]
hour=time.localtime()[3]
minute=time.localtime()[4]
second=time.localtime()[5]

# Get UTC offset of computer

if (time.localtime().tm_isdst == 0):
	tz=time.tzname[0]
else:
	tz=time.tzname[1]



# pdb.set_trace()
p.add_option('--date','-d',default=str(month)+'/'+str(day)+'/'+str(year),help='''mlb.py [no options]: Prints all box scores for games today. mlb.py -d '04/23/2013': Prints all box scores for only date listed. mlb.py -d '04/23/2012' -t 'NYY': Prints box score for selected team on selected date''')
p.add_option('--teams','-t',default='ALL',help='''mlb.py [no options]: Prints all box scores for games today. mlb.py -t 'NYY': Prints box score for selected team for today. mlb.py -d '04/23/2012' -t 'NYY': Prints box score for selected team on selected date''')
options, arguments = p.parse_args()



game_year=str(options.date.split('/')[2])
game_month=str(options.date.split('/')[0]).rjust(2, '0')
game_day=str(options.date.split('/')[1]).rjust(2, '0')
# pdb.set_trace()

# game_year="2013"
# game_month="04"
# game_day="21"



# print 'http://gd2.mlb.com/components/game/mlb/year_'+game_year+'/month_'+game_month+'/day_'+game_day+'/master_scoreboard.json'

json_data = urllib2.urlopen('http://gd2.mlb.com/components/game/mlb/year_'+game_year+'/month_'+game_month+'/day_'+game_day+'/master_scoreboard.json')

# json_data = urllib2.urlopen('https://dl.dropboxusercontent.com/u/4178416/json.txt')

data = json.load(json_data)


#f=open('json.txt','r')
#data = json.load(f)





#pprint(data)

# game_day=data["data"]["games"]["day"]


#pprint(data["data"]["games"]["game"][0]["away_team_name"])

away_team_names=[]
home_team_names=[]
away_team_city=[]
home_team_city=[]
#away_name_abbrev=[]
#home_name_abbrev=[]
away_time=[]
home_time=[]
away_time_zone=[]
home_time_zone=[]
away_win=[]
home_win=[]
away_loss=[]
home_loss=[]


# pdb.set_trace()
for team in data["data"]["games"]["game"]:
   if (team["away_name_abbrev"].lower() == options.teams.lower() or team["home_name_abbrev"].lower() == options.teams.lower() or options.teams == 'ALL'):
	   away_team_names.append(team["away_team_name"])
	   home_team_names.append(team["home_team_name"])
	   away_team_city.append(team["away_team_city"])
	   home_team_city.append(team["home_team_city"])
	#   away_name_abbrev.append(team["away_name_abbrev"])
	#   home_name_abbrev.append(team["home_name_abbrev"])
	   away_time.append(team["away_time"])
	   home_time.append(team["home_time"])
	   away_time_zone.append(team["away_time_zone"])
	   home_time_zone.append(team["home_time_zone"])
	   away_win.append(team["away_win"])
	   home_win.append(team["home_win"])
	   away_loss.append(team["away_loss"])
	   home_loss.append(team["home_loss"])

	#   print "linescore for "+team["away_name_abbrev"]+" at "+team["home_name_abbrev"]
	#   print "Status"
	#   print team["status"]["status"]
	   if (team["status"]["status"] == "In Progress" or team["status"]["status"] == "Final"):

		   inning = team["status"]["inning"]
		   if (inning == "1"):
			   inning_suffix = "st"
		   elif (inning == "2"):
			   inning_suffix = "nd"
		   elif (inning == "3"):
			   inning_suffix = "rd"
		   elif (int(inning) > 3):
			   inning_suffix = "th"

		   if (team["status"]["status"] == "Final"):
			   top_bottom = "Final"
		   else:
			   if (team["status"]["top_inning"] == "Y"):
				   top_bottom = "Top"+" "+inning+inning_suffix
			   else:
				   top_bottom = "Bottom"+" "+inning+inning_suffix




	#       print "It's currently the "+top_bottom+" of the "+inning+inning_suffix

		   runs_away = team["linescore"]["r"]["away"]
		   runs_home = team["linescore"]["r"]["home"]
		   errors_away = team["linescore"]["e"]["away"]
		   errors_home = team["linescore"]["e"]["home"]
		   hits_away  = team["linescore"]["h"]["away"]
		   hits_home  = team["linescore"]["h"]["home"]
		   home_runs_away = team["linescore"]["hr"]["away"]
		   home_runs_home = team["linescore"]["hr"]["home"]
		   stolen_bases_away  = team["linescore"]["sb"]["away"]
		   stolen_bases_home  = team["linescore"]["sb"]["home"]
		   strike_outs_away = team["linescore"]["so"]["away"]
		   strike_outs_home = team["linescore"]["so"]["home"]


	#       print "runs away: "+runs_away
	#       print "runs home: "+runs_home
	#       print "errors away: "+errors_away
	#       print "errors home: "+errors_home
	#       print "hits away: "+hits_away
	#       print "hits home: "+hits_home
	#       print "home runs away: "+home_runs_away
	#       print "home runs home: "+home_runs_home
	#       print "stolen bases away: "+stolen_bases_away
	#       print "stolen bases home: "+stolen_bases_home
	#       print "strike outs away: "+strike_outs_away
	#       print "strike outs home: "+strike_outs_home


	#       print team["linescore"]["inning"]
		   box_away = []
		   box_home = []
		   for score in team["linescore"]["inning"]:
			   try:
				   if (score["away"] == ""):
					   score_away=" "
				   else:
					   score_away = score["away"]
			   except:
				   score_away=" "
			   box_away.append(score_away)

			   try:
				   if (score["home"] == ""):
					   score_home=" "
				   else:
					   score_home = score["home"]
			   except:
				   score_home=" "
			   box_home.append(score_home)


		   # pdb.set_trace()
		   roof = "__"
		   pipe = "|"
		   floor = u"\u203E"u"\u203E"
		   low_line = u"\u0332"


		   if (int(runs_away) >= 10 or int(runs_home) >= 10):
			   run_R="  R"
		   else:
			   run_R=" R"
		   if (int(hits_away) >= 10 or int(hits_home) >= 10):
			   hit_H="  H"
		   else:
			   hit_H=" H"
		   if (int(errors_away) >= 10 or int(errors_home) >= 10):
			   err_E="  E"
		   else:
			   err_E=" E"


		   if (int(runs_away) >= 10 and int(runs_home) < 10):
			   runs_home=" "+runs_home
		   if (int(runs_home) >= 10 and int(runs_away) < 10):
			   runs_away=" "+runs_away

		   if (int(hits_away) >= 10 and int(hits_home) < 10):
			   hits_home=" "+hits_home
		   if (int(hits_home) >= 10 and int(hits_away) < 10):
			   hits_away=" "+hits_away

		   if (int(errors_away) >= 10 and int(errors_home) < 10):
			   errors_home=" "+errors_home
		   if (int(errors_home) >= 10 and int(errors_away) < 10):
			   errors_away=" "+errors_away

		   if (len(team["away_name_abbrev"]) < 3):
			   away_name_abbrev = team["away_name_abbrev"]+" "
		   else:
			   away_name_abbrev = team["away_name_abbrev"]
		   if (len(team["home_name_abbrev"]) < 3):
			   home_name_abbrev = team["home_name_abbrev"]+" "
		   else:
			   home_name_abbrev = team["home_name_abbrev"]


		   out0 = []
		   out1 = []
		   out2 = []
		   out3 = []
		   out4 = []
		   index=1
		   index2=0
		   for box in box_home:
			   box_a=box_away[index2]
			   box_h=box_home[index2]

			   if (box_a >= 10 and box_h < 10):
				   box_h=" "+box_h
				   inn = str(index)+low_line+" "

			   if (box_h >= 10 and box_a < 10):
				   box_a=" "+box_a
				   inn = str(index)+low_line+" "

			   if (box_h >= 10 and box_a >= 10):
				   inn = str(index)+low_line+" "

			   if (index > 9):
				   inn = str(index)+low_line
				   box_a=" "+box_a
				   box_h=" "+box_h
			   else:
				   inn = str(index)+low_line

			   if (str(box_home[index2]) == " " and str(team["status"]["status"]) == "Final"):
				box_h="X"


			   if (index == 1):
				   out1.append("    "+inn)
				   out2.append(away_name_abbrev+pipe+box_a)
				   out3.append(home_name_abbrev+pipe+box_h)
			   elif (index > 1 and index < len(box_home)):
				   out1.append(" "+inn)
				   out2.append(pipe+box_a)
				   out3.append(pipe+box_h)
			   elif (index == len(box_home)):
				   out1.append(" "+inn+"  "+run_R+low_line+hit_H+low_line+err_E+low_line)
				   out2.append(pipe+box_a+pipe+" "+pipe+runs_away+pipe+hits_away+pipe+errors_away+pipe)
				   out3.append(pipe+box_h+pipe+" "+pipe+runs_home+pipe+hits_home+pipe+errors_home+pipe)
			   index=index+1
			   index2=index2+1


		   out1 = "".join(out1)
		   out2 = "".join(out2)
		   out3 = "".join(out3)
		   
		   localFormat = "%Y-%m-%d %H:%M"
# 		   pdb.set_trace()
		   localmoment_unaware = datetime.strptime(game_year+'-'+game_month+"-"+game_day+' '+str(team["away_time"]),localFormat)
# 		   pdb.set_trace()
		   if str(team["away_time_zone"]) == 'CT' or str(team["away_time_zone"]) == 'CST' or str(team["away_time_zone"]) == 'CDT':
		   		localtimezone = pytz.timezone('US/Central')
		   if str(team["away_time_zone"]) == 'PT' or str(team["away_time_zone"]) == 'PST' or str(team["away_time_zone"]) == 'PDT':
		   		localtimezone = pytz.timezone('US/Pacific')    
		   if str(team["away_time_zone"]) == 'ET' or str(team["away_time_zone"]) == 'EST' or str(team["away_time_zone"]) == 'EDT':
		   		localtimezone = pytz.timezone('US/Eastern')
		   if str(team["away_time_zone"]) == 'MT' or str(team["away_time_zone"]) == 'MST' or str(team["away_time_zone"]) == 'MDT':
		   		localtimezone = pytz.timezone('US/Mountain')
		   
		   localmoment = localtimezone.localize(localmoment_unaware)
		   local_game_time = localmoment.astimezone(pytz.timezone(str(local_tz)))
		   local_game_time = local_game_time.strftime('%H:%M')

# 		   pdb.set_trace()
		   print team["away_name_abbrev"]+"("+str(team["away_win"])+"-"+str(team["away_loss"])+")" +" @ "+team["home_name_abbrev"]+"("+str(team["home_win"])+"-"+str(team["home_loss"])+")" +" "+top_bottom
		   print out1
		   print out2
		   print out3
		   print options.date+'   '+local_game_time + ' '+tz
		   print " "


	   localFormat = "%Y-%m-%d %H:%M"
	   localmoment_unaware = datetime.strptime(game_year+'-'+game_month+"-"+game_day+' '+str(team["away_time"]),localFormat)
	   if str(team["away_time_zone"]) == 'CT' or str(team["away_time_zone"]) == 'CST' or str(team["away_time_zone"]) == 'CDT':
	   		localtimezone = pytz.timezone('US/Central')
	   if str(team["away_time_zone"]) == 'PT' or str(team["away_time_zone"]) == 'PST' or str(team["away_time_zone"]) == 'PDT':
	   		localtimezone = pytz.timezone('US/Pacific')    
	   if str(team["away_time_zone"]) == 'ET' or str(team["away_time_zone"]) == 'EST' or str(team["away_time_zone"]) == 'EDT':
	   		localtimezone = pytz.timezone('US/Eastern')
	   if str(team["away_time_zone"]) == 'MT' or str(team["away_time_zone"]) == 'MST' or str(team["away_time_zone"]) == 'MDT':
	   		localtimezone = pytz.timezone('US/Mountain')
# 	   pdb.set_trace()	   
	   localmoment = localtimezone.localize(localmoment_unaware)
	   local_game_time = localmoment.astimezone(pytz.timezone(str(local_tz)))
	   local_game_time = local_game_time.strftime('%H:%M')
	   if (team["status"]["status"] == "Preview" or team["status"]["status"] == "Pregame"):
		   print team["away_name_abbrev"]+" ("+str(team["away_win"])+"-"+str(team["away_loss"])+")" +" @ "+team["home_name_abbrev"]+" ("+str(team["home_win"])+"-"+str(team["home_loss"])+") "+local_game_time +" "+tz
		   print " "




   pdb.set_trace()

#print "away team names"
#print away_team_names
#print "home team names"
#print home_team_names
#print "home team coty"
#print away_team_city
#print "home team city"
#print home_team_city
#print "away team abbrev"
#print away_name_abbrev
#print "home team abbrev"
#print home_name_abbrev
#print "away_time"
#print away_time
#print "home_time"
#print home_time
#print "away_time_zone"
#print away_time_zone
#print "home_time_zone"
#print home_time_zone
#print "away_loss"
#print away_loss
#print "home_loss"
#print home_loss
#print "away_win"
#print away_win
#print "home_win"
#print home_win

input_team_abbrev='NYY'

# need to include case for double header and when not playing that day
#away_index=[]
#for team in away_name_abbrev:
#   if (input_team_abbrev.lower == team.lower):
#       print "You have selected: "+team
#   else:
#       print "Team not found in away list, must be home. checking..."

#home_index=[]
#for team in home_name_abbrev:
#   if (input_team_abbrev.lower == team.lower):
#       print "You have selected: "+team
#   else:
#       print "Team not Found at All...something went wrong"



