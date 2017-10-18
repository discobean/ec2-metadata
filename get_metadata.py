#!/usr/bin/env python2.7
import requests
import boto3
import time
import re
import traceback
import os

def make_request(url, timeout=10, required=True):
    print "Calling: %s" % url
    while True:
        try:
            response = requests.get(url, timeout=timeout)
        except:
            traceback.print_exc()
            print "Trying again in 1 second..."
            time.sleep(1)
            continue

        # try once more
        if response.status_code != 200:
            print "Response code (%s) trying again in 1 second..." % response.code
            time.sleep(1)
            continue

        # if no resposne, then try again
        if required and not response.text:
            continue

        return response.text

def write_variable(filename, name, value):
    print "Saving variable: %s=%s" % (name, value)

    while True:
        try:
            with open(filename, "a+") as f:
                f.write("%s=%s\n" % (name, value))

            return True
        except:
            traceback.print_exc()
            print "Trying again in 1 second..."
            time.sleep(1)
            continue

if __name__ == "__main__":
    filename = "/run/metadata/ec2"
    dir = os.path.dirname(filename)

    if not os.path.isdir(dir):
        print "Making directory %s" % dir
        os.mkdir(dir)

    if os.path.isfile(filename):
        print "Deleting old file %s" % filename
        os.remove(filename)

    print "Saving to file: %s" % filename
    value = make_request("http://169.254.169.254/2016-09-02/meta-data/local-ipv4")
    write_variable(filename, "AWS_LOCAL_IPV4", value)

    value = make_request("http://169.254.169.254/2016-09-02/meta-data/instance-id")
    write_variable(filename, "AWS_INSTANCE_ID", value)

    value = make_request("http://169.254.169.254/2016-09-02/meta-data/placement/availability-zone")
    write_variable(filename, "AWS_AVAILABILITY_ZONE", value)
    write_variable(filename, "AWS_REGION", re.sub(r'[a-z]$', '', value))
