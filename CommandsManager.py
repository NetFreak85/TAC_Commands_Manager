#!/usr/local/bin/python3.9

#***********************************************************************************************************************#
#                                                                                                                       #
#   --usage:                                                                                                            #
#             ./CommandsManager.py                                                                                      #
#         or  python CommandsManager.py                                                                                 #
#                                                                                                                       #
# date:  15/06/2022 Created                                                                                             #
#***********************************************************************************************************************#

##################
# Import Section #
##################

import Constant
import time
import requests
import argparse
import urllib3
from requests.auth import HTTPBasicAuth
from paramiko import SSHClient, MissingHostKeyPolicy
from datetime import date
from termcolor import colored

#############
# Variables #
#############

#List that will store all the commands required
Command_List = []

#Variable that allow verbose mode
Verbose_Mode = False

#########################
# Functions Declaration #
#########################

#Defining the Argument function that allow the verbose mode
def get_args():
    parser = argparse.ArgumentParser()

    #Method that enable verbose mode
    parser.add_argument('-v',
                        help='Verbose mode',
                        action='store_true',
                        required=False)

    return parser.parse_args()

#Function that clear the SSH buffer
def clear_buffer(connection):
    if connection.recv_ready():
        return connection.recv(Constant.NetworkDeviceMaxBuffer)

#Function that will read all the commands requested by Cisco TAC from a file and will store then into a List
def read_Commands_File():

    #List that will store the Commands from file
    List = []

    #We open the file Command_List.txt that have all the commands and stored in the List variable
    with open(Constant.CMD_FILE_PATH) as file:
        for Line in file:
            List.append(Line)

    #Delete all posibles blank lines in the List variable
    List = ' '.join(List).split('\n')

    #Closing the Command_List.txt File
    file.close()

    #Returning the List with the commands
    return List

#Function that create the SSH session to the Host 
def get_connection():
    
    #We generate the SSH Client object
    ssh = SSHClient()

    try:
        #We check the system host keys for hosts
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(MissingHostKeyPolicy())

        #Generate the SSH connection with the credentials
        ssh.connect(hostname=Constant.NetworkDevice, username=Constant.User, password=Constant.Password, port=Constant.NetworkDevice_SSH_Port, allow_agent=True, compress=True, look_for_keys=False)
    
    #Cauth the possible errors in the SSH Connection
    except ssh.AuthenticationException:
        print("Authentication failed, please verify your credentials: %s")
    except ssh.SSHException as sshException:
        print("Unable to establish SSH connection: %s" % sshException)
    except ssh.BadHostKeyException as badHostKeyException:
        print("Unable to verify server's host key: %s" % badHostKeyException)

    #Return the SSH session
    return ssh

#Function that upload the file in the Cisco Cloud
def upload_Tac_File(Filename):

    #Get authentication with the SR Ticket Number and Case Token
    auth = HTTPBasicAuth(Constant.SR_Ticket, Constant.Token)

    #We open the file with the commands results
    f = open(Filename, 'rb')

    #Upload the file to Cisco Cloud
    r = requests.put(Constant.URL + Filename, f, auth=auth, verify=False)
    
    #Close the request & file
    r.close()
    f.close()

    #Check the request status code
    if r.status_code == 201:
        print("File Uploaded Successfully")

#Send Command to APICs
def get_Command_Results():

    #Disable warning msgs when we upload the file into the Cisco Cloud
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    #Global variable that store the Argument verbose (bolean)
    global Verbose_Mode

    #Class that evaluate arguments in the script
    args = get_args()

    #Check if verbose mode is enable 
    if args.v:
        Verbose_Mode = True

    #Variable that remove the \n and will print
    aux = ""

    #Variable that delete the first space in the line of the command list
    Index = False

    #Boolean variable that allow us enable the terminal len 0 commands
    Terminal_Len = True

    #Read Commands Line from File
    Command_List = read_Commands_File()
    
    #Generation the SSH Connection
    ssh = get_connection()

    #Invoke a shell throught the SSH Connection
    Shell = ssh.invoke_shell()

    #We use the Date Class in order to know when the Output File was created
    today = date.today()

    #Variable that generate the filename with the SR Ticket number and generation date
    APIC_OUTPUT_FILENAME = Constant.NetworkDevice + "-SR-" + Constant.SR_Ticket + "-" + today.strftime("%d-%m-%Y") + ".txt"
    
    #Open the file to write the cmd outputs
    try:
        APIC_CMD_OUTPUT = open( APIC_OUTPUT_FILENAME, "x")
    except:
        APIC_CMD_OUTPUT = open( APIC_OUTPUT_FILENAME, "w")

    #Execute the commands stored in the Command_List
    for cmd in Command_List:

        #Check if the Command is not empty
        if cmd != "":

            #Variable that remove the \n and will print
            if Verbose_Mode:
                aux = cmd

            #Variable that Check if the command is a moquery command
            mQuery_Check = cmd.split()

            #Clean the first empty carater in the List
            if Index:
                cmd = cmd[1: : ]
            Index = True

            #Enable the terminal len 0 for the cmd outputs
            if Terminal_Len:

                if Verbose_Mode:
                    print ("*" * Constant.Verbose_Mode_len)

                #Enable the Terminal lenght command in the APIC, clearing the buffer and sleep 
                # procees to give some time to the APIC for the next cmd
                Shell.send('terminal length 0\n')
                clear_buffer(Shell)
                time.sleep(Constant.Time_Sleep)
                Terminal_Len = False

            #Put a \n at the end of the command
            cmd = cmd + "\n"

            #Checking if the command is a moquery command
            if mQuery_Check[0] == "moquery":
                Shell.send('bash\n')

            #Printing on console when the command is send to network device
            if Verbose_Mode:
                print (colored('Sending command '"'" + aux + "'"' to '"'" + Constant.NetworkDevice + "'", 'red'))

            #We send the command over the invoked shell
            Shell.send(cmd)

            #Wait the APIC to procees the command
            time.sleep(Constant.Time_Sleep)

            #Print the cmd output
            #print(Shell.recv(Constant.NetworkDeviceMaxBuffer).decode(encoding='UTF-8'))

            #Printing on console when the command is receive from network device
            if Verbose_Mode:
                print (colored('Reciving command '"'" + aux + "'"' information from '"'" + Constant.NetworkDevice + "'", 'yellow'))

            #Printing on console when the command is receive from network device
            if Verbose_Mode:
                print (colored('Writing the command results over the file ', 'green'))

            #Write the Shell cmd output under the File
            APIC_CMD_OUTPUT.write(Shell.recv(Constant.NetworkDeviceMaxBuffer).decode(encoding='UTF-8'))
            APIC_CMD_OUTPUT.write("\n")

            #Clearing the buffer
            clear_buffer(Shell)

            #If th cmd was a moquery we disable the bash mode in the apic
            if mQuery_Check[0] == "moquery":
                Shell.send('exit\n')

            #to diferenciate the output with the next cmd
            if Verbose_Mode:
                print("*" * Constant.Verbose_Mode_len)


    #Close the APIC Filename
    APIC_CMD_OUTPUT.close()

    #Close the SSH Connection
    ssh.close()

    #Close the Shell Connection
    Shell.close()

    if Constant.Upload_File_Case:
        upload_Tac_File(APIC_OUTPUT_FILENAME)



################
# Main Program #
################

if __name__ == '__main__':
    exit(get_Command_Results())
