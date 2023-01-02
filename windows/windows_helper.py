# https://learn.microsoft.com/en-us/windows/win32/winprog/windows-data-types
# https://learn.microsoft.com/en-us/windows/win32/api/tlhelp32/ns-tlhelp32-processentry32
# https://learn.microsoft.com/en-us/windows/win32/api/tlhelp32/ns-tlhelp32-threadentry32
# https://learn.microsoft.com/en-us/windows/win32/procthread/scheduling-priorities
# https://docs.python.org/3/library/ctypes.html
# https://learn.microsoft.com/en-us/windows-hardware/drivers/kernel/what-does-the-zw-prefix-mean-

import ctypes
from ctypes.wintypes import *

KB = 1024
KERNEL32 = ctypes.windll.kernel32
NT = ctypes.windll.ntdll
INVALID_HANDLE_VALUE = -1

# Standard permission flags
STANDARD_RIGHTS_REQUIRED = 0x000F0000
DELETE = 0x00010000
READ_CONTROL = 0x00020000
SYNCHRONIZE = 0x00100000
WRITE_DAC = 0x00040000
WRITE_OWNER = 0x00080000

STANDARD_RIGHTS_ALL = (DELETE | READ_CONTROL |
                       WRITE_DAC | WRITE_OWNER | SYNCHRONIZE)
STANDARD_RIGHTS_EXECUTE = READ_CONTROL
STANDARD_RIGHTS_READ = READ_CONTROL
STANDARD_RIGHTS_REQUIRED = (DELETE | READ_CONTROL | WRITE_DAC | WRITE_OWNER)
STANDARD_RIGHTS_WRITE = READ_CONTROL

# Snapshot flags
TH32CS_INHERIT = 0x80000000
TH32CS_SNAPHEAPLIST = 0x00000001
TH32CS_SNAPMODULE = 0x00000008
TH32CS_SNAPMODULE32 = 0x00000010
TH32CS_SNAPPROCESS = 0x00000002
TH32CS_SNAPTHREAD = 0x00000004
TH32CS_SNAPALL = (TH32CS_SNAPHEAPLIST | TH32CS_SNAPMODULE |
                  TH32CS_SNAPPROCESS | TH32CS_SNAPTHREAD)

# Process permission flags
PROCESS_CREATE_PROCESS = 0x0080
PROCESS_CREATE_THREAD = 0x0002
PROCESS_DUP_HANDLE = 0x0040
PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
PROCESS_SET_INFORMATION = 0x0200
PROCESS_SET_QUOTA = 0x0100
PROCESS_SUSPEND_RESUME = 0x0800
PROCESS_TERMINATE = 0x0001
PROCESS_VM_OPERATION = 0x0008
PROCESS_VM_READ = 0x0010
PROCESS_VM_WRITE = 0x0020
# I have no idea what the 0xFFFF Flag is for, but its in the docs XD
PROCESS_ALL_ACCESS = (STANDARD_RIGHTS_REQUIRED | SYNCHRONIZE | 0xFFFF)


THREAD_DIRECT_IMPERSONATION = 0x0200
THREAD_GET_CONTEXT = 0x0008
THREAD_IMPERSONATE = 0x0100
THREAD_QUERY_INFORMATION = 0x0040
THREAD_QUERY_LIMITED_INFORMATION = 0x0800
THREAD_SET_CONTEXT = 0x0010
THREAD_SET_INFORMATION = 0x0020
THREAD_SET_LIMITED_INFORMATION = 0x0400
THREAD_SET_THREAD_TOKEN = 0x0080
THREAD_SUSPEND_RESUME = 0x0002
THREAD_TERMINATE = 0x0001
THREAD_ALL_ACCESS = (STANDARD_RIGHTS_REQUIRED |
                     THREAD_TERMINATE | THREAD_SUSPEND_RESUME | THREAD_SET_CONTEXT | THREAD_SET_INFORMATION | THREAD_SET_THREAD_TOKEN | THREAD_GET_CONTEXT | THREAD_DIRECT_IMPERSONATION | THREAD_QUERY_INFORMATION)

# Priority flags process
ABOVE_NORMAL_PRIORITY_CLASS = 0x00008000
BELOW_NORMAL_PRIORITY_CLASS = 0x00004000
HIGH_PRIORITY_CLASS = 0x00000080
IDLE_PRIORITY_CLASS = 0x00000040
NORMAL_PRIORITY_CLASS = 0x00000020
PROCESS_MODE_BACKGROUND_BEGIN = 0x00100000
PROCESS_MODE_BACKGROUND_END = 0x00200000
REALTIME_PRIORITY_CLASS = 0x00000100

# Priority flags thread
THREAD_MODE_BACKGROUND_BEGIN = 0x00010000
THREAD_MODE_BACKGROUND_END = 0x00020000

THREAD_PRIORITY_ABOVE_NORMAL = 1
THREAD_PRIORITY_BELOW_NORMAL = -1
THREAD_PRIORITY_HIGHEST = 2
THREAD_PRIORITY_IDLE = -15
THREAD_PRIORITY_LOWEST = -2
THREAD_PRIORITY_NORMAL = 0
THREAD_PRIORITY_TIME_CRITICAL = 15

PAGE_READWRITE = 0x04

VIRTUAL_MEM = (0x1000 | 0x2000)

INT8 = ctypes.c_int8
UINT8 = ctypes.c_uint8
INT16 = ctypes.c_int16
UINT16 = ctypes.c_uint16
INT32 = ctypes.c_int32
UINT32 = ctypes.c_uint32
INT64 = ctypes.c_int64
UINT64 = ctypes.c_uint64

DWORDLONG = UINT64

