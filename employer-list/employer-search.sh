#!/usr/bin/env bash

db_init() {
	python employer-list.py > populate.sql
	sqlite3 test.db < employer-list.sql
	sqlite3 test.db < populate.sql
}

test -f test.db || db_init
QUERY="SELECT organization,url,location FROM employers JOIN employers_majors ON employers_majors.e_id = employers.id JOIN majors on employers_majors.m_id = majors.id WHERE majors.title = '${1}' AND permanent = 1;"
sqlite3 test.db ".mode columns; .width 30 10 10;${QUERY}"
