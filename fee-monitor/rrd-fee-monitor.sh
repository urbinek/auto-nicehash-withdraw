#!/bin/sh

# define global parms
# name of dataset, will be uset to generate db and graphs
ds_name="bc_btc_fee"

# directory to store graphs - DO NOT REMOVE $ds_name
img_dir="/var/www/html/auto-nicehash-withdraw/fee-monitor"

# db directory - DO NOT REMOVE $ds_name
db_dir="/var/www/html/auto-nicehash-withdraw/fee-monitor"
db="$db_dir/$ds_name.rrd"

# define data collection command
data=`curl --silent https://api2.nicehash.com/main/api/v2/public/service/fee/info | jq '.withdrawal.BITGO.rules.BTC.intervals[0].element.sndValue' | awk -F "E" 'BEGIN{OFMT="%0.8f"} {print $1 * (10 ^ $2)}'`

# create db if not existing
if [ ! -e $db ]; then
    mkdir -p $db_dir

    rrdtool create $db \
        --step 60 \
        DS:$ds_name:GAUGE:120:0:1000 \
        RRA:MAX:0.5:1:44640
fi

# fill db with data
echo "Updating RRD $ds_name with value $data"
rrdtool update $db N:$data

# generate graph from db
mkdir -p "/var/www/html/auto-nicehash-withdraw/fee-monitor"
for period in day week month ; do
    
    case $period in
        "day")   x_axis="--x-grid MINUTE:10:HOUR:1:MINUTE:120:0:%R" ;;
        "week")  x_axis="--x-grid HOUR:12:DAY:1:DAY:1:0:%A" ;;
        "month") x_axis="--x-grid WEEK:1:WEEK:1:DAY:1:0:%d" ;;
        *) x_axis=" "
    esac

    rrdtool graph "$img_dir/$ds_name-$period".png \
        -w 900 -h 150 -a PNG \
        --slope-mode \
        --disable-rrdtool-tag \
        --start end-1"$period" --end now \
        --font DEFAULT:8:Courier \
        --font TITLE:9:BOLD:Courier \
        --color CANVAS#31373D \
        --color BACK#1F262D \
        --color FONT#FFFFFF \
        --color MGRID#6A6E73 \
        --color GRID#6A6E73 \
        --color ARROW#FFDD00 \
        --border 0 \
        --title "BC BTC Fee - Last $period" \
        --watermark "`date`" \
        --vertical-label 'BTC' \
        --units-exponent 0 \
        --left-axis-format "%.8lf" \
        --units-length 10 \
        $x_axis \
        --right-axis 1:0 \
        --right-axis-format "%.8lf" \
        --right-axis-label 'BTC' \
        DEF:btc_fee="$db":"$ds_name":LAST \
        LINE2:btc_fee#FFDD00:"Fee" \
        GPRINT:btc_fee:LAST:"Current\: %0.8lf BTC\t    " \
        GPRINT:btc_fee:MIN:"Min\: %0.8lf BTC\t     " \
        GPRINT:btc_fee:MAX:"Max\: %0.8lf BTC\n"
done
