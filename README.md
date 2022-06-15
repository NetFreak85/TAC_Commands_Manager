Send commands to Cisco ACI Fabric in order to collect all TAC information required

<!-- ABOUT THE PROJECT -->
## About the Project

TAC_Commands_Manager 
====================

The purpose of this code is to grant a easy way to Send commands to Cisco ACI Fabric in order to collect all Cisco TAC information required.

<!-- GETTING STARTED -->
## Getting Started

In this Script we will be able to take all the information required by Cisco TAC with all commands inserted in the file Command_List.txt.

Before you execute the script you should complete the Constant.py file with the following information:

1.  SR_Ticket
2.  Token
3.  Upload_File_Case (True or False)
4.  User
5.  Password
6.  NetworkDevice (IP Address or DNS name)

### Installation

1.  Clone the Project:
        ``git clone https://github.com/NetFreak85/TAC_Commands_Manager.git``

Usage
=====

1.  Configure the ``Constants.py`` file with the credentials information and the APIC IP address (or DNS name)
2.  Execute the ``CommandsManager.py`` with Python 3  

Contributing
============

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
Please make sure to update tests as appropriate.

<!-- LICENSE -->
## License

Do whatever you want with the script. I created it for helping the Cisco Community

<!-- CONTACT -->
## Contact

Email : jrguerra71@hotmail.com
