from ctypes import CDLL
from subprocess import Popen, PIPE
import time
from windows.utils import *
from windows.windows_helper import *


pids = get_processes_for("RSI Launcher.exe")
print(pids)
tids0 = get_threads_for(pids[0])
tids1 = get_threads_for(pids[1])
tid2 = get_threads_for(pids[2])


hProcess: HANDLE = open_process(PROCESS_ALL_ACCESS, False, pids[0])
#hThread: HANDLE = open_thread(THREAD_ALL_ACCESS, False, tids[33][0])

#print(terminate_thread(hThread, 0))

#print("Freezing process")
#print(terminate_process(hProcess, 0))
print(suspend_process(hProcess))
time.sleep(60)
print(resume_process(hProcess))
# print(suspend_thread_test(tids1[0]))

#print("Resuming process")
# terminate_process(pids[0])
# Still working on the core helper functions that will make the memory mapping and process/thread modification a lot easier
