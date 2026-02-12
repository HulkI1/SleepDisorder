#!/usr/bin/env bash
# Simple server manager for the Flask app
# Usage: ./manage_server.sh start|stop|status

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
PIDFILE="$ROOT_DIR/flask_server.pid"
LOGFILE="$ROOT_DIR/flask_server.log"

start_server() {
  if [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
    echo "Server already running (pid $(cat "$PIDFILE"))"
    return 0
  fi

  echo "Starting Flask server..."
  nohup python3 "$ROOT_DIR/flask_app.py" > "$LOGFILE" 2>&1 &
  echo $! > "$PIDFILE"
  sleep 1
  if kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
    echo "Started (pid $(cat "$PIDFILE"))"
  else
    echo "Failed to start server; check $LOGFILE"
    rm -f "$PIDFILE"
  fi
}

stop_server() {
  if [ ! -f "$PIDFILE" ]; then
    echo "Server not running (no $PIDFILE)"
    return 0
  fi
  PID=$(cat "$PIDFILE")
  echo "Stopping server pid $PID..."
  kill $PID 2>/dev/null || true
  sleep 1
  if kill -0 $PID 2>/dev/null; then
    echo "Process still running, forcing kill"
    kill -9 $PID 2>/dev/null || true
  fi
  rm -f "$PIDFILE"
  echo "Stopped"
}

status_server() {
  if [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
    echo "Running (pid $(cat "$PIDFILE"))"
  else
    echo "Not running"
  fi
}

case "$1" in
  start)
    start_server
    ;;
  stop)
    stop_server
    ;;
  status)
    status_server
    ;;
  restart)
    stop_server
    start_server
    ;;
  *)
    echo "Usage: $0 {start|stop|status|restart}"
    exit 1
    ;;
esac

exit 0
