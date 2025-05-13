#!/bin/bash
PIPE_PATH="/tmp/minecraft_pipe"

if [[ ! -p $PIPE_PATH ]]; then
	mkfifo $PIPE_PATH
fi

tail -f $PIPE_PATH | java -jar -Xmx8G `minecraft_server.jar file` --nogui

