#!/bin/bash
# mud_cmd.sh — Send commands to tbaMUD at localhost:4000 and print the full output.
#
# Usage:
#   ./mud_cmd.sh "look"
#   ./mud_cmd.sh "go north" "look" "inventory"
#
# The script authenticates, then sends each command with a short delay to
# allow the server to respond before the next command is sent.
# It is designed to be called once per agent turn — send only the commands
# you need for this step and read the output before deciding what comes next.

MUD_HOST="localhost"
MUD_PORT="4000"
MUD_USER="dummy"
MUD_PASS="helloworld"

# Seconds to wait after each command for the server response.
# Increase CMD_WAIT if the MUD output feels cut off.
LOGIN_WAIT=3
MENU_WAIT=2
CMD_WAIT=2

(
  sleep "$LOGIN_WAIT"   # wait for "By what name do you wish to be known?"
  echo "$MUD_USER"
  sleep 1               # wait for password prompt
  echo "$MUD_PASS"
  sleep "$MENU_WAIT"    # wait for the main menu
  echo "0"              # "0" = Enter the game
  sleep "$MENU_WAIT"    # wait for starting room description

  for cmd in "$@"; do
    echo "$cmd"
    sleep "$CMD_WAIT"
  done

  sleep 1
) | nc -w 2 "$MUD_HOST" "$MUD_PORT"
