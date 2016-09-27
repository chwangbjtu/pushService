#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
    This is tool used to export videos id from maze's database.
    --help,                 print this help
    -p,                     password used to connect to mysql
    -d,                     database in which where data locates     
    -h,                     host where mysql is running
    -P,                     port where mysql is listening on
    -u,                     user used to connect to mysql
    -s,                     the start date to search video file 
    -e,                     the end date to search video file
    -f,                     the file to save video id file
"""
import time
import MySQLdb
from datetime import date, timedelta

_maze_host="localhost"
_maze_port=3306
_maze_database="ugc"
_maze_user="root"
_maze_passwd="rz33dpsk"

_maze_start=(date.today()+timedelta(-1)).isoformat()
_maze_end=date.today().isoformat()
_maze_file_name = None

def parse_option():
    global _maze_host, _maze_port, _maze_database, _maze_user, _maze_passwd, _maze_start, _maze_end, _maze_file_name
    only_help = False
    import getopt, sys
    try:
        opts, operands = getopt.getopt( sys.argv[1:], "h:d:e:f:p:P:s:u:", ["help"] )
        for opt, value in opts:
            if opt == "-h":         
                _maze_host   = (value)
            elif opt == "-d":    
                _maze_database   = value
            elif opt == "-p":  
                _maze_passwd = value
            elif opt == "-P": 
                _maze_port   = int(value)
            elif opt == "-u":
                _maze_user = value  
            elif opt == "-s":
                _maze_start = value
            elif opt == "-e":
                _maze_end = value
            elif opt == "-f":
                _maze_file_name = value
            elif opt == "help": 
                only_help = True
    except getopt.GetoptError, err:
        print err
        only_help = True
    except ValueError, err:
        print err
        only_help = True        
    except Exception, err:
        print "can not parse options\n%s" % (err)
        only_help = True 
    if only_help or not _maze_file_name:
        print __doc__ 
    return only_help
    
def produce_video_id_map(db_records, video_id_map):
        for rec in db_records:
            if not video_id_map.has_key(rec[0]):
                video_id_map[rec[0]] = []

            video_id_map[rec[0]].append(rec[1])
                
def load_video_ids(start, end):
    global _maze_host, _maze_port, _maze_database, _maze_user, _maze_passwd 
    video_id_map = {}
    dbconn = None
    dbcursor = None
    try:
        connstr = "select tid, funshion_id from ugc_file where ctime > '%s' and ctime < '%s' order by tid;" % (start, end)
        #print connstr
        dbconn = MySQLdb.connect(host = _maze_host, user = _maze_user, passwd = _maze_passwd, db = _maze_database, port = _maze_port, charset = 'utf8')
        dbcursor = dbconn.cursor(cursorclass = MySQLdb.cursors.Cursor)
        count = dbcursor.execute(connstr)
        db_records = None
        if count > 0:
            db_records = dbcursor.fetchall()

        if not db_records:
            return video_id_map
   
        produce_video_id_map(db_records, video_id_map)
    finally:
        if dbcursor:
            dbcursor.close()
        if dbconn:
            dbconn.close()
    
    return video_id_map

def write_video_id(video_id_map, filename):
    video_id_file = open(filename,'w')
    for key in video_id_map:
        line = key
        for video_id in video_id_map[key]:
            line = line + "\t" + video_id
        video_id_file.write(line+"\n")
    video_id_file.close()
        
def main():
    global _maze_start, _maze_end, _maze_file_name
    only_help =  parse_option()
    #print _maze_host, _maze_port, _maze_database, _maze_user, _maze_passwd, _maze_start, _maze_end, _maze_file_name
    if only_help or not _maze_file_name:
        return
    
    video_id_map = load_video_ids(_maze_start, _maze_end)
    
    write_video_id(video_id_map, _maze_file_name)
# yestoday=$(date -d "-1days"  +%Y-%m-%d)
# today=$(date -d "0days"  +%Y-%m-%d)   
# mysql -e "select tid, funshion_id from ugc_file where ctime > '$yestoday' and ctime < '$today' order by tid" -uroot -prz33dpsk -hlocalhost 
if __name__ == "__main__":
    main()
