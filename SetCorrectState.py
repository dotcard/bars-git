# -*- coding: cp1251 -*- 
import os
import sys
import logging
import datetime

try:
  ROOT = sys.argv[1] + ":\\"
except IndexError:
  ROOT = "D:\\"

GITDIFFERENCES = "%smsysgit\\gitdifferences" % ROOT
NOW = datetime.datetime.now()

logging.basicConfig(format = u'%(asctime)s - %(message)s', level = logging.DEBUG, filename = u'%smsysgit\\gitForBisLog\\MackBacLog.txt' % ROOT)

def commStringOutput(strng):
  return os.popen(strng).read()

def getCurrentBranch():
  return commStringOutput("git symbolic-ref --short HEAD") # нашёл более короткую команду с выводом названия ветки

def SaveChangeToRemote():
  ReserveRepositories=[]
  try:
    with open(GITOPTIONS) as gitOptions:
      ReserveRepositories = gitOptions.readlines()
  except IOError:
    logging.info("No such file - %s" % GITOPTIONS)
    sys.exit(2)

  for s in ReserveRepositories:
    os.chdir(s)
    logging.info(commStringOutput("git checkout master 2>&1"))
    logging.info(commStringOutput("git pull 2>&1"))
  logging.info("SaveChangeToRemote END")
  os.chdir(ROOT)

def SaveDiffsToLog(): # непонятная процедура пересохранения в основной лог различий из GITDIFFERENCES
  # вычитываем из файла GITDIFFERENCES различия
  logging.info("modified files:")
  with open(GITDIFFERENCES, "r") as f:
    differences = f.read()
  logging.info(differences)

#MAIN--MAIN--MAIN--MAIN--MAIN--MAIN--MAIN--MAIN
logging.info("SetCorrectState START")

os.chdir(ROOT)
code = 0

if (len(sys.argv[2:]) == 0): # параметров мало
  logging.info("too few arguments")
  code = 1

if(getCurentBranch() == "master"): # в мастере, ничего изменять не нужно
  logging.info("we are in master branch") # и чо?

if(sys.argv[2] == "M"): #переход в прошлое подтверждённое состояние
  # ждём, пока закроется IGIT
  isIGIT = commStringOutput("tasklist").find("IGIT.exe")
  while(isIGIT != -1):
    print("IGIT is running")
    time.sleep(0.5)
  SaveDiffsToLog()
  logging.info(commStringOutput("git checkout master 2>&1"))
  #save changes to remote repositories
  SaveChangeToRemote()
  logging.info("goToMaster END")

elif(sys.argv[2] == "C"): #устанавливаем текущеее состояние подтверждённым
  # почему-то не ждём, пока закроется IGIT
  SaveDiffsToLog()
  logging.info(commStringOutput("git branch -f master %s 2>&1") % getCurentBranch())
  logging.info(commStringOutput("git checkout master 2>&1"))
  #save changes to remote repositories
  SaveChangeToRemote()
  logging.info("MargeCurentAndMaster END")

sys.exit(code)
# сделал обычный выход с кодом, потому что так рекомендует Python
# убрал функцию WriteToLog, дублирующуюся встроенными функциями Python