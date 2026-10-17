"""
Automated Fault Injection Framework
Architecture : RISC-V 32-bit (Bare-metal simulation)
"""

from unicorn import UC_HOOK_CODE
import config
from target_loader import load_binary, create_clean_cpu
from fault_models import inject_instruction_skip

# Recording safe execution frame with bad password (addr instruction and size)
def get_safe_trace(code, stop_addr):
    trace = []
    
    def record_frame(uc, pc_address, instruction_size, user_data):
        trace.append((pc_address, instruction_size))

    mu_trace = create_clean_cpu(code, stop_addr)
    mu_trace.hook_add(UC_HOOK_CODE, record_frame)
    mu_trace.emu_start(config.BASE_ADDR, stop_addr)
    
    return trace

if __name__ == "__main__":
    print("--- Simulation Fault Injection ---")
    code = load_binary(config.TARGET_FILE)
    stop_addr = config.BASE_ADDR + len(code)

    # Phase 1
    trace = get_safe_trace(code, stop_addr)
    print(f"Safe frame recorded : {len(trace)} instructions executed.\n")
    print()

    # Phase 2
    print("Starting Fault Injection (Instruction Skip) :")
    
    for index, (target_addr, instr_size) in enumerate(trace):
        state = inject_instruction_skip(target_addr, instr_size, code, stop_addr)
        print(f"Shot #{index:02d} | Addr: 0x{target_addr:x} ({instr_size} bytes) -> {state}")