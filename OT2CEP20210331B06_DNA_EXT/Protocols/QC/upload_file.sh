HOST="root@OT2CEP20210331B06"
LOCAL_DIRECTORY="C:/Users/omicstemp/Documents/Opentrons/OT2CEP20210331B06_DNA_EXT/Protocols/QC/InputCSV/*.csv"
REMOTE_DIRECTORY="rm /data/user_files/*.csv"

ssh -i ot2_ssh_key_OT2CEP20210331B06 $HOST $REMOTE_DIRECTORY
scp -i ot2_ssh_key_OT2CEP20210331B06 $LOCAL_DIRECTORY $HOST:/data/user_files/input.csv
rm $LOCAL_DIRECTORY
read -n 1 -r -s -p $'Press enter to continue...\n'