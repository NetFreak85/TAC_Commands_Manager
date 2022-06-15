###################################################################
# Constant Declaration for SSH Connection into the Network Device #
###################################################################
# coding=utf-8

#Cisco Support Ticket Number
#example: SR_Ticket = "123456789"
SR_Ticket = ""

#Cisco Support Ticket Token
Token = ""

#Cisco Support URL
URL = 'https://cxd.cisco.com/home/'

#Variable that help you to print * in the verbose mode
Verbose_Mode_len = 100

#Boolean variable to upload or not the file to Cisco Cloud
Upload_File_Case = False

#Network Device Username
#Example: User = "admin"
User = ""

#Network Device Password
#Example: Password = "Password"
Password = ""

#Network Device Name or IP Address
#NetworkDevice = "www.cisco.com"
NetworkDevice = ""

#Network Device Command line List
CMD_FILE_PATH = "Command_List.txt"

#Network Device SSH Port number
NetworkDevice_SSH_Port = 22

#SSH Network Device Buffer
NetworkDeviceMaxBuffer = 65535

#Idle Time waiting for the SSH Responds
Time_Sleep = 30
