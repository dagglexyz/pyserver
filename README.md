sudo apt-get install python3.10-venv
python3 -m venv .
source ./bin/activate

# Run the Program
uvicorn index:app &

# Kill the Program
# Get PID
ps -e
# Kill
kill 1667(pid from above command)
