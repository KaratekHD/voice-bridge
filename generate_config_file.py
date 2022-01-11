#!/usr/bin/python3

# This file is used when starting the program in a container.
import os
import toml
import inspect

# Used to get the name of a variable
def retrieve_name(var):
    for fi in reversed(inspect.stack()):
        names = [
            var_name for var_name,
            var_val in fi.frame.f_locals.items() if var_val is var]
        if len(names) > 0:
            return names[0]


# get the environment
env = os.environ


def main():
    # get all the required values from env
    discord_token = env["discord_token"]
    teamspeak_server = env["teamspeak_server"]
    teamspeak_identity = env["teamspeak_identity"]
    teamspeak_server_password = env.get("teamspeak_server_password")
    teamspeak_channel_id = env.get("teamspeak_channel_id")
    teamspeak_channel_name = env.get("teamspeak_channel_name")
    teamspeak_channel_password = env.get("teamspeak_channel_password")
    teamspeak_name = env["teamspeak_name"]
    verbose = 1 if env.get("verbose") is None else env.get("verbose")
    # Volume is not currently used
    # volume = env["volume"]

    conf = {
        "teamspeak_server": teamspeak_server,
        "teamspeak_identity": teamspeak_identity,
        "discord_token": discord_token,
        "verbose": verbose
    }

    # loop over optional values and add them to conf
    for e in (
            teamspeak_server_password,
            teamspeak_channel_id,
            teamspeak_channel_name,
            teamspeak_channel_password):
        if e is not None:
            conf[retrieve_name(e)] = e

    # print and write to file
    content = toml.dumps(conf)
    print(content)
    with open("credentials.toml", "w") as file:
        file.write(content)
        file.close()
    pass


if __name__ == "__main__":
    main()
