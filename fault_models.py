from unicorn import UC_HOOK_CODE
from unicorn.riscv_const import UC_RISCV_REG_PC, UC_RISCV_REG_A0
import config
from target_loader import create_clean_cpu

# Simulation hardware glitch (instruction skip)
def inject_instruction_skip(target_addr, instr_size, code, stop_addr):
    # New CPU
    mu = create_clean_cpu(code, stop_addr)
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
        mu.emu_start(config.BASE_ADDR, stop_addr)
        ret = mu.reg_read(UC_RISCV_REG_A0)
        if ret == 1:
            return "[BYPASS]"
        return "[NORMAL]"
    except Exception as e:
        return f"[-] Error crash ({type(e).__name__})"