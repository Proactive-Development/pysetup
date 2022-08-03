import sys
import os
import configparser
from colorama import Back, Fore, Style
import requests
if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Enter a setup file to install")
        exit()
    config_path = sys.argv[-1]
    config = configparser.ConfigParser()
    config.read(config_path)
    print(Fore.CYAN+"The program named "+Fore.WHITE+config["setup"]["name"]+Fore.CYAN+" wants to install their software onto your computer")
    if config["setup"]["beta"] == "False":
        print(Fore.CYAN+"Version: "+Fore.GREEN+config["setup"]["version"]+" STABLE"+Style.RESET_ALL)
    else:
        print("Version"+Fore.RED+config["setup"]["version"]+" BETA")

    consent = input("Do you want to install this software on your system. Type ? for more info [Y/N/?]").upper()
    if consent == "Y":
        pass
    elif consent == "?":
        print(Fore.CYAN+"Install location: "+Fore.WHITE+config["setup"]["install_dir"])
        print(Fore.CYAN+"Files required to download:"+Fore.WHITE)
        for i in config["setup"]["urls"].split(","):
            print(i)
        if config["setup"]["pip"].upper() != "NONE":
            print(Fore.CYAN+"Python modules required to be installed:"+Fore.WHITE)
            for i in config["setup"]["pip"].split(","):
                print(i)
        print(Fore.RED+"After install command: "+config["setup"]["finish_command"]+Style.RESET_ALL)
        consent = input("Do you want to install this software on your system [Y/N]").upper()
        if consent == "Y":
            pass
        else:
            print("No changes have been made to your system")
            exit()
    else:
        print("No changes have been made to your system")
        exit()
        
    try:
        os.mkdir(config["setup"]["create_dir"])
    except:
        pass
    x = 1
    for i in config["setup"]["urls"].split(","):
        print("GET "+str(x)+":",i)
        url = i
        r = requests.get(url, allow_redirects=True)
        open(config["setup"]["install_dir"]+i.split("/")[-1], 'wb').write(r.content)
        x = x + 1
    if config["setup"]["pip"].upper() != "NONE":
        x = 1
        for i in config["setup"]["pip"].split(","):
            print("PIP "+str(x)+":",i)
            os.system("pip install",i)
            x = x + 1
    if config["setup"]["finish_command"].upper() != "NONE":  
        print("Running: "+config["setup"]["finish_command"])
        os.system(config["setup"]["finish_command"])
    print("Done installing!")