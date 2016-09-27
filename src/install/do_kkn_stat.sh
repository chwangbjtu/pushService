#/bin/sh
DIR=`dirname "$0"`
$DIR/find_kkn.sh > $DIR/kkn-stat.csv
python $DIR/sendmail.py "kkn daily stat" "wangli1@funshion.com;lisz@funshion.com;shangym@funshion.com;qiaojw@funshion.com;shiwg@funshion.com;lihh@funshion.com"  $DIR/kkn-stat.csv
