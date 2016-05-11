
CREATE TABLE IF NOT EXISTS Ticket(
	symbol varchar(20) NOT NULL,
	date DATE,
	time TIME, 
	Open DOUBLE,
	High DOUBLE,
	Low DOUBLE,
	Close DOUBLE,
	Volume int
);
