#!/bin/bash

sessionname="bunkyo_2024proc5"
apacheConfigFilePath="httpd.conf"
mariadbConfigFilePath="my.cnf"
fastapifilePath="app.py"
mode=$1

function main() {
    if [[ "$mode" == "start" ]]; then
        if IsSessionAlive $sessionname; then
            echo "session is already on"
            exit 1
        fi
        NewSession $sessionname
        NewWindow $sessionname httpd
        NewWindow $sessionname mariadb
        NewWindow $sessionname fastapi
        SendKey1 $sessionname httpd "httpd -d ./ -f $apacheConfigFilePath"
        SendKey1 $sessionname mariadb "mysqld --defaults-file=$mariadbConfigFilePath"
        SendKey1 $sessionname fastapi "python3.11 $fastapifilePath"
        KillWindow $sessionname dummy
        echo "session $sessionname initialized!"
    elif [[ "$mode" == "stop" ]]; then
        if ! IsSessionAlive $sessionname; then
            echo "session $sessionname wasn't found"
            exit 1
        fi
        SendHalt1 $sessionname fastapi
        SendHalt1 $sessionname httpd
        SendHalt1 $sessionname mariadb
        WaitUntilAllProcessDie "$(ProcessesOfSession $sessionname)" #TODO: 非アクティブpaneにもSend_Haltする
        KillSession $sessionname
    elif [ "$mode" == "test" ]; then
        # SendKey $sessionname "httpd" "ls"
        # ProcessesOfSession $sessionname
        PaneCountOfWindow $sessionname "fastapi"
        # ProcessesOfWindow $sessionname mariadb
    fi
    exit 0
}
function IsSessionAlive() {
    local sessionname=$1
    if tmux list-sessions -F '#{session_name}' 2>/dev/null | grep -q "$sessionname"; then
        return 0
    fi
    return 1
}
function NewSession() {
    local sessionname=$1
    if IsSessionAlive "$sessionname"; then
        echo "$sessionname session is already on"
    else
        echo "starting session"
        tmux new -d -s "$sessionname" -n dummy
    fi
}
function KillSession() {
    local sessionname=$1
    if IsSessionAlive "$sessionname"; then
        echo "killing $sessionname session"
        tmux kill-session -t "$sessionname"
    else
        echo "$sessionname wasn't found"
    fi
}
function IsWindowAlive() {
    local sessionname=$1
    local windowname=$2
    if tmux list-windows -aF '#{session_name} #{window_name}' 2>/dev/null | grep -q "$sessionname $windowname"; then
        return 0
    fi
    return 1
}
function NewWindow() {
    local sessionname=$1
    local windowname=$2
    if IsWindowAlive "$sessionname" "$windowname"; then
        echo "$1:$2 window is already on"
    else
        tmux new-window -a -t "$sessionname" -n "$windowname"
    fi
}
function KillWindow() {
    local sessionname=$1
    local windowname=$2
    if IsWindowAlive "$sessionname" "$windowname"; then
        echo "killing $sessionname:$windowname window"
        tmux kill-window -t "$sessionname:$windowname"
    else
        echo "$sessionname:$windowname wasn't found"
    fi
}
function SendKey1() {
    local sessionname=$1
    local windowname=$2
    local keys=$3
    # if [[ $windowname == "" ]]; then
    #     tmux send-keys -t "$sessionname" "$keys" C-m
    # elif [[ $paneid == "" ]]; then
        tmux send-keys -t "$sessionname:$windowname" "$keys" C-m
    # else
    #     tmux send-keys -t "$sessionname:$windowname.$paneid" "$keys" C-m
    # fi
}
function SendKey2() {
    local sessionname=$1
    local windowname=$2
    local pane=$3
    local keys=$4
    tmux send-keys -t "$sessionname:$windowname.$pane" C-m
}
function SendHalt1() {
    local sessionname=$1
    local windowname=$2
    tmux send-keys -t "$sessionname:$windowname" C-c
}
function SendHalt2() {
    local sessionname=$1
    local windowname=$2
    local pane=$3
    tmux send-keys -t "$sessionname:$windowname.$pane" C-c
}
function PaneCountOfWindow() {
    local sessionname=$1
    local windowname=$2
    tmux list-windows -aF "#{session_name} #{window_name} #{window_panes}" | grep "$sessionname $windowname" | awk '{print $3}'
}
function ProcessesOfTty() {
    local tty=$1
    result=()
    for process in $(ps -o pid -t "$tty" | tail -n +2); do
        if [[ ! $(ps -p "$process" -o comm=) == "-zsh" ]]; then
            result+=("$process")
        fi
    done
    echo "${result[*]}"
}
function ProcessesOfWindow() {
    local sessionname=$1
    local windowname=$2
    if ! IsWindowAlive; then
        echo "window $sessionname:$windowname wasn't found"
        exit 1
    fi
    for tty in $(tmux list-panes -aF "#{session_name} #{window_name} #{pane_tty}" | grep "$sessionname $windowname " | awk '{print $3}'); do
        ProcessesOfTty "$tty"
    done
}
function ProcessesOfSession() {
    local sessionname=$1
    if ! IsSessionAlive; then
        echo "session $sessionname wasn't found"
        exit 1
    fi
    sessions=$(tmux list-windows -aF "#{session_name} #{window_name}" | grep "$sessionname " | awk '{print $2}')
    for session in $sessions; do
        ProcessesOfWindow "$sessionname" "$session"
    done
}
function WaitUntilAllProcessDie() {
    local processes=$1
    running=true
    while [[ "$running" == "true" ]]; do
        running=false
        for process in $processes; do
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
if ! printf '%s\n' "${modes[@]}" | grep -qx "$mode"; then
    echo "select function: { start | stop }"
    exit 1
fi

main "$mode"
