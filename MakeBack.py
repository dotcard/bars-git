# -*- coding: cp1251 -*- 
import os
import sys
import logging
import datetime
from datetime import datetime

try:
  ROOT = sys.argv[1] + ":\\"
except IndexError:
  ROOT = "D:\\"

GITOPTIONS = "%smsysgit\\gitOptions.poo" % ROOT
GITMESSAGES = "%smsysgit\\GitMessages" % ROOT
GITDIFFERENCES = "%smsysgit\\gitdifferences" % ROOT
GITFORBISLOG = "%smsysgit\\gitForBisLog\\" % ROOT
PERIOD_BEFORE_DEL = 365
NOW = datetime.now()

ReserveRepositories=[]
try:
  with open(GITOPTIONS) as gitOptions:
    ReserveRepositories = gitOptions.readlines()
except IOError:
  logging.info("No such file - %s" % GITOPTIONS)
  sys.exit(2)

Messages = [] # убрано во всей программе, т. к. встречается в трёх ненужных местах; TODO: посмотреть в оригинале и максимально смягчить отсутствие

logging.basicConfig(format = u'%(asctime)s - %(message)s', level = logging.DEBUG, filename = u'%smsysgit\\gitForBisLog\\MackBacLog.txt' % ROOT)

def commStringOutput(strng):
  return os.popen(strng).read()

def diffsLocalRemote(ReserveRepositories): # список удалённых репозиториев которые отличаются от главного
  areDiffs = False
  for s in ReserveRepositories:
    os.chdir(s.strip())
    if commStringOutput("git fetch --dry-run 2>&1"): # изобразить копирование источника (диска D:\\) в клон в текущей папке; с выводом stderror в stdout ('2>&1' - не менять, полная информация: http://www.4its.ru/html/windows-cmd.html)
      logging.info("%s differs from the main repository" % s)
      areDiffs = True
      break
  return areDiffs

def folderHasChanges(folder):
  os.chdir(folder)
  return commStringOutput("git status --porcelain") # есть ли изменённые файлы? (вывод в кратком виде, форматированном для чтения скриптом)
# программа раньше возвращала True или False, но я переделал просто на возврат строки; если она будет пустой, то значение будет False

def getCurrentBranch():
  return commStringOutput("git symbolic-ref --short HEAD") # нашёл более короткую команду с выводом названия ветки

# MAIN--MAIN--MAIN--MAIN--MAIN--MAIN--MAIN--MAIN
logging.info("MakeBack START")

noDiffsRemote = not diffsLocalRemote(ReserveRepositories) #система в рабочем состоянии, если коммиты в удалённых ветках не отличаются от коммитов в локальных
if noDiffsRemote:
  logging.info("No diffs between local and remote repositories")
else:
  logging.info("Diffs between local and remote repositories")

#проверка на возможность дальнейшего выполнения и выполнение основной процедуры и если есть изменения
if noDiffsRemote and folderHasChanges(ROOT):
  branchName = NOW.strftime('%Y_%m_%d__%H_%M_%S') # название для новой ветки
  #создаём новую ветку если находимся в мастере
  if(getCurrentBranch() == "master"):
    logging.info(commStringOutput("git checkout -b %s 2>&1" % branchName))
  #сохраняем изменения локально
  logging.info(commStringOutput("git add -A . .gitignore 2>&1")) # добавить все файлы в общий индекс
  logging.info(commStringOutput("git commit -m %s 2>&1" % branchName)) # создать коммит с названием = branchName
  #сохраняем изменения в удалённые репозитории
  for s in ReserveRepositories:
    os.chdir(s.strip())
    CurrentBranch = getCurrentBranch()
    logging.info(commStringOutput("git fetch 2>&1")) # копируем отличающиеся файлы из источника (диска D:\\)
    logging.info(commStringOutput("git branch --track %s origin/%s 2>&1" % (CurrentBranch, CurrentBranch)))
    logging.info(commStringOutput("git checkout %s 2>&1"  % CurrentBranch)) # меняем ветку на CurrentBranch
    logging.info(commStringOutput("git pull 2>&1")) # тянем обновлённые файлы из источника
    logging.info(commStringOutput("git fetch --dry-run 2>&1")) # проверяем, что нет различий между текущей папкой и удалённой
  if folderHasChanges(ROOT): # проверяем, изменился ли за это время корневой каталог
    logging.info("Unsaved changes in %s" % ROOT)
  else:
    logging.info("No unsaved changes in %s" % ROOT)

#записываем разницу между текущей веткой и веткой мастер в файл GITDIFFERENCES
os.chdir(ROOT)
differences = commStringOutput("git diff --name-status master..%s" % getCurrentBranch())
logging.info("Differences between currentBranch and 'master': %s" % differences)
with open(GITDIFFERENCES, "w") as fdifference: # пишем значения в отдельный файл
  fdifference.write(differences)

# чистка от старых файлов
dir_to_search = os.path.curdir
for dirpath, dirnames, filenames in os.walk(GITFORBISLOG):
  for filename in filenames:
    full_filename = os.path.join(dirpath, filename)
    age_of_file_in_secs = os.path.getmtime(full_filename)
    when_file_was_modified = datetime.fromtimestamp(age_of_file_in_secs)
    if (NOW - when_file_was_modified).days > PERIOD_BEFORE_DEL:
      os.remove(full_filename)

logging.info("MakeBack END")

sys.exit(0)
# сделал обычный выход с кодом, потому что так рекомендует Python
# убрал странное if currentBranch == 'master': она - не master, это точно