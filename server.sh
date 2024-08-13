#!/bin/bash

sessionname="bunkyo_2024proc5_server"
apacheConfigFilePath="httpd.conf"
mariadbConfigFilePath="my.cnf"
fastapifilePath="app.py"
mode=$1

function NewSession() {
    if tmux list-sessions | grep -q "$1"; then
        echo "$sessionname session is already on"
    else
        echo "starting server"
        tmux new -d -s $1 -n dummy
    fi
}
function NewWindow() {
    if tmux list-windows -F '#S:#W' | grep -q "$1:$2"; then
        echo "$2 window is already on"
    else
        tmux new-window -a -t $1 -n $2
    fi
}
function KillWindow() {
    if tmux list-windows -F '#S:#W' | grep -q "$1:$2"; then
        echo "killing $2 window"
        tmux kill-window -t $1:$2
    else
        echo "$2 wasn't found"
    fi
}
function SendKey() {
    tmux send-keys -t "$1":"$2" "$3" C-m
}

modes=("start" "stop" "test")
if ! printf '%s\n' "${modes[@]}" | grep -qx "$1"; then
    echo "select function: { start | stop }"
    exit 1
fi

if [ "$mode" == "start" ]; then
    NewSession $sessionname
    NewWindow $sessionname httpd
    NewWindow $sessionname mariadb
    NewWindow $sessionname fastapi
    SendKey $sessionname httpd "httpd -d ./ -f $apacheConfigFilePath"
    SendKey $sessionname mariadb "mysqld --defaults-file=$mariadbConfigFilePath"
    SendKey $sessionname fastapi "python3.11 $fastapifilePath"
    KillWindow $sessionname dummy
    #TODO: 二重起動を対策する
    echo "server initialized!"
elif [ "$mode" == "stop" ]; then
    echo "not implemented yet"
    #TODO: implement stop function
elif [ "$mode" == "test" ]; then
    SendKey $sessionname "httpd" "ls"
fi
exit 0
