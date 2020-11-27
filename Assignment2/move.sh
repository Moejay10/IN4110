#!/bin/bash

if [ $# -eq 2 ]; then

  if [ -d $1 ] && [ -d $2 ]; then
    #mv $1/* $2
    find $1 -type f -name "*.txt" -exec mv {} $2 \;

  #else
  #  echo "Error: Directories $1 or $2 does not exist."

  fi

  if [ ! -d $1 ]; then
    echo "Error: Directory $1 does not exist."
    exit -1

  elif [ ! -d $2 ]; then
    echo "Error: Directory $2 does not exist."
    echo "We will then create the directory $2."

    mkdir $2
    find $1 -type f -name "*.txt" -exec mv {} $2 \;
  fi

  cd $2
  # put current date as yyyy-mm-dd HH:MM:SS in $date
  mkdir $(date +%F-%H-%M)

  cd ..
  find $2 -type f -name "*.txt" -exec mv {} $2/$(date +%F-%H-%M) \;


else
  echo "Error: 2 command line arguments needed to run."

fi
