#!/bin/bash

[ -z "$1" ] && echo "Please specify checkpoint name" && exit 1

[ ! -d ~/.rnode ] && echo "$HOME/.rnode does not exist for checkpointing" && exit 2

ALREADY=`ps -fu |grep -v grep |grep " java .*rnode"|sed 's/[ \t][ \t]*/ /g'|cut -d' ' -f 2`

[ -n "$ALREADY" ] && echo "
$0: rnode is currently running
Use 'kill $ALREADY' to fix.
" && while read -p "Execute 'kill $ALREADY' [y]? " response;do
	if [ "$response" == "y" ] || [ -z "$response" ];then
      set -x
		kill $ALREADY
      set +x
		break
	else
		echo "Aborting $0"
		exit 3
	fi
done

cd `dirname $0`

mkdir -p checkpoint

TARGET=$PWD/checkpoint/$1.tgz

[ -f $TARGET ] && while read -p "$TARGET already exists. Replace [y]? " response;do
   if [ "$response" == 'y' ] || [ -z "$response" ]; then
      break
   else
      echo "Aborted"
      exit 0
   fi
done

(cd ~; tar czf $TARGET .rnode)
echo "Checkpoint created: $TARGET"