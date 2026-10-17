
target/target.o:     file format elf32-littleriscv


Disassembly of section .text:

00000000 <verify_acces>:
   0:	fd010113          	addi	sp,sp,-48
   4:	02112623          	sw	ra,44(sp)
   8:	02812423          	sw	s0,40(sp)
   c:	03010413          	addi	s0,sp,48
  10:	fca42e23          	sw	a0,-36(s0)
  14:	000017b7          	lui	a5,0x1
  18:	33778793          	addi	a5,a5,823 # 1337 <.L2+0x12ff>
  1c:	fef42423          	sw	a5,-24(s0)
  20:	fe042623          	sw	zero,-20(s0)
  24:	fdc42703          	lw	a4,-36(s0)
  28:	fe842783          	lw	a5,-24(s0)
  2c:	00f71663          	bne	a4,a5,38 <.L2>
  30:	00100793          	li	a5,1
  34:	fef42623          	sw	a5,-20(s0)

00000038 <.L2>:
  38:	fec42783          	lw	a5,-20(s0)
  3c:	00078513          	mv	a0,a5
  40:	02c12083          	lw	ra,44(sp)
  44:	02812403          	lw	s0,40(sp)
  48:	03010113          	addi	sp,sp,48
  4c:	00008067          	ret
