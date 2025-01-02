
#Pass the variable in string
case "$1" in
    "MR7") #EddiePratik
		ADB_CMD="adb -s 87f3bda"
		;;
	"MR9") #Eddie212C
		ADB_CMD="adb -s 8de7d30 "
		;;
	"MR11") #LCMEddie1
                ADB_CMD="adb -s 27f44214"
                ;;
	*) 
		echo "Invalid Product Type ........."
		exit 0
		;;
esac

$ADB_CMD shell rm /mnt/nv/product-persistence/HTTPProxy_telemetry.json
$ADB_CMD reboot
echo "Removed Previous data of telemtry and rebooted the device"

echo
echo "Startig Logcapture that will timeout after 1 day"
timeout -s SIGTERM 1d $ADB_CMD wait-for-device shell logread -f > $1_Eddie_NoActivity_Full_Logread.txt;
echo "Log Captured Done"
echo


$ADB_CMD pull /mnt/nv/product-persistence/HTTPProxy_telemetry.json $1_Eddie_NoActivity_Telemetry.json
echo "Pulled HTTPProxy_telemetry file from device"
echo

echo "Converting logread file to Csv file for HTTP Requests"
cat $1_Eddie_NoActivity_Full_Logread.txt | grep -e 'HTTP request:' | awk '{ print $7","$8","$11","$12}' > $1_Eddie_NoActivity_HTTPRequests.csv
echo

echo "Converting Telemetry file to Csv file for Metrics"
cat $1_Eddie_NoActivity_Telemetry.json | jq .ComponentMetric.metrics | jq -r '(map(keys) | add | unique) as $cols | map(. as $row | $cols | map($row[.])) as $rows | $cols, $rows[] | @csv' > $1_Eddie_NoActivity_Telemetry.csv
echo
echo "Process Comepleted, Exiting....."
