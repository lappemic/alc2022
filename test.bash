#!/bin/bash

red=`tput setaf 1`
green=`tput setaf 2`
reset=`tput sgr0`
failed=0
for f in public-instances/*.hsp
do
    echo "in file ${f}"
    time=5 # edit time here
    gtimeout ${time}s python3 proj1.py < ${f} > output.out
    if [ $? == 124 ]; then # 124 is the int for TERM signal
        echo "${red}Time limit exceeded: ${time} second :(${reset}"
        failed=$((failed+1))
        continue
    else
        OUTPUT=$(./check ${f} output.out)
        cat output.out
        echo "----------------------"
        cat "${f%????}.out"
        echo
        if [[ $(head -1 output.out) = $(head -1 "${f%????}.out") ]]; then
            echo "${green}Passed :)${reset}"
        else
            echo "${red}Wrong :(${reset}"
        fi
        echo
        #diff output.out "${f%????}.out"
    fi
    if [ "${OUTPUT}" != "No errors found. Everything seems to be ok!" ]; then
        echo "${OUTPUT}"
        continue
    fi
    continue  # read next file and skip the cp command

done
echo
echo "${failed} got Time Limit exceeded :("
