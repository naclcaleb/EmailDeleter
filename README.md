# EmailDeleter
Trashes Useless emails based on a given filter

The EmailDeleter goes through all the emails in a particular Gmail mailbox, and moves them to trash if the sender matches a specified regex.

## Requirements
python3
git (optional)

## Config
Start by defining parameters in the `config.json`file. The options for this file are described below:
`"whitelisted_senders":{

}`

The `whitelisted_senders` object defines a list of senders whose emails to you should never be deleted by the program.
Add them by giving them an index and an email address, as a key/value pair: `"0": "example@example.com"`

```
"credentials": {
  "email": "example@example.com",
  "password": "password"
}
```
The `credentials` object defines your email address and password to be used by the program.

```
"imap_server": "imap.example.com"
```

The `imap_server` value defines the IMAP server that the program will use. Defaults to `imap.gmail.com`.

```
"mailbox": "inbox"
```

The mailbox that the program should search. Defaults to `inbox`.

```
"regex_filter": "regex"
```

The regex used to match sender addresses.


## Running

To run the program, run `git clone https://github.com/naclcaleb/EmailDeleter && cd EmailDeleter`, then run `python3 main.py`.
(On Windows, you will have to specify the path to the Python executable, unless you have added Python to your `PATH`)