# typedef struct tagPROCESSENTRY32 {
#    DWORD     dwSize
#    DWORD     cntUsage
#    DWORD     th32ProcessID
#    ULONG_PTR th32DefaultHeapID
#    DWORD     th32ModuleID
#    DWORD     cntThreads
#    DWORD     th32ParentProcessID
#    LONG      pcPriClassBase
#    DWORD     dwFlags
#    CHAR      szExeFile[MAX_PATH]
# } PROCESSENTRY32


class PROCESSENTRY32(ctypes.Structure):
    _fields_ = [
        ('dwSize', DWORD),
        ('cntUsage', DWORD),
        ('th32ProcessID', DWORD),
        ('th32DefaultHeapID', PULONG),
        ('th32ModuleID', DWORD),
        ('cntThreads', DWORD),
        ('th32ParentProcessID', DWORD),
        ('pcPriClassBase', LONG),
        ('dwFlags', DWORD),
        ('szExeFile', CHAR*MAX_PATH)
    ]


# typedef struct tagTHREADENTRY32 {
#    DWORD dwSize
#    DWORD cntUsage
#    DWORD th32ThreadID
#    DWORD th32OwnerProcessID
#    LONG  tpBasePri
#    LONG  tpDeltaPri
#    DWORD dwFlags
# } THREADENTRY32

class THREADENTRY32(ctypes.Structure):
    _fields_ = [
        ('dwSize', DWORD),
        ('cntUsage', DWORD),
        ('th32ThreadID', DWORD),
        ('th32OwnerProcessID', DWORD),
        ('tpBasePri', LONG),
        ('tpDeltaPri', LONG),
        ('dwFlags', DWORD)
    ]

# BOOL SetPriorityClass(
#  [ in ] HANDLE hProcess,
#  [ in ] DWORD  dwPriorityClass
# );


def set_process_priority(hProcess: HANDLE, dwPriorityClass: DWORD) -> BOOL:
    return KERNEL32.SetPriorityClass(hProcess, dwPriorityClass)


# BOOL SetThreadPriority(
#  [ in ] HANDLE hThread,
#  [ in ] int    nPriority
# );
def set_thread_priority(hThread: HANDLE, nPriority: INT) -> BOOL:
    return KERNEL32.SetThreadPriority(hThread, nPriority)


# DWORD GetPriorityClass(
#  [ in ] HANDLE hProcess
# );
def get_process_priority(hProcess: HANDLE) -> DWORD:
    return KERNEL32.GetPriorityClass(hProcess)


# int GetThreadPriority(
#  [ in ] HANDLE hThread
# );
def get_thread_priority(hThread: HANDLE) -> INT:
    return KERNEL32.GetThreadPriority(hThread)


# HANDLE OpenProcess(
#  [ in ] DWORD dwDesiredAccess,
#  [ in ] BOOL  bInheritHandle,
#  [ in ] DWORD dwProcessId
# );
def open_process(dwDesiredAccess: DWORD, bInheritHandle: BOOL, dwProcessId: DWORD) -> HANDLE:
    return KERNEL32.OpenProcess(dwDesiredAccess, bInheritHandle, dwProcessId)


# HANDLE OpenThread(
#  [ in ] DWORD dwDesiredAccess,
#  [ in ] BOOL  bInheritHandle,
#  [ in ] DWORD dwThreadId
# );
def open_thread(dwDesiredAccess: DWORD, bInheritHandle: BOOL, dwThreadId: DWORD) -> HANDLE:
    return KERNEL32.OpenThread(dwDesiredAccess, bInheritHandle, dwThreadId)


# DWORD ResumeThread(
#  [ in ] HANDLE hThread
# );
def resume_thread(hThread: HANDLE) -> DWORD:
    return KERNEL32.ResumeThread(hThread)


# DWORD SuspendThread(
#  [ in ] HANDLE hThread
# );
def suspend_thread(hThread: HANDLE) -> DWORD:
    return KERNEL32.SuspendThread(hThread)


# DWORD Wow64SuspendThread(
#    HANDLE hThread
# );
def wow64_suspend_thread(hThread: HANDLE) -> DWORD:
    return KERNEL32.Wow64SuspendThread(hThread)


# BOOL GetExitCodeThread(
#  [ in ]  HANDLE  hThread,
#  [ out ] LPDWORD lpExitCode
# );
def get_exit_code_thread(hThread: HANDLE, lpExitCode: LPDWORD) -> BOOL:
    return KERNEL32.GetExitCodeThread(hThread)


# BOOL GetExitCodeProcess(
#  [ in ]  HANDLE  hProcess,
#  [ out ] LPDWORD lpExitCode
# );
def get_exit_code_process(hProcess: HANDLE, lpExitCode: LPDWORD) -> BOOL:
    return KERNEL32.GetExitCodeProcess(hProcess)


# BOOL TerminateThread(
#  [ in , out ] HANDLE hThread,
#  [ in ]      DWORD  dwExitCode
# );
def terminate_thread(hThread: HANDLE, dwExitCode: DWORD) -> BOOL:
    return KERNEL32.TerminateThread(hThread, dwExitCode)


# BOOL TerminateProcess(
#  [ in ] HANDLE hProcess,
#  [ in ] UINT   uExitCode
# );
def terminate_process(hProcess: HANDLE, uExitCode: UINT) -> BOOL:
    return KERNEL32.TerminateProcess(hProcess, uExitCode)


# Call undocumented functions from NTDLL

# DWORD SuspendProcess(
#  [ in ] HANDLE hThread
# );
def suspend_process(hProcess: HANDLE):
    return NT.NtSuspendProcess(hProcess)


# DWORD NTResumeProcess(
#  [ in ] HANDLE hThread
# );
def resume_process(hProcess: HANDLE):
    return NT.NtResumeProcess(hProcess)
