print-monitor
=============

Small utility to load up an HP printer's usage page and scrape the number of
duplex and simplex printed pages. The data is stored in a round-robin database
(RRD) for producing plots. You can use this to get a sense of when most your
printing happens---very helpful if you have printing fiend as a lab mate.

To use, add the following to your crontab:

    @hourly cd <path-to-print-monitor> && <path-to-python> print-monitor.py

Specifying the python path allows you to use a virtualenv python
