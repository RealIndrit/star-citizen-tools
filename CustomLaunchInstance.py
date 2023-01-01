from windows.utils import *
from windows.windows_helper import *


pids = get_processes_for("RSI Launcher.exe")
tids = get_threads_for(list(pids))
print(pids)
print(tids)

#hProcess: HANDLE = open_process(PROCESS_ALL_ACCESS, False, pids[0])
hThread: HANDLE = open_thread(THREAD_ALL_ACCESS, False, tids[33][0])
#print(terminate_process(hProcess, 0))
print(terminate_thread(hThread, 0))


# Still working on the core helper functions that will make the memory mapping and process/thread modification a lot easier
