# SeCrypt

simple file security solution

Current features/functions:
- basic GUI built using Tkinter
- locks all files within a folder using bcrypt and Fernet
- allows for random generation of passwords
- hides hash key and pass keys using ADS

future implementations:
- selection of individual files (currently locks all in "files" folder)
- hide hash and pass keys in file using ADS
- locked files when opened with run python script to open tkinter window to prompt unlocking
- 2FA and/or mobile authentication
- salting of passwords
- locks downloaded files containing sensitive information
