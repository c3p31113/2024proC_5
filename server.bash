#!/bin/bash

sessionname="bunkyo_2024proc5"
apacheConfigFilePath="config/httpd.conf"
mariadbConfigFilePath="config/my.cnf"
fastapifilePath="api/main.py"

mode=$1

function main() {
    local mode=$1
    case $mode in
    start)
        if IsSessionAlive $sessionname; then
            echo "session is already on"
            exit 1
        fi
        NewSession $sessionname
        NewWindow $sessionname httpd
        NewWindow $sessionname mariadb
        NewWindow $sessionname fastapi
        SendKey $sessionname:httpd "httpd -d ./ -f $apacheConfigFilePath"
        SendKey $sessionname:mariadb "mysqld --defaults-file=$mariadbConfigFilePath"
        SendKey $sessionname:fastapi "source .venv/bin/activate" # venvに指定してるのがちょっと気に食わないが
        SendKey $sessionname:fastapi "python3.12 $fastapifilePath"
        KillWindow $sessionname dummy
        echo "session $sessionname initialized!"
        sayIP
        ;;
    stop)
        if ! IsSessionAlive $sessionname; then
            echo "session $sessionname wasn't found"
            exit 1
        fi
        HaltWindow $sessionname fastapi
        # HaltWindow $sessionname httpd
        # HaltWindow $sessionname mariadb
        httpd_PSID=$(pstree | grep -e "httpd -d ./ -f $apacheConfigFilePath" | grep -e "=" | grep -v "grep" | awk '{print $2}' | sed 's/0*\([0-9]*[0-9]$\)/\1/g')
        SendKey $sessionname:httpd "kill $httpd_PSID" #きったねぇけどこれしかない　httpdコマンドの時点でバックグラウンド起動バッチなのを恨む
        for ps in $(ProcessesOfSession $sessionname); do
            kill "$ps"
        done
        WaitUntilAllProcessDie "$(ProcessesOfSession $sessionname)"
        KillSession $sessionname
        ;;
    test)
        # SendKey $sessionname "httpd" "ls"
        # ProcessesOfSession $sessionname
        # PaneCountOfWindow $sessionname "fastapi"
        HaltWindow $sessionname fastapi
        # ProcessesOfWindow $sessionname mariadb
        ;;
    status)
        error=0
        if ! IsSessionAlive $sessionname; then
            echo "session is not alive!"
            error=1
            exit 1
        fi
        if ! IsWindowAlive $sessionname fastapi; then
            echo "fastapi window is not alive!"
            error=1
        elif [ -z "$(ProcessesOfWindow $sessionname fastapi >/dev/null)" ]; then
            echo "fastapi isn't working!"
            error=1
        fi
        if ! IsWindowAlive $sessionname mariadb; then
            echo "mariadb window is not alive!"
            error=1
        elif [ -z "$(ProcessesOfWindow $sessionname mariadb >/dev/null)" ]; then
            echo "mariadb isn't working!"
            error=1
        fi
        if ! IsWindowAlive $sessionname httpd; then
            echo "apache window is not alive!"
            error=1
        elif ! pstree | grep -e "httpd -d ./ -f $apacheConfigFilePath" | grep -e "=" | grep -v "grep" >/dev/null; then
            echo "apache isn't working!"
        fi
        if [ $error -eq 0 ]; then
            echo "all ok"
            sayIP
        else
            exit 1
        fi
        ;;
    *)
        echo "select function: { start | stop | status }"
        exit 1
        ;;
    esac
    exit 0
}
function sayIP() {
    globalip=$(curl "inet-ip.info" 2>/dev/null)
    localip=$(ifconfig | grep -e "inet " | grep -v "127.0.0.1" | awk '{print $2}')
    echo "global ip is $globalip"
    echo "local ip is $localip"
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
    if tmux list-windows -aF "#{session_name} #{window_name} " 2>/dev/null | grep -q "$sessionname $windowname "; then
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
function HaltWindow() {
    local sessionname=$1
    local windowname=$2
    if IsWindowAlive "$sessionname" "$windowname"; then
        for ((i = 0; i < $(PaneCountOfWindow "$sessionname" "$windowname"); i++)); do
            SendHalt "$sessionname:$windowname.$i"
        done
    else
        echo "$sessionname:$windowname wasn't found"
    fi
}
function SendKey() {
    local target=$1
    local keys=$2
    tmux send-keys -t "$target" "$keys" C-m
}
function SendHalt() {
    local target=$1
    tmux send-keys -t "$target" C-c
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
    if ! IsWindowAlive "$sessionname" "$windowname"; then
        echo "window $sessionname:$windowname wasn't found"
        return 1
    fi
    for tty in $(tmux list-panes -aF "#{session_name} #{window_name} #{pane_tty}" | grep "$sessionname $windowname " | awk '{print $3}'); do
        ProcessesOfTty "$tty"
    done
}
function ProcessesOfSession() {
    local sessionname=$1
    if ! IsSessionAlive; then
        echo "session $sessionname wasn't found"
        return 1
    fi
    windows=$(tmux list-windows -aF "#{session_name} #{window_name}" | grep "$sessionname " | awk '{print $2}')
    for window in $windows; do
        ProcessesOfWindow "$sessionname" "$window"
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

main "$mode"
