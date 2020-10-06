
function add_entry {
    CPU_USAGE=$(grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage "%"}')
    DATE=$(date "+%Y-%m-%dT%H:%M:%S")
    
    echo $DATE "," $CPU_USAGE >> cpu_usage.csv
    exit
}

# echo "Date, CPU_usage" >> cpu_usage.csv

for i in {1..10}
do
    add_entry &
    sleep 1 
done