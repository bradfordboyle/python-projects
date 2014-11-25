#!/bin/bash
WEEK=${1}
PATH=$PATH:.

BuildYahooURL.py --week ${WEEK} --uid 42749 --position all --output-dir week${WEEK} --cookie cookie.txt
Scratch.py --week ${WEEK} > week${WEEK}/FantasyFootballData.csv
BuildLPModel.py --file week${WEEK}/FantasyFootballData.csv > week${WEEK}/input.lp
lp_solve -S2 < week${WEEK}/input.lp > week${WEEK}/solution.txt
mkdir -p week$((WEEK+1))
touch week$((WEEK+1))/__init__.py
VerifySolution.py --file week${WEEK}/FantasyFootballData.csv --sol week${WEEK}/solution.txt > week$((WEEK+1))/team.py

