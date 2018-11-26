import os
import sys
import time
import argparse
import signal
import json

#from wizardbot import start_bot
from class_wizardbot import start_bot

PID_FILE = "/tmp/wizardbot"
VERSION = "0.0.0"

def main():
    parser = argparse.ArgumentParser(description='Wizardbot manager', fromfile_prefix_chars='@',prog='PROG')
    subparsers = parser.add_subparsers()

    parser_start = subparsers.add_parser('start')
    parser_start.set_defaults(func=start_program)

    parser_stop = subparsers.add_parser('stop')
    parser_stop.set_defaults(func=stop_program)

    parser_restart = subparsers.add_parser('restart')
    parser_restart.set_defaults(func=restart_program)

    parsed = parser.parse_args()
    parsed.func(vars(parsed))

def restart_program(Args=[]):
    stop_program()
    start_program()

def start_program(Args=[]):
    pid = str(os.getpid()) ## parents proccess id

    if os.path.isfile(PID_FILE): ## checks to see if the file is there
        print("ERROR: Wizardbot is already running")
        sys.exit()

    newpid = os.fork() ## starts child process
    
    if newpid == 0: ## if this is the child process do work
        while(True): ## if the bot loses connection/errors out it needs to come back online
            try:
                open(PID_FILE, 'w').write(str(os.getpid())) ## create file and put child pid in file
                call_wizardbot()
            finally:
                os.unlink(PID_FILE)
                time.sleep(60)

    else: ## else this is the parent process still
        None ## not the forked child so do nothing

def call_wizardbot():
    print("Started Wizardbot")
    print (time.localtime())
    start_bot()
    print("Ended Wizardbot")
    print (time.localtime())

def stop_program(Args=[]):
    if os.path.isfile(PID_FILE):
        try: ## found the pidfile now attempting to kill that pid
            text_file = open(PID_FILE, "rb")
            dat = text_file.read()
            text_file.close()

            if (int(dat) != 0): ## if this is zero don't kill myself
                os.kill(int(dat), signal.SIGTERM)
            os.unlink(PID_FILE)
            print("SUCCESS: killed wizardbot")
        except OSError: ## pid wasn't valid, delete old file
            os.unlink(PID_FILE)
            print("ERROR: Wizardbot is not currently running")
        except: ## if it hits this case debug why
            print("ERROR: Could not kill wizardbot for unknown reason")

    else:
        ## pidfile was not found so I don't know what to stop
        print("ERROR: Wizardbot is not currently running")

if __name__ == '__main__':
    with open('config.json', 'r') as f:
      array = json.load(f)
    PID_FILE += array["VERSION"]
    print(PID_FILE)
    main()
