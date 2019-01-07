printf "Starting SmartPark\n"
xterm -xrm 'XTerm.vt100.allowTitleOps: false' -T SmartPark-Communication -e python3 communication.py &
xterm -xrm 'XTerm.vt100.allowTitleOps: false' -T SmartPark-Application -e python3 main.py &
