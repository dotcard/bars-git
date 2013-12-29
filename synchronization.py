# -*- coding: cp1251 -*- 
import os
import sys
import logging
logging.basicConfig(format = u'%(asctime)s - %(message)s', level = logging.DEBUG)

try:
  ROOT = sys.argv[1] + ":\\"
except IndexError:
  ROOT = "D:\\"

GITOPTIONS = "%smsysgit\\gitOptions.poo" % ROOT
GIT_PULL_COMMAND = "git pull 2 > &1"

os.chdir(ROOT)


ReserveRepositories=[]
try:
  with open(GITOPTIONS) as gitOptions:
    ReserveRepositories = gitOptions.readlines()
except IOError:
  logging.info("No such file - %s" % GITOPTIONS)

for s in ReserveRepositories:
  os.chdir(s.strip())
  logging.info(os.popen(GIT_PULL_COMMAND).read()) #os.popen устарела, новый вариант - subprocess.Popen('git pull 2>&1', stdout = PIPE).stdout.read()
logging.info("synchronization END")

os.chdir(ROOT)
