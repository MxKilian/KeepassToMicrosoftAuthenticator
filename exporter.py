import sys
import os
import pandas as pd
from getpass import getpass
from pykeepass import PyKeePass


def skip_if_entry(kp_entry):
    if kp_entry.title is None or kp_entry.url is None or kp_entry.username is None or kp_entry.password is None:
        return True


def read_password():
    return getpass()


def validate_input():
    if len(sys.argv) < 2:
        print("Too few parameters. Please specify database and kee file path.")
        exit(0)

validate_input()

# Paths
database_path = sys.argv[1]
key_path = sys.argv[2]
password = read_password()

# Database
db = PyKeePass(database_path, password, key_path)

# Entries
db_entries = db.entries

# Loop over all available entries
data = []
for entry in db_entries:
    if skip_if_entry(entry):
        continue
    data.append([entry.title, entry.url, entry.username, entry.password])

# Create CSV
export_csv = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') + '/exported.csv'
data_frame = pd.DataFrame(data, columns=['name', 'url', 'username', 'password'])
data_frame.to_csv(export_csv, sep=',', index=False, encoding='utf-8')
