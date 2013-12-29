# -*- coding: cp1251 -*- 
import os
import sys

try:
  ROOT = sys.argv[1] + ":\\"
except IndexError:
  ROOT = "D:\\"

GITOPTIONS = "%smsysgit\\gitOptions.poo" % ROOT

try:
  HESH = sys.argv[2]
except IndexError:
  HESH = "HEAD"

os.chdir(ROOT)
os.system("git revert %s --no-edit" % HESH)

ReserveRepositories = []
try:
  with open(GITOPTIONS) as gitOptions:
    ReserveRepositories = gitOptions.readlines()
except IOError:
  print "No such file - %s" % GITOPTIONS

for s in ReserveRepositories:
  os.chdir(s.strip())
  os.system("git pull")

os.chdir(ROOT)
