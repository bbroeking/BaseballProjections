# BaseballProjections

Missing the data needed for the engine to run
The folder architechture I'm using is:

    Stores the lineups broken into individual players
	Lineups/

    Store the lines from the past 3 years. Can be populated with scapers.
	MLBLines/

    Stores the totals from the past 3 years. Can be poplated with the scrapers.
	MLBTotals/

    Stores the ownership percentages of each of the players in each contests, each day
	Ownerships/

    Currently working on implementation, stand by
	Steamer600Batter.csv

    Currently working on implementation, stand by
	Steamer600Pitcher.csv
	
    Raw Draftkings data, not needed
    data/

    All this data is contained in a SQLite database, I know.. I know, I should use something better, I'm working on it
	src/Database/