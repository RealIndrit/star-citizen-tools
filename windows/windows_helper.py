# https://learn.microsoft.com/en-us/windows/win32/winprog/windows-data-types
# https://learn.microsoft.com/en-us/windows/win32/api/tlhelp32/ns-tlhelp32-processentry32
# https://learn.microsoft.com/en-us/windows/win32/api/tlhelp32/ns-tlhelp32-threadentry32
# https://docs.python.org/3/library/ctypes.html

import ctypes
from ctypes.wintypes import *

KB = 1024
KERNEL32 = ctypes.windll.kernel32
INVALID_HANDLE_VALUE = -1

TH32CS_INHERIT = 0x80000000
TH32CS_SNAPHEAPLIST = 0x00000001
TH32CS_SNAPMODULE = 0x00000008
TH32CS_SNAPMODULE32 = 0x00000010
TH32CS_SNAPPROCESS = 0x00000002
TH32CS_SNAPTHREAD = 0x00000004
TH32CS_SNAPALL = (TH32CS_SNAPHEAPLIST | TH32CS_SNAPMODULE |
                  TH32CS_SNAPPROCESS | TH32CS_SNAPTHREAD)

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

STANDARD_RIGHTS_REQUIRED = 0x000F0000
DELETE = 0x00010000
READ_CONTROL = 0x00020000
SYNCHRONIZE = 0x00100000
WRITE_DAC = 0x00040000
WRITE_OWNER = 0x00080000

PAGE_READWRITE = 0x04
# I have no idea what the 0xFFFF Flag is for, but its in the docs XD
PROCESS_ALL_ACCESS = (STANDARD_RIGHTS_REQUIRED | SYNCHRONIZE | 0xFFFF)
VIRTUAL_MEM = (0x1000 | 0x2000)

INT8 = ctypes.c_int8
UINT8 = ctypes.c_uint8
INT16 = ctypes.c_int16
UINT16 = ctypes.c_uint16
INT32 = ctypes.c_int32
UINT32 = ctypes.c_uint32
INT = INT32
UINT = UINT32
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
