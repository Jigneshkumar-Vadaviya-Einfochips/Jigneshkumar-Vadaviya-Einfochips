#!/bin/bash

#set -x

RELEASE_BUILD="$1"
ADB_CMD="adb -s $2 wait-for-device "

if [ -z $1 ]
then
	echo "Please provide Release build as argument..............."
	exit 1
else
	echo "Release build is:" $1
fi

if [ -z $2 ]
then
	echo "Please provide Device ADB ID as argument..............."
	exit 1
else
	echo "Device ADB cmd id is:" $2
fi

$ADB_CMD shell rm /mnt/nv/product-persistence/HTTPProxy_telemetry.json
$ADB_CMD shell sync
$ADB_CMD shell sync
$ADB_CMD shell reboot
echo "Removed Previous data of telemtry and rebooted the device"

echo
echo "Startig Logcapture that will timeout"
time timeout -s SIGTERM 5m $ADB_CMD shell logread -f > $1_Flipper_OOB_2_Full_Logread.txt;
echo "Log Captured Done"
echo


echo "Executing tap-command telemetry persist"
$ADB_CMD shell /opt/Bose/bin/tap-command telemetry persist

$ADB_CMD pull /mnt/nv/product-persistence/HTTPProxy_telemetry.json $1_Flipper_OOB_2_Telemetry.json
echo "Pulled HTTPProxy_telemetry file from device"
echo

echo "Converting logread file to Csv file for Reverse URL"

if [ $RELEASE_BUILD == "MR7" ]
then
	echo "MR7................."
	cat $1_Flipper_OOB_2_Full_Logread.txt | grep -e 'reverse url:' | awk '{ print $1,$2","$3","$9}' > $1_Flipper_OOB_2_HTTPRequests.csv
else
	cat $1_Flipper_OOB_2_Full_Logread.txt | grep -e 'HTTP request:' | awk '{ print $7","$8","$11","$12}' > $1_Flipper_OOB_2_HTTPRequests.csv
fi


echo "Converting Telemetry file to Csv file for Metrics"
cat $1_Flipper_OOB_2_Telemetry.json | jq .ComponentMetric.metrics | jq -r '(map(keys) | add | unique) as $cols | map(. as $row | $cols | map($row[.])) as $rows | $cols, $rows[] | @csv' > $1_Flipper_OOB_2_Telemetry.csv
echo
echo "Process Comepleted, Exiting....."
