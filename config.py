"""
Global hardware configuration for the emulator.
"""

BASE_ADDR = 0x10000
MEM_SIZE  = 2 * 1024 * 1024
STACK_ADDR = BASE_ADDR + 0x100000

# Updated path to point to the new target folder
TARGET_FILE = "target/target.bin"