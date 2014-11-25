#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime as _dt
import gpxpy
import math
from scipy import signal
import yaml
import jinja2

def floor_time(tm):
    """http://stackoverflow.com/questions/3463930/how-to-round-the-minute-of-a-datetime-object-python"""
    return tm - _dt.timedelta(minutes = tm.minute % 15,
                              seconds = tm.second,
                              microseconds = tm.microsecond)

def summarize_tracks(gpx):
    for t in gpx.tracks:
        distance = t.length_3d() * 0.000621371
        time = float(t.get_duration())/3600
        speed = 0.0 if time == 0.0 else distance/time
        count = len(t.segments)
        print("%s (%d):\n\tDistance: %.2f miles\n\tTime: %.2f hours\n\t"
              "Speed: %.2f MPH" %(t.name, count, distance, time, speed))

def time_dictionary(time_s):
    time_d = {
        'hours': int(math.floor(time_s / 3600)),
        'minutes': int(math.floor((time_s % 3600) / 60)),
        'seconds': int(time_s % 60)
    }
    return time_d

def format_time(time_s):
    if not time_s:
        return 'n/a'
    time_d = time_dictionary(time_s)
    time_str = '{hours:02d}:{minutes:02d}:{seconds:02d}'.format(**time_d)

    return time_str

def mod_summarize_tracks(gpx):
    tracks = {}
    for t in gpx.tracks:
        summary = {}
        m = t.get_moving_data()
        if m.moving_time == 0:
            continue
        summary['moving_time'] = format_time(m.moving_time)
        summary['stopped_time'] = format_time(m.stopped_time)
        moving_distance = round(0.0621371 * m.moving_distance) / 100.
        summary['moving_distance'] = moving_distance
        summary['avg_speed'] = round(moving_distance / m.moving_time * 360000) / 100.
        tracks[t.name.replace(' ', '_')] = summary
    print yaml.dump(tracks, default_flow_style = False)

def load_template(template_file):
    template_loader = jinja2.FileSystemLoader(searchpath = "./")
    template_env = jinja2.Environment(loader = template_loader)
    return template_env.get_template(template_file)

def save_speed(track):
    header = load_template('template.gpi')
    track_name_s = track.name.replace(' ', '-')

    start_time, end_time = track.get_time_bounds()
    start_time = floor_time(start_time)
    end_time = floor_time(end_time)

    file_name = track_name_s + u'-speed.gpi'
    speed_file = open(file_name, 'w')
    plot_details = {
        'xlabel': 'Time [hh:mm]',
        'ylabel': 'Speed [mph]',
        'title': 'Speed',
        'start_time': start_time.isoformat(),
        'end_time': end_time.isoformat(),
    }
    speed_file.write(header.render(plot_details))

    file_name = track_name_s + u'-elevation.gpi'
    elevation_file = open(file_name, 'w')
    plot_details = {
        'xlabel': 'Time [hh:mm]',
        'ylabel': 'Elevation [ft]',
        'title': 'Elevation',
        'start_time': start_time.isoformat(),
        'end_time': end_time.isoformat(),
    }
    elevation_file.write(header.render(plot_details))

    for s in track.segments:
        (t, speed, elevation) = handle_segment(s)
        #code.interact(local=locals())
        f_speed = filter_speed(speed)

        data_format = '{}\t{:4f}\n'

        for (i, x) in enumerate(f_speed):
            speed_file.write(data_format.format(t[i], x))
        speed_file.write('\n\n')

        for (i,x) in enumerate(elevation):
            elevation_file.write(data_format.format(t[i], x))
        elevation_file.write('\n\n')
    speed_file.close()
    elevation_file.close()


def handle_segment(s):
    speed = [0] * (len(s.points))
    timestamp = [''] * len(speed)
    elevation = [0] * (len(speed))

    prev_p = s.points[0]
    for p,i in s.walk():
        # calculate speed in m/s
        x = prev_p.speed_between(p)
        speed[i] = 2.23694 * x if x else 0.0
        #timestamp[i] = prev_p.time_difference(p) + timestamp[i-1]
        timestamp[i] = p.time.isoformat()
        elevation[i] = 3.28084 * p.elevation
        prev_p = p

    return (timestamp, speed, elevation)

def filter_speed(x):
    (b, a) = signal.butter(2, 0.1)
    y = signal.lfilter(b, a, x)

    return y

def main(args):
    gpx_file = open(args[0], 'r')
    gpx = gpxpy.parse(gpx_file)
    mod_summarize_tracks(gpx)
    #summarize_tracks(gpx)
    for t in gpx.tracks:
        save_speed(t)

if __name__ == '''__main__''':
    import sys
    main(sys.argv[1:])
