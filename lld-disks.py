#!/usr/bin/python
import os
import json
import sys

if __name__ == "__main__":

    # Iterate over all block devices, but ignore them if they are in the
    # skippable set
    skippable = ["sr", "loop", "ram"]
    # add user-configured skippables if appropriate
    script_path = os.path.dirname(os.path.realpath(__file__))
    skippable_filename = "{}/skippable".format(script_path)
    if os.path.isfile(skippable_filename):
        # load file and append to skippable list
        try:
            user_skippable = open(skippable_filename, 'r').read().rstrip()
            skippable = skippable + user_skippable.split(',')
        except Exception as e:
            print('could not read skippable device config "{}": {}'.format(skippable_filename, e))

    devices = (device for device in os.listdir("/sys/class/block")
               if not any(ignore in device for ignore in skippable))
    data = [{"{#DEVICENAME}": device} for device in devices]
    print(json.dumps({"data": data}, indent=4))
