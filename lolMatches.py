import datetime as dt
from mwrogue.esports_client import EsportsClient

Lolsite = EsportsClient('lol')

def getMatches():
	date = dt.datetime.utcnow().date()
	date1 = (dt.datetime.utcnow() + dt.timedelta(1)).date()
	response2 = Lolsite.cargo_client.query(tables="MatchSchedule",
										   fields="Team1, Team2, ShownName, DateTime_UTC",
										   limit="max",
										   where="DateTime_UTC >= '" + str(date) + "' AND DateTime_UTC <= '" + str(
											   date1) + "'")

	interere = ['LEC', 'LCS', 'LPL', 'LCK', 'EM', 'MSI', 'Worlds']
	TODAY_MATCHES = list()
	for row in response2:
		if any(ext in row['ShownName'] for ext in interere):
			TODAY_MATCHES.insert(len(TODAY_MATCHES), row)
	return TODAY_MATCHES
