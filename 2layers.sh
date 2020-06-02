#!/usr/bin/env bash

workdir=$(pwd)

function prepare() {
  echo "Installing CoAPthon dependency..."
  pip install CoAPthon
}

function startController() {
    echo "#######################"
    echo "# Starting sensors... #"
    echo "#######################"
    echo -e "\n"
    sense_emu_gui && cd "${workdir}/sensor" && ./controller.py -i 127.0.0.1 -p 5683 >> /dev/null 2> /dev/null &
    sleep 4
}

function startClient() {
    cd "${workdir}/client" || exit 1

    echo "##########################################"
    echo "# Starting client in interactive mode... #"
    echo "##########################################"
    echo -e "\n"

    echo "##################################"
    echo "# Getting current temperature... #"
    echo "##################################"
    echo -e "\n"
    ./client.py -o GET -p coap://127.0.0.1:5683/temp
    sleep 4

    echo "############################################"
    echo "# Getting current temperature threshold... #"
    echo "############################################"
    echo -e "\n"
    ./client.py -o GET -p coap://127.0.0.1:5683/temp_threshold
    sleep 4

    echo "########################################"
    echo "# Setting new temperature threshold... #"
    echo "########################################"
    echo -e "\n"
    ./client.py -o POST -p coap://127.0.0.1:5683/temp_threshold -P1
    sleep 4

    echo "############################################"
    echo "# Getting current temperature threshold... #"
    echo "############################################"
    echo -e "\n"
    ./client.py -o GET -p coap://127.0.0.1:5683/temp_threshold
    sleep 4

    echo "###############################"
    echo "# Getting current humidity... #"
    echo "###############################"
    echo -e "\n"
    ./client.py -o GET -p coap://127.0.0.1:5683/humi
    sleep 4

    echo "#########################################"
    echo "# Getting current humidity threshold... #"
    echo "#########################################"
    echo -e "\n"
    ./client.py -o GET -p coap://127.0.0.1:5683/humi_threshold
    sleep 4

    echo "#####################################"
    echo "# Setting new humidity threshold... #"
    echo "#####################################"
    echo -e "\n"
    ./client.py -o POST -p coap://127.0.0.1:5683/humi_threshold -P50
    sleep 4

    echo "#########################################"
    echo "# Getting current humidity threshold... #"
    echo "#########################################"
    echo -e "\n"
    ./client.py -o GET -p coap://127.0.0.1:5683/humi_threshold
    sleep 4
}

function cleanUp() {
  echo "Cleaning up threads..."
    ps aux | grep -E '(client.py|controller.py|server.py)' | awk '{ print $2 }' | xargs kill -9
}

prepare
startController
startClient
cleanUp

exit 0