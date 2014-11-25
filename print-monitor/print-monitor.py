#!/usr/bin/evn python
import ConfigParser
import logging
import lxml.html
import os.path
import requests
import rrdtool

def _column_headers(table):
    col_headers = table.xpath("tr/th/div/text()")
    return [i.lower() for i in col_headers]

def _extract_table(doc):
    table = doc.xpath('''//table[@id="tbl-1851"]''')
    return table[0]

def _extract_rows(table):
    return table.xpath("tr[td]")

def _extract_cols(tr):
    cols = tr.xpath("td/div/text()")
    return [i.lower() for i in cols]

def _parse_table(table):
    col_headers = _column_headers(table)
    rows = _extract_rows(table)
    table_dict = {}
    for tr in rows:
        col_values = _extract_cols(tr)
        table_dict[col_values[0]] = dict(zip(col_headers, col_values[1:]))
    return table_dict

def _load_html_from_file(path):
    f = open(path, 'r')
    return f.read()

def fetch_printer_usage(url, cafile):
    r = requests.get(url, verify=False)
    doc = lxml.html.fromstring(r.content)
    table = _extract_table(doc)
    return _parse_table(table)


def _create_rrd(rrd_path, config):
    step = config.get("create", "step")
    sources = config.get("create", "sources")
    DS = sources.split('|')
    archives = config.get("create", "archives")
    RRA = archives.split('|')
    try:
        rrdtool.create(rrd_path, "--step", step, DS, RRA)
    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
        raise e

def _update_rrd(rrd_path, config, paper_usage):
    log_msg = "_update_rrd {0}".format(rrd_path)
    logging.debug(log_msg)
    template = config.get("update", "template")
    update_fmt = config.get("update", "fmt")
    rrdtool.update(rrd_path, "--template", template,
                   update_fmt.format(**paper_usage))


def _munger(paper_usage):
    p = {}
    for k in paper_usage:
        p[k] = paper_usage[k].replace(',', '')
    return p


def main():
    # load config
    config = ConfigParser.RawConfigParser()
    config.read('print-monitor.cfg')

    # set up logging
    logfile = config.get("logging", "logfile")
    level = config.get("logging", "level")
    loglevel = getattr(logging, level.upper())
    logformat = config.get("logging", "format")
    logging.basicConfig(filename = logfile, level = loglevel, format=logformat)

    rrd_path = config.get("general", "path")
    if not os.path.isfile(rrd_path):
        log_msg = "RRD does not exist..."
        logging.warn(log_msg)
        _create_rrd(rrd_path, config)

    usage_url = config.get("general", "usage_url")
    cafile = config.get("general", "cafile")
    printer_usage = fetch_printer_usage(usage_url, cafile)

    paper_size = config.get("general", "paper_size")
    paper_usage = _munger(printer_usage[paper_size])
    _update_rrd(rrd_path, config, paper_usage)

if __name__ == "__main__":
    main()
