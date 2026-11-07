import sys, timeit, tracemalloc, ctypes
import ctypes.wintypes as wt

sys.path.insert(0, "src")
import calculations as calc
from models import FlightInputs
from status import assess_status

i = FlightInputs(1200, 200, 250, 500, 80, 100, 200)


def full_calculation():
    calc.total_endurance_h(i); calc.endurance_to_threshold_h(i)
    calc.range_preserving_threshold_km(i); calc.time_to_endpoint_h(i)
    calc.fuel_required_kg(i); calc.endpoint_fuel_kg(i); calc.margin_kg(i)
    calc.fuel_use_difference_kg(i); assess_status(i)


n = 100_000
t = timeit.timeit(full_calculation, number=n)
print(f"Calculations + status: {t / n * 1e6:.2f} microseconds per run (n={n})")

tracemalloc.start()
full_calculation()
current, peak = tracemalloc.get_traced_memory()
print(f"Python-allocated memory during one calculation: peak {peak / 1024:.1f} KB")


class PMC(ctypes.Structure):
    _fields_ = [("cb", wt.DWORD), ("PageFaultCount", wt.DWORD),
                ("PeakWorkingSetSize", ctypes.c_size_t), ("WorkingSetSize", ctypes.c_size_t),
                ("QuotaPeakPagedPoolUsage", ctypes.c_size_t), ("QuotaPagedPoolUsage", ctypes.c_size_t),
                ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t), ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
                ("PagefileUsage", ctypes.c_size_t), ("PeakPagefileUsage", ctypes.c_size_t)]


k32, psapi = ctypes.windll.kernel32, ctypes.windll.psapi
k32.GetCurrentProcess.restype = wt.HANDLE
psapi.GetProcessMemoryInfo.argtypes = [wt.HANDLE, ctypes.POINTER(PMC), wt.DWORD]
pmc = PMC()
pmc.cb = ctypes.sizeof(PMC)
psapi.GetProcessMemoryInfo(k32.GetCurrentProcess(), ctypes.byref(pmc), pmc.cb)
print(f"Whole-process peak memory (incl. interpreter): {pmc.PeakWorkingSetSize / 1024 / 1024:.1f} MB")