
days=1
if [ $# == 1 ] ; then
    days=$1
fi

end=$(date -d "-0days"  +%Y%m%d)
beg=$(date -d "$end -${days}days" +%Y%m%d)
echo 时间, 国内, 国际, 社会, 上海, 军事, 看看出品, 财经, 法制,  总数

while(($beg<$end))
do
    day=$(date -d "$beg" +%Y-%m-%d)
    /usr/local/mysql/bin/mysql -h localhost  -u root -prz33dpsk -e "set names utf8; select site, tags  from ugc.ugc_video where site = 'kkn' and ctime like '$day%';" > temp
    today_kkn=`cat temp | awk '{print $1}' | grep kkn | wc -l`
    today_internal=`cat temp | awk '{print $2}' | awk -F'|' '{print $1}' | grep 国内 | wc -l`
    today_international=`cat temp | awk '{print $2}' | awk -F'|' '{print $1}' |grep 国际 | wc -l`
    today_socity=`cat temp | awk '{print $2}' | awk -F'|' '{print $1}' |grep 社会 | wc -l`
    today_shanghai=`cat temp | awk '{print $2}' | awk -F'|' '{print $1}' |grep 上海 | wc -l`
    today_mili=`cat temp | awk '{print $2}' | awk -F'|' '{print $1}' |grep 军事 | wc -l`
    today_kk_produce=`cat temp | awk '{print $2}' | awk -F'|' '{print $1}' | grep 看看出品 | wc -l`
    today_caijing=`cat temp | awk '{print $2}' | awk -F'|' '{print $1}' | grep 财经 | wc -l`
    today_law=`cat temp | awk '{print $2}' | awk -F'|' '{print $1}' | grep 法制 | wc -l`
    echo $day, $today_internal, $today_international, $today_socity, $today_shanghai, $today_mili, $today_kk_produce, $today_caijing, $today_law, $today_kkn
    beg=$(date -d "$beg +1days" +%Y%m%d)
done
