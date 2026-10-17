from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UC_PROT_ALL
from unicorn.x86_const import UC_X86_REG_EBX, UC_X86_REG_ECX

# Opcode en hexadécimal : INC ecx; ADD ebx, ecx
X86_CODE = b"\x41\x01\xcb"

# Adresse de base où charger le code
ADDRESS = 0x1000000

# Initialiser l'émulateur en mode x86 32 bits
mu = Uc(UC_ARCH_X86, UC_MODE_32)

# Allouer une page de mémoire (2 Mo) avec permissions rwx
mu.mem_map(ADDRESS, 2 * 1024 * 1024, UC_PROT_ALL)

# Écrire le bytecode à l'adresse spécifiée
mu.mem_write(ADDRESS, X86_CODE)

# Définir l'état initial des registres
mu.reg_write(UC_X86_REG_ECX, 10)
mu.reg_write(UC_X86_REG_EBX, 20)

# Lancer l'émulation (début, fin)
mu.emu_start(ADDRESS, ADDRESS + len(X86_CODE))

# Lire les résultats
val_ecx = mu.reg_read(UC_X86_REG_ECX)
val_ebx = mu.reg_read(UC_X86_REG_EBX)

print(f"ECX = {val_ecx}")  # Attendu : 11
print(f"EBX = {val_ebx}")  # Attendu : 31
