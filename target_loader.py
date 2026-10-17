from unicorn import Uc, UC_ARCH_RISCV, UC_MODE_RISCV32
from unicorn.riscv_const import UC_RISCV_REG_A0, UC_RISCV_REG_SP, UC_RISCV_REG_RA
import config

# Reading binary file
def load_binary(filepath):
    with open(filepath, "rb") as f:
        return f.read()

# Generate virtual CPU (RISCV-32)
def create_clean_cpu(code, stop_addr):
    mu = Uc(UC_ARCH_RISCV, UC_MODE_RISCV32)
    mu.mem_map(config.BASE_ADDR, config.MEM_SIZE)
    mu.mem_write(config.BASE_ADDR, code)

   # Fake password (0x0000) / stack / return addr
    mu.reg_write(UC_RISCV_REG_A0, 0x0000)
    mu.reg_write(UC_RISCV_REG_SP, config.STACK_ADDR)
    mu.reg_write(UC_RISCV_REG_RA, stop_addr)

    return mu