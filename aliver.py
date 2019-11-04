from vivaldialive import VivaldiAlive
from pathlib import Path
import configparser
import pprint as pp
import os

CWD = "/".join(str(Path(__file__).resolve()).split("/")[:6])
config = configparser.ConfigParser()
config.read(CWD + "/config.txt")

done = ["IrieYarn"]

usernames = [
    "AngelinaJolie",
    "BradPitt",
    "DanielRadcliffe",
    "EmmaStone",
    "GeorgeClooney",
    "JakeGyllenhaal",
    "JenniferLawrence",
    "KristenStewart",
    "RalphFiennes",
    "SandraBullock",
    "ScarlettJohansson",
    "jenniferlawrence",
    "priyapunia",
    "tigershroff",
]

usernames = [x for x in usernames if x not in done]
if os.path.exists(CWD + "/done.txt"):
    with open(CWD + "/done.txt", "r") as file:
        read_lines = file.readlines()
    dynamic_dones = [line.replace("\n", "") for line in read_lines]
    dynamic_dones = list(set(dynamic_dones))
    usernames = [x for x in usernames if x not in dynamic_dones]

successful = []
failed = []
with open(CWD + "/done.txt", "a+") as file:
    file.write("\n")
for username in usernames:
    try:
        vivaldi_password = config.get("configuration", username + "_password")
        session = VivaldiAlive(
            vivaldi=username, vivaldi_password=vivaldi_password, headless=False
        )
        session.check_mail()
        successful.append(username)
        with open(CWD + "/done.txt", "a+") as file:
            file.write(username + "\n")
    except Exception as e:
        failed.append(username)
with open(CWD + "/done.txt", "a+") as file:
    file.write("\n")

print("successful:")
pp.pprint(successful)

print("failed:")
pp.pprint(failed)
