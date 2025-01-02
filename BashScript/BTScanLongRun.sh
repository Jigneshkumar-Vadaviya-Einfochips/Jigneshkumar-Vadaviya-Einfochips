#!/bin/bash
# Define the log file path
rm output.log
logfile="output.log"

 
# Redirect all output to both the log file and the screen
exec &> >(tee -a "$logfile")

while true; do
	echo "==============>>>>>>>>>>>>>>>>>> $(date) <<<<<<<<<<<<<<<<=================="
	echo "Start Scan.........."
	frontdoorutil -c POST /bluetooth/source/scan '{}'
	sleep 5
	echo "CPU Informarion:"
	ps -aux | grep -ie "/opt/Bose/bin/Bluetooth" -ie "USER         PID" | grep -v grep
	BTPID=`pidof Bluetooth`
	FDVALUE=`ls  /proc/${BTPID}/fd | wc -l`
	echo "File Descriptor Usage: $FDVALUE"
	sleep 10
	frontdoorutil -c POST /bluetooth/source/stopScan '{}'
	sleep 1
done

