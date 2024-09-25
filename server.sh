#!/bin/bash

sessionname="bunkyo_2024proc5"
apacheConfigFilePath="httpd.conf"
mariadbConfigFilePath="my.cnf"
fastapifilePath="app.py"
mode=$1

function IsSessionAlive() {
    if tmux list-sessions -F '#{session_name}' 2>/dev/null | grep -q "$1"; then
        return 0
    fi
    return 1
}
function NewSession() {
    if IsSessionAlive "$1"; then
        echo "$1 session is already on"
    else
        echo "starting session"
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
    if tmux list-windows -aF '#{session_name} #{window_name}' 2>/dev/null | grep -q "$1 $2"; then
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
        echo "killing $1:$2 window"
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
function ProcessesOfWindow() {
    if ! IsWindowAlive; then
        echo "session $1:$2 wasn't found"
        exit 1
    fi
    tty=$(tmux list-windows -aF "#{session_name} #{window_name} #{pane_tty}" | grep "$1 $2 " 2>/dev/null | awk '{print $3}')
    for process in $(ps -o pid -t "$tty" | tail -n +2); do
        if [[ ! $(ps -p "$process" -o comm=) == "-zsh" ]]; then
            if [[ $counter -eq "0" ]]; then
                result=$(printf "%s%s" "$result" "$process")
            else
                result=$(printf "%s\n%s" "$result" "$process")
            fi
            ((counter++))
        fi
    done
    echo "$result" | tail -1
}
function ProcessesOfSession() {
    if ! IsSessionAlive; then
        echo "session $1 wasn't found"
        exit 1
    fi
    sessions=$(tmux list-windows -aF "#{session_name} #{window_name}" | grep "$1 " | awk '{print $2}')
    for session in $sessions; do
        ProcessesOfWindow "$1" "$session"
    done
}
function WaitUntilAllProcessDie() {
    running=true
    while [[ "$running" == "true" ]]; do
        running=false
        for process in $1; do
            if ps -p "$process" >/dev/null; then
                running=true
                continue
            fi
            running=false
        done
        echo "shutdown..."
        sleep 1
    done
}

modes=("start" "stop" "test")
if ! printf '%s\n' "${modes[@]}" | grep -qx "$1"; then
    echo "select function: { start | stop }"
    exit 1
fi

if [[ "$mode" == "start" ]]; then
    if IsSessionAlive $sessionname; then
        echo "session is already on"
        exit 1
    fi
    NewSession $sessionname
    NewWindow $sessionname httpd
    NewWindow $sessionname mariadb
    NewWindow $sessionname fastapi
    SendKey $sessionname httpd "httpd -d ./ -f $apacheConfigFilePath"
    SendKey $sessionname mariadb "mysqld --defaults-file=$mariadbConfigFilePath"
    SendKey $sessionname fastapi "python3.11 $fastapifilePath"
    KillWindow $sessionname dummy
    echo "session $sessionname initialized!"
elif [[ "$mode" == "stop" ]]; then
    if ! IsSessionAlive $sessionname; then
        echo "session $sessionname wasn't found"
        exit 1
    fi
    SendHalt $sessionname fastapi
    SendHalt $sessionname httpd
    SendHalt $sessionname mariadb
    WaitUntilAllProcessDie "$(ProcessesOfSession $sessionname)"
    KillSession $sessionname
elif [ "$mode" == "test" ]; then
    # SendKey $sessionname "httpd" "ls"
    ProcessesOfSession $sessionname
    # ProcessesOfWindow $sessionname mariadb
fi
exit 0
