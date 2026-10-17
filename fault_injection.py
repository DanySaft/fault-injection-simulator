from unicorn import Uc, UC_ARCH_RISCV, UC_MODE_RISCV32, UC_HOOK_CODE
from unicorn.riscv_const import UC_RISCV_REG_A0, UC_RISCV_REG_SP, UC_RISCV_REG_RA, UC_RISCV_REG_PC

# Configuration of the virtual memory
BASE_ADDR = 0x10000
MEM_SIZE  = 2 * 1024 * 1024
STACK_ADDR = BASE_ADDR + 0x100000

# Reading binary file
with open("target.bin", "rb") as f:
    code = f.read()

STOP_ADDR = BASE_ADDR + len(code)

# PHASE 1 : Recording the safe execution frame
trace = []

def record_frame(uc, pc_address, instruction_size, user_data):
    trace.append((pc_address, instruction_size))

mu_trace = Uc(UC_ARCH_RISCV, UC_MODE_RISCV32)
mu_trace.mem_map(BASE_ADDR, MEM_SIZE)
mu_trace.mem_write(BASE_ADDR, code)

# False data (0x0000) / stack / return addr
mu_trace.reg_write(UC_RISCV_REG_A0, 0x0000)
mu_trace.reg_write(UC_RISCV_REG_SP, STACK_ADDR)
mu_trace.reg_write(UC_RISCV_REG_RA, STOP_ADDR)

# To add the hook each instruction
mu_trace.hook_add(UC_HOOK_CODE, record_frame)
mu_trace.emu_start(BASE_ADDR, STOP_ADDR)

print(f"Safe frame recorded : {len(trace)} instructions executed.\n")

# PHASE 2 : Shooting (Instruction Skip)
print("Starting Fault Injection (Instruction Skip)...")
print("-" * 65)

def inject_instruction_skip(target_addr, instr_size):
    mu = Uc(UC_ARCH_RISCV, UC_MODE_RISCV32)
    mu.mem_map(BASE_ADDR, MEM_SIZE)
    mu.mem_write(BASE_ADDR, code)
    mu.reg_write(UC_RISCV_REG_A0, 0x0000)
    mu.reg_write(UC_RISCV_REG_SP, STACK_ADDR)
    mu.reg_write(UC_RISCV_REG_RA, STOP_ADDR)

    applied_fault = False

    def hook_glitch(uc, address, size, user_data):
        nonlocal applied_fault
        # If the CPU is on the target instruction
        if address == target_addr and not applied_fault:
            # Jump the instruction (PC incrementation)
            uc.reg_write(UC_RISCV_REG_PC, address + size)
            applied_fault = True

    mu.hook_add(UC_HOOK_CODE, hook_glitch)

    try:
        mu.emu_start(BASE_ADDR, STOP_ADDR)
        ret = mu.reg_read(UC_RISCV_REG_A0)
        if ret == 1:
            return "[BYPASS]"
        return "[NORMAL]"
    except Exception as e:
        return f"[-] Error crash ({type(e).__name__})"

# Loop on each instruction
for index, (target_addr, instr_size) in enumerate(trace):
    state = tester_tir(target_addr, instr_size)
    print(f"Shot #{index:02d} | Addr: 0x{target_addr:x} ({instr_size} bytes) -> {state}")
