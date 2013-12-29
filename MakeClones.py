# -*- coding: cp1251 -*- 
import os
import sys
import logging

try:
  ROOT = sys.argv[1] + ":\\"
except IndexError:
  ROOT = "D:\\"

GITOPTIONS = "%smsysgit\\gitOptions.poo" % ROOT

logging.basicConfig(format = u'%(asctime)s - %(message)s', level = logging.DEBUG, filename = u'%smsysgit\\gitForBisLog\\MakeClonesLog.txt' % ROOT)

logging.info("MakeClones START")
os.chdir(ROOT)
ReserveRepositories=[]

try:
  with open(GITOPTIONS) as gitOptions:
    ReserveRepositories = gitOptions.readlines()
except IOError:
  logging.info("No such file - %s" % GITOPTIONS)

for s in ReserveRepositories:
  os.chdir(s.strip())
  logging.info(os.popen("git clone %s %s 2>&1" % (ROOT, s)).read()) #os.popen устарела, новый вариант - subprocess.Popen('git pull 2>&1', stdout = PIPE).stdout.read()

logging.info("MakeClones END")
os.chdir(ROOT)

#Судя по программе, в ней выполняется клонирование корня диска D в папки из файла GITOPTIONS, после чего диск D в конфигурации git в папках помечается как удалённый репозиторий