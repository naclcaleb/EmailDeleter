#!/usr/bin/python3
import imaplib
import email
import base64
import xlwt
import re
import json
import sys

#For colored prints
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def read_file(filename):
	file = open(filename, "r+")
	output = file.read()
	file.close()
	return output

#Read config file
config = json.loads( read_file('config.json') )

#Whitelist
whitelisted_senders = []
for i in config["whitelisted_senders"]:
	whitelisted_senders.append(config["whitelisted_senders"][i])


#Credentials
personal_email = ""
password = ""

if "credentials" in config:
	print(bcolors.OKGREEN + "Loading credentials from config file" + bcolors.ENDC)
	personal_email = config["credentials"]["email"]
	password = config["credentials"]["password"]
else:
	print(bcolors.OKGREEN + "Please enter your email and password" + bcolors.ENDC)
	personal_email = input("Email: ") 
	password = input("Password: ")


#Connect to Gmail
imap_server = ""

if "imap_server" in config:
	print(bcolors.OKGREEN + "Using IMAP server '{}'".format(config["imap_server"]) + bcolors.ENDC)
	imap_server = config["imap_server"]
else:
	print(bcolors.WARNING + "No IMAP server specified in config. Defaulting to 'imap.gmail.com'..." + bcolors.ENDC)
	imap_server = 'imap.gmail.com'


Mailbox = imaplib.IMAP4_SSL(imap_server)

try:
	Mailbox.login(personal_email, password)
except:
	print(bcolors.FAIL + "Mail login failed. Exiting..." + bcolors.ENDC)
	sys.exit()

mailbox = ''

if "mailbox" not in config:
	print(bcolors.WARNING + "No mailbox specified in config. Defaulting to 'inbox'..." + bcolors.ENDC)
	mailbox = 'inbox'
else:
	mailbox = str('"{}"').format(config["mailbox"])

Mailbox.select(mailbox)

#Fetch Emails
print("Fetching mail, please wait...")

result, data = Mailbox.search(None, "ALL")

ids = data[0]
id_list = ids.split()


#Open a spreadsheet
book = xlwt.Workbook()
sheet = book.add_sheet("Deleted")

#Keep track of the rows
row = 0

to_delete = []


for i in range(len(id_list)):
	latest = id_list[-i]

	result, new_email = Mailbox.fetch(latest, "(RFC822)")

	raw_email = new_email[0][1]

	email_message = email.message_from_bytes(raw_email)

	hdr = email.header.make_header(email.header.decode_header(email_message["From"]))
	from_data = email.utils.parseaddr(email_message["From"])

	if "regex_filter" not in config:
		print(bcolors.FAIL + "No regex filter specified in config. Exiting..." + bcolors.ENDC)
		sys.exit()

	regex = config["regex_filter"]

	if re.search(regex, from_data[1]) != None and not (from_data[1] in whitelisted_emails):
		#The email matches the regex, so we'll delete it
		print(bcolors.OKBLUE + "Deleting email from " + from_data[1] + bcolors.ENDC)

		#Write the data
		sheet.write(row, 0, from_data[0])
		sheet.write(row, 1, from_data[1])

		#Delete the email
		to_delete.append(latest)
		

		#Increment the row
		row += 1

	else:
		print(".")

book.save("deleted_emails.xls")

imsure = input(bcolors.WARNING + "View 'deleted_emails.xls' for a list of emails to be deleted.\n" + bcolors.ENDC + bcolors.OKGREEN + " Confirm Trashing? " + bcolors.ENDC)

if 'y' in imsure:

	for i in to_delete:
		Mailbox.store(latest, '+X-GM-LABELS', '\\Trash')

	Mailbox.expunge()
	Mail.close()
	Mail.logout()

	print(bcolors.OKGREEN + "Successfully moved emails to trash." + bcolors.ENDC)
else:
	print(bcolors.FAIL + "Abort" + bcolors.ENDC)
