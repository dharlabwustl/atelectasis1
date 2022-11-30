#!/bin/bash
cd /software/
git clone https://github.com/dharlabwustl/atelectatsis.git
mv atelectatsis/* /software/
chmod +x /software/*.sh 
#INPUTFILENAME=${1}
#OUTPUTDIRNAME=/workingoutput #${2}
#SESSION_ID=${1}
#XNAT_USER=${2}
#XNAT_PASS=${3}
#TYPE_OF_PROGRAM=${5}

/software/script_to_call_main_program.sh  #${INPUTFILENAME} ${OUTPUTDIRNAME} #$SESSION_ID $XNAT_USER $XNAT_PASS ${TYPE_OF_PROGRAM}
