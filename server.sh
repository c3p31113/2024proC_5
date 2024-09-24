#!/bin/bash

servername="bunkyo_2024proc5"
apacheConfigFilePath="httpd.conf"
mariadbConfigFilePath="my.cnf"
fastapifilePath="app.py"
mode=$1

function IsSessionAlive() {
    if tmux list-sessions -F '#S' | grep -q "$1"; then
        return 0
    fi
    return 1
}
function NewSession() {
    if IsSessionAlive "$1"; then
        echo "$1 session is already on"
    else
        echo "starting server"
        tmux new -d -s "$1" -n dummy
    fi
}
function KillSession() {
    if IsSessionAlive "$1"; then
        echo "killing $1 session"
        tmux kill-session -t "$1"
    else
        echo "$1 wasn't found"
    fi
}
function IsWindowAlive() {
    if tmux list-windows -F '#S:#W' | grep -q "$1:$2"; then
        return 0
    fi
    return 1
}
function NewWindow() {
    if IsWindowAlive "$1" "$2"; then
        echo "$1:$2 window is already on"
    else
        tmux new-window -a -t "$1" -n "$2"
    fi
}
function KillWindow() {
    if IsWindowAlive "$1" "$2"; then
        echo "killing $2 window"
        tmux kill-window -t "$1":"$2"
    else
        echo "$1:$2 wasn't found"
    fi
}
function SendKey() {
    tmux send-keys -t "$1":"$2" "$3" C-m
}
function SendHalt() {
    tmux send-keys -t "$1":"$2" C-c
}
function ProcessesOfSession() {
    tty=$(tmux list-sessions -F "#{session_name} #{pane_tty}" | grep "^$1 " 2>/dev/null | awk '{print $2}')
    for process in $(ps -o pid -t "$tty" | tail -n +2); do
        if [[ $counter -eq "0" ]]; then
            result=$(printf "%s%s" "$result" "$process")
        else
            result=$(printf "%s\n%s" "$result" "$process")
        fi
        ((counter++))
    done
    echo "$result" | tail -1
}
function ProcessesOfWindow() {
    tty=$(tmux list-windows -aF "#{session_name} #{window_name} #{pane_tty}" | grep "$1 $2 " 2>/dev/null | awk '{print $3}')
    for process in $(ps -o pid -t "$tty" | tail -n +2); do
        if [[ $counter -eq "0" ]]; then
            result=$(printf "%s%s" "$result" "$process")
        else
            result=$(printf "%s\n%s" "$result" "$process")
        fi
        ((counter++))
    done
    echo "$result" | tail -1
}


modes=("start" "stop" "test")
if ! printf '%s\n' "${modes[@]}" | grep -qx "$1"; then
    echo "select function: { start | stop }"
    exit 1
fi

if [[ "$mode" == "start" ]]; then
    if IsSessionAlive $servername; then
        echo "session is already on"
        exit 1
    fi
    NewSession $servername
    NewWindow $servername httpd
    NewWindow $servername mariadb
    NewWindow $servername fastapi
    SendKey $servername httpd "httpd -d ./ -f $apacheConfigFilePath"
    SendKey $servername mariadb "mysqld --defaults-file=$mariadbConfigFilePath"
    SendKey $servername fastapi "python3.11 $fastapifilePath"
    KillWindow $servername dummy
    echo "server $servername initialized!"
elif [[ "$mode" == "stop" ]]; then
    if ! IsSessionAlive $servername; then
        echo "server $servername wasn't found"
        exit 1
    fi
    SendHalt $servername fastapi
    SendHalt $servername httpd
    SendHalt $servername mariadb
    #FIXME: プロセス終了は待つべき
    KillSession $servername
elif [ "$mode" == "test" ]; then
    # SendKey $servername "httpd" "ls"
    # for process in $(ProcessesOfSession $servername); do
    #     echo "$process"
    # done
    # ProcessesOfSession $servername fastapi
    ProcessesOfWindow $servername fastapi
fi
exit 0
