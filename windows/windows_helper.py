# https://learn.microsoft.com/en-us/windows/win32/winprog/windows-data-types
# https://learn.microsoft.com/en-us/windows/win32/api/tlhelp32/ns-tlhelp32-processentry32
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

PAGE_READWRITE = 0x04
PROCESS_ALL_ACCESS = (0x00F0000 | 0x00100000 | 0xFFF)
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
