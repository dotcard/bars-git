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

Messages = [] # ������ �� ���� ���������, �. �. ����������� � ��� �������� ������; TODO: ���������� � ��������� � ����������� �������� ����������

logging.basicConfig(format = u'%(asctime)s - %(message)s', level = logging.DEBUG, filename = u'%smsysgit\\gitForBisLog\\MackBacLog.txt' % ROOT)

def commStringOutput(strng):
  return os.popen(strng).read()

def diffsLocalRemote(ReserveRepositories): # ������ �������� ������������ ������� ���������� �� ��������
  areDiffs = False
  for s in ReserveRepositories:
    os.chdir(s.strip())
    if commStringOutput("git fetch --dry-run 2>&1"): # ���������� ����������� ��������� (����� D:\\) � ���� � ������� �����; � ������� stderror � stdout ('2>&1' - �� ������, ������ ����������: http://www.4its.ru/html/windows-cmd.html)
      logging.info("%s differs from the main repository" % s)
      areDiffs = True
      break
  return areDiffs

def folderHasChanges(folder):
  os.chdir(folder)
  return commStringOutput("git status --porcelain") # ���� �� ��������� �����? (����� � ������� ����, ��������������� ��� ������ ��������)
# ��������� ������ ���������� True ��� False, �� � ��������� ������ �� ������� ������; ���� ��� ����� ������, �� �������� ����� False

def getCurrentBranch():
  return commStringOutput("git symbolic-ref --short HEAD") # ����� ����� �������� ������� � ������� �������� �����

# MAIN--MAIN--MAIN--MAIN--MAIN--MAIN--MAIN--MAIN
logging.info("MakeBack START")

noDiffsRemote = not diffsLocalRemote(ReserveRepositories) #������� � ������� ���������, ���� ������� � �������� ������ �� ���������� �� �������� � ���������
if noDiffsRemote:
  logging.info("No diffs between local and remote repositories")
else:
  logging.info("Diffs between local and remote repositories")

#�������� �� ����������� ����������� ���������� � ���������� �������� ��������� � ���� ���� ���������
if noDiffsRemote and folderHasChanges(ROOT):
  branchName = NOW.strftime('%Y_%m_%d__%H_%M_%S') # �������� ��� ����� �����
  #������ ����� ����� ���� ��������� � �������
  if(getCurrentBranch() == "master"):
    logging.info(commStringOutput("git checkout -b %s 2>&1" % branchName))
  #��������� ��������� ��������
  logging.info(commStringOutput("git add -A . .gitignore 2>&1")) # �������� ��� ����� � ����� ������
  logging.info(commStringOutput("git commit -m %s 2>&1" % branchName)) # ������� ������ � ��������� = branchName
  #��������� ��������� � �������� �����������
  for s in ReserveRepositories:
    os.chdir(s.strip())
    CurrentBranch = getCurrentBranch()
    logging.info(commStringOutput("git fetch 2>&1")) # �������� ������������ ����� �� ��������� (����� D:\\)
    logging.info(commStringOutput("git branch --track %s origin/%s 2>&1" % (CurrentBranch, CurrentBranch)))
    logging.info(commStringOutput("git checkout %s 2>&1"  % CurrentBranch)) # ������ ����� �� CurrentBranch
    logging.info(commStringOutput("git pull 2>&1")) # ����� ���������� ����� �� ���������
    logging.info(commStringOutput("git fetch --dry-run 2>&1")) # ���������, ��� ��� �������� ����� ������� ������ � ��������
  if folderHasChanges(ROOT): # ���������, ��������� �� �� ��� ����� �������� �������
    logging.info("Unsaved changes in %s" % ROOT)
  else:
    logging.info("No unsaved changes in %s" % ROOT)

#���������� ������� ����� ������� ������ � ������ ������ � ���� GITDIFFERENCES
os.chdir(ROOT)
differences = commStringOutput("git diff --name-status master..%s" % getCurrentBranch())
logging.info("Differences between currentBranch and 'master': %s" % differences)
with open(GITDIFFERENCES, "w") as fdifference: # ����� �������� � ��������� ����
  fdifference.write(differences)

# ������ �� ������ ������
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
# ������ ������� ����� � �����, ������ ��� ��� ����������� Python
# ����� �������� if currentBranch == 'master': ��� - �� master, ��� �����