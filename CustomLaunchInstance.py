import ctypes
from windows.windows_helper import (
    HANDLE,
    INVALID_HANDLE_VALUE,
    KERNEL32,
    PAGE_READWRITE,
    PROCESS_ALL_ACCESS,
    PROCESSENTRY32,
    TH32CS_SNAPPROCESS,
    VIRTUAL_MEM,
    DWORD,
    ULONG
)


def get_process_id(processName: str) -> DWORD:
    h_snapshot: HANDLE = KERNEL32.CreateToolhelp32Snapshot(
        TH32CS_SNAPPROCESS, 0)

    structprocsnapshot = PROCESSENTRY32()
    structprocsnapshot.dwSize = ctypes.sizeof(PROCESSENTRY32)

    if h_snapshot == INVALID_HANDLE_VALUE or KERNEL32.Process32First(h_snapshot, ctypes.byref(structprocsnapshot)) == False:
        print(f"Snapshot or first process is not valid entry!\n")
        return -1

    while KERNEL32.Process32Next(h_snapshot, ctypes.byref(structprocsnapshot)):
        if structprocsnapshot.szExeFile == bytearray(processName, "utf-8"):

            print(
                f"Process {processName}. Process ID:{structprocsnapshot.th32ProcessID}\n")
            continue
            KERNEL32.CloseHandle(h_snapshot)
            return structprocsnapshot.th32ProcessID

    KERNEL32.CloseHandle(h_snapshot)
    print(f"Process {processName} not found\n")
    return -1


def inject_dll(pid: DWORD, dll_path) -> bool:
    dll_len = len(dll_path)

    h_process: HANDLE = KERNEL32.OpenProcess(
        PROCESS_ALL_ACCESS, False, pid)

    if not h_process:
        print(f"Couldn't get handle to PID: {pid}")
        return False

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
        print("Failed to inject DLL, exit...")
        return False

    print(f"Remote Thread with ID {thread_id.value} created.")
    return True


get_process_id("RSI Launcher.exe")
