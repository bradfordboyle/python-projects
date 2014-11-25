CREATE TABLE employers(
	id INTEGER PRIMARY KEY,
	location TEXT,
	organization TEXT,
	url TEXT,
	international INTEGER,
	coop INTEGER,
	permanent INTEGER
);

CREATE TABLE majors(
	id INTEGER PRIMARY KEY,
	title TEXT
);

CREATE TABLE employers_majors(
	id INTEGER PRIMARY KEY,
	e_id INTEGER NOT NULL,
	m_id INTEGER NOT NULL,
	FOREIGN KEY(e_id) REFERENCES employers(id),
	FOREIGN KEY(m_id) REFERENCES majors(id)
);
