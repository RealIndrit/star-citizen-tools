import ctypes
from windows.error import InvalidHandle, ProcessNotFound, ProcessInjectionFailed, ThreadNotFound
from windows.windows_helper import (
    HANDLE,
    INVALID_HANDLE_VALUE,
    KERNEL32,
    PAGE_READWRITE,
    PROCESS_ALL_ACCESS,
    PROCESSENTRY32,
    TH32CS_SNAPPROCESS,
    TH32CS_SNAPTHREAD,
    THREAD_SUSPEND_RESUME,
    THREADENTRY32,
    VIRTUAL_MEM,
    DWORD,
    ULONG,
    open_thread,
    resume_thread,
    suspend_thread,
    wow64_suspend_thread,
    open_process
)


def get_processes_for(processName: str) -> tuple[DWORD]:
    found_ids = []
    h_snapshot: HANDLE = KERNEL32.CreateToolhelp32Snapshot(
        TH32CS_SNAPPROCESS, 0)

    pe = PROCESSENTRY32()
    pe.dwSize = ctypes.sizeof(PROCESSENTRY32)

    if h_snapshot == INVALID_HANDLE_VALUE or KERNEL32.Process32First(h_snapshot, ctypes.byref(pe)) == False:
        raise InvalidHandle

    while KERNEL32.Process32Next(h_snapshot, ctypes.byref(pe)):
        if pe.szExeFile == bytearray(processName, "utf-8"):
            found_ids.append(pe.th32ProcessID)

    if not found_ids:
        raise ProcessNotFound(f"{processName} is not a targetable process")
    KERNEL32.CloseHandle(h_snapshot)
    return tuple(found_ids)


def get_threads_for(pid) -> tuple[DWORD]:
    found_ids = []
    h_snapshot: HANDLE = KERNEL32.CreateToolhelp32Snapshot(
        TH32CS_SNAPTHREAD, 0)

    te = THREADENTRY32()
    te.dwSize = ctypes.sizeof(THREADENTRY32)
    if h_snapshot == INVALID_HANDLE_VALUE or KERNEL32.Thread32First(h_snapshot, ctypes.byref(te)) == False:
        raise InvalidHandle

    while KERNEL32.Thread32Next(h_snapshot, ctypes.byref(te)):
        if te.th32OwnerProcessID == pid:
            found_ids.append(te.th32ThreadID)
    if not found_ids:
        # Should be impossible if not suspendended assuming the pid exists
        raise ThreadNotFound(f"Found no threads for {pid}")
    KERNEL32.CloseHandle(h_snapshot)
    return tuple(found_ids)


# Replaced by resume_process and suspend_process in NTDLL
"""
def suspend_process(pid: DWORD, x64: bool = True):
    print(pid)
    for tid in get_threads_for(pid):
        hThread: HANDLE = open_thread(
            THREAD_SUSPEND_RESUME, False, tid)
        if x64:
            suspend_thread(hThread)
        else:
            wow64_suspend_thread(hThread)
        KERNEL32.CloseHandle(hThread)


def resume_process(pid):
    for tid in get_threads_for(pid):
        hThread: HANDLE = open_thread(
            THREAD_SUSPEND_RESUME, False, tid)
        resume_thread(hThread)
        KERNEL32.CloseHandle(hThread)
"""


def inject_dll(pid: DWORD, dll_path) -> bool:
    dll_len = len(dll_path)

    h_process: HANDLE = open_process(
        PROCESS_ALL_ACCESS, False, pid)

    if not h_process:
        raise ProcessNotFound(f"{pid} is not a targetable process")

    # Allocate space for DLL path
    arg_address = KERNEL32.VirtualAllocEx(
        h_process, 0, dll_len, VIRTUAL_MEM, PAGE_READWRITE)

    # Write DLL path to allocated space
    written = ULONG(0)
    KERNEL32.WriteProcessMemory(h_process, arg_address,
                                dll_path, dll_len, ctypes.byref(written))

    # Resolve LoadLibraryA Address
    h_kernel32 = KERNEL32.GetModuleHandleA("kernel32.dll")
    h_loadlib = KERNEL32.GetProcAddress(h_kernel32, "LoadLibraryA")

    # Now we createRemoteThread with entrypoiny set to LoadLibraryA and pointer to DLL path as param
    thread_id = DWORD(0)

    if not KERNEL32.CreateRemoteThread(h_process, None, 0, h_loadlib, arg_address, 0, ctypes.byref(thread_id)):
        raise ProcessInjectionFailed()

    print(f"Remote Thread with ID {thread_id.value} created.")
    KERNEL32.CloseHandle(h_process)
    return True
