#!/bin/bash

touch LOGFILE
LOGFILE=LOGFILE
criteria="END"

function track() {

  #echo "This is a small program tracking the time spent on various tasks."

  #echo "The program tracks only one task at a time."

  #echo "You start the program by using the commando 'source' and then typing the filename 'track.sh'."
  #echo "Then you can call the program by calling the function 'track' and some command line argument."
  #echo "Type 'track help' for a helpful message to tell you how to use the program."

  if tail -n 1 LOGFILE | grep -q $criteria || [ ! -s LOGFILE ]; then # Checking if last line is END

    if [ $1 == "start" ]; then

      if [ $# != 2 ]; then
        echo "Must assign a label when starting a new task"
        return 1

      else
        echo "" >> LOGFILE
        currentdate=$(date +"%A %d %B %T %Y")
        echo "START: ${currentdate}" >> LOGFILE
        echo "LABEL: This is task $2"  >> LOGFILE
      fi

    elif [ $1 == "status" ]; then
      echo "No task is currently running."

    elif [ $1 == "stop" ]; then
      echo "There is no active task to stop right now."

    elif [ $1 == "log" ]; then
      listOfStartTime=( $(grep 'START' LOGFILE | cut -d\   -f5) )
      listOfTasks=( $(grep 'LABEL' LOGFILE | cut -d\   -f5) )
      listOfEndTime=( $(grep 'END' LOGFILE | cut -d\   -f5) )
      len=${#listOfEndTime[@]}
      for (( i=0; i<$len; i++ ));
        do
          elapsetime=$(date -d @$(( $(date -d "${listOfEndTime[$i]}" +%s) - $(date -d "${listOfStartTime[$i]}" +%s) )) -u +'%H:%M:%S')
          echo "Task ${listOfTasks[$i]}: $elapsetime"
        done
    else
      echo "Invalid argument."

      # Help Message
      echo " "
      echo "List of arguments are:"
      echo " "
      #echo "usage: track (--help)                        # Shows this help message"
      echo "usage: track (--start) [label]               # Starts a new task with a label"
      echo "usage: track (--stop)                        # Stops the current task, if there is one running."
      echo "usage: track (--status)                      # Shows what the current task is, if there is one running."
      echo "usage: track (--log)                         # Displays the time spent on each task."

    fi

  else

    if [ $1 == "start" ]; then
      listOfTasks=( $(tail -n 1 LOGFILE | grep 'LABEL' LOGFILE | cut -d\   -f5) )
      echo "Task ${listOfTasks[-1]} is already running. You have to stop the current task before starting a new task."

    elif [ $1 == "status" ]; then
      #tail -n 1 LOGFILE
      listOfTasks=( $(tail -n 1 LOGFILE | grep 'LABEL' LOGFILE | cut -d\   -f5) )
      echo "Currently task ${listOfTasks[-1]} is running."

    elif [ $1 == "stop" ]; then
      currentdate=$(date +"%A %d %B %T %Y")
      echo "END: ${currentdate}" >> LOGFILE

    elif [ $1 == "log" ]; then
      listOfTime=( $(grep 'START' LOGFILE | cut -d\   -f5) )
      listOfTasks=( $(grep 'LABEL' LOGFILE | cut -d\   -f5) )
      endtime=$(date +"%T")
      elapsetime=$(date -d @$(( $(date -d "$endtime" +%s) - $(date -d "${listOfTime[-1]}" +%s) )) -u +'%H:%M:%S')
      echo "Task ${listOfTasks[-1]}: $elapsetime"

    else
      echo "Invalid argument."

      # Help Message
      echo " "
      echo "List of arguments are:"
      echo " "
      #echo "usage: track (--help)                        # Shows this help message"
      echo "usage: track (--start) [label]               # Starts a new task with a label"
      echo "usage: track (--stop)                        # Stops the current task, if there is one running."
      echo "usage: track (--status)                      # Shows what the current task is, if there is one running."
      echo "usage: track (--log)                         # Displays the time spent on each task."

    fi

  fi


}
