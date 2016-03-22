#!/usr/bin/env python
import sys
import os
import shutil
import time
import subprocess

class ToughError(Exception):
    def __init__(self, message):
        self.message = message

class ToughShell(object):
    
    def __init__(self,debug=False):
        self.err = lambda s: sys.stdout.write("\033[1m%s[31;2m%s%s[0m\n"%(chr(27),s, chr(27)))
        self.succ = lambda s: sys.stdout.write("\033[1m%s[32;2m%s%s[0m\n"%(chr(27),s, chr(27)))
        self.debug = lambda s: sys.stdout.write("\033[1m%s[36;2m%s%s[0m\n"%(chr(27),s, chr(27)))
        self.warn = lambda s: sys.stdout.write("\033[1m%s[35;2m%s%s[0m\n"%(chr(27),s, chr(27)))
        self.info = lambda s: sys.stdout.write("%s\n" % s)
        self.read = lambda ask,val:raw_input(ask) or val

    def wait(self,sec):
        for i in reversed(range(sec)):self.debug(str(i));time.sleep(1.0)

    def run(self,command, raise_on_fail=False, shell=True, env={},wait=0):
        self.info("RUN: %s"%command)
        run_env = os.environ.copy()
        if env:run_env.update(env)
        if wait > 0:
            subprocess.Popen(command, shell=True)
            self.wait(wait)
        else:    
            proc = subprocess.Popen(command,shell=shell,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=run_env)
            stdout, stderr = proc.communicate('through stdin to stdout')
            result = proc.returncode, stdout, stderr
            if proc.returncode > 0 and raise_on_fail:
                error_string = "# Could not run command (return code= %s)\n" % proc.returncode
                error_string += "# Error was:\n%s\n" % (stderr.strip())
                error_string += "# Command was:\n%s\n" % command
                error_string += "# Output was:\n%s\n" % (stdout.strip())
                if proc.returncode == 127:  # File not found, lets print path
                    path = os.getenv("PATH")
                    error_string += "# Check if y/our path is correct: %s" % path
                self.err(error_string)
                raise ToughError(error_string)
            else:
                if stdout.strip():
                    self.debug(stdout)
                if stderr.strip():
                    self.err(stderr)

                if proc.returncode == 0:
                    self.succ("RUN: %s success!"%command)
                else:
                    self.err("RUN: %s failure!"%command)

                return result    
                
shell = ToughShell()










