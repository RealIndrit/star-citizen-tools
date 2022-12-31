from windows.utils import get_process_id, get_thread_id, inject_dll


pids = get_process_id("RSI Launcher.exe")
tids = get_thread_id(list(pids))
print(pids)
print(tids)

# Still working on the core helper functions that will make the memory mapping and process modification a lot easier
