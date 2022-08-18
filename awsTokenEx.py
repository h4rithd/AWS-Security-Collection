#!/usr/bin/python3
import os
import textwrap
import argparse
from pathlib import Path
from colorama import init, Fore

init()

GREEN = Fore.GREEN
RED   = Fore.RED
BLUE  = Fore.BLUE
RESET = Fore.RESET

def exportToken(token,profile):
	with open(token,'r') as file:
		text = file.read().replace('\\n', '\n')

	AccessKey = [line for line in text.split('\n') if "AWS_ACCESS_KEY_ID" in line][0].split("=")[1]
	SecretKey = [line for line in text.split('\n') if "AWS_SECRET_ACCESS_KEY" in line][0].split("=")[1]
	SessionToken = [line for line in text.split('\n') if "AWS_SESSION_TOKEN" in line][0].split("=")[1]

	with open(os.path.expanduser("~/.aws/credentials"), "a") as outfile:
		outfile.write(f'\n[{profile}]\n')
		outfile.write(f'aws_access_key_id = {AccessKey}\n')
		outfile.write(f'aws_secret_access_key = {SecretKey}\n')
		outfile.write(f'aws_session_token = {SessionToken}\n')

	print (f'{GREEN}[SUCCESS]{RESET} Profile name {BLUE}{profile}{RESET} has been imported!')


if __name__ == "__main__":

	parser = argparse.ArgumentParser(
		prog='awsTokenEx.py',
		formatter_class=argparse.RawDescriptionHelpFormatter,
		description=textwrap.dedent('''\
	-------------------------------------------------------------
	--------------- | Bulk SSH Login check |---------------------
	-------------------------------------------------------------
		    _            _____    _            ___     
		   /_\__ __ ____|_   _|__| |_____ _ _ | __|_ __
		  / _ \ V  V (_-< | |/ _ \ / / -_) ' \| _|\ \ /
		 /_/ \_\_/\_//__/ |_|\___/_\_\___|_||_|___/_\_
					by h4rith.com
	-------------------------------------------------------------'''),
		usage='python3 %(prog)s -f [env_file] -p [ProfileName] ',
		epilog='---------------- Script from h4rithd.com ----------------'
	)

	parser._action_groups.pop()
	required = parser.add_argument_group('[!] Required arguments')
	optional = parser.add_argument_group('[!] Optional arguments')

	required.add_argument("-f", "--file", metavar='', required=True, help="Environment variable file that contain token.") 
	required.add_argument("-p", "--profile", metavar='', required=True, help="Valid profile name.") 
	args = parser.parse_args()

	with open(f"{Path.home()}/.aws/credentials",'r') as file:
		text = file.read()
		if f'[{args.profile}]' in text:
			print(f'{RED}[ERROR] Profile {BLUE}{args.profile}{RESET} name is alrady exist on {Path.home()}/.aws/credentials file!')
		else:
			exportToken(args.file,args.profile)	
