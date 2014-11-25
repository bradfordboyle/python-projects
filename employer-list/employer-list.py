#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xlrd

ADD_EMPLOYER = 'INSERT INTO employers VALUES({id}, "{tbl}", "{org}", "{url}", {intl}, {coop}, {perm});'
ADD_MAJOR = 'INSERT INTO majors VALUES({}, "{}");'
ADD_LINK = 'INSERT INTO employers_majors VALUES(null, {}, {});'


wb = xlrd.open_workbook('employer list.xls')
# should only be a single sheet
sheet = wb.sheets()[0]
num_employers = (sheet.nrows - 1) / 2

seen_majors = set([])
major_ids = {}
m_id = 0
for i in range(num_employers):
    row = 2 * i + 1
    e = {
        'id': i + 1,
        'tbl': sheet.cell(row, 0).value,
        'org': sheet.cell(row, 1).value,
        'url': sheet.hyperlink_map.get((row, 2)).url_or_path if sheet.hyperlink_map.get((row, 2)) else sheet.cell(row, 2).value,
        'coop': int('Co-op' in sheet.cell(row, 3).value),
        'perm': int('Permanent' in sheet.cell(row, 3).value),
        'intl': int(sheet.cell(row, 4).value == 'yes')
    }
    print(ADD_EMPLOYER.format(**e))
    majors = set(sheet.cell(row + 1, 1).value.split(', '))
    for m in majors - seen_majors:
        m_id += 1
        major_ids[m] = m_id
        print(ADD_MAJOR.format(m_id, m))
    seen_majors |= majors

    for m in majors:
        print(ADD_LINK.format(e['id'], major_ids[m]))
