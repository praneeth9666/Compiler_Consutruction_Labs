
.globl main
main:
    pushl %ebp        ## save caller’s base pointer
    movl %esp, %ebp   ## set our base pointer
    subl $72, %esp    ## allocate for local vars (replace 20 with the actual size needed)
    pushl %ebx        ## save callee saved registers
    pushl %esi
    pushl %edi
    movl -12(%ebp), %ecx
    addl -8(%ebp), %ecx
    movl %ecx, -16(%ebp)
    movl -24(%ebp), %ecx
    addl -20(%ebp), %ecx
    movl %ecx, -28(%ebp)
    movl -36(%ebp), %ecx
    addl -32(%ebp), %ecx
    movl %ecx, -40(%ebp)
    movl -8(%ebp), %ecx
    addl -20(%ebp), %ecx
    movl %ecx, -48(%ebp)
    movl -48(%ebp), %ecx
    addl -32(%ebp), %ecx
    movl %ecx, -52(%ebp)
    movl -52(%ebp), %ecx
    addl -44(%ebp), %ecx
    movl %ecx, -56(%ebp)
    movl -56(%ebp), %ecx
    addl -60(%ebp), %ecx
    movl %ecx, -64(%ebp)
    pushl -64(%ebp)
    call print_int_nl
    addl $4, %esp

    popl %edi        ## restore callee saved registers
    popl %esi
    popl %ebx
    movl $0, %eax    ## set return value
    movl %ebp, %esp  ## restore esp
    popl %ebp        ## restore ebp (alt. “leave”)
    ret              ## jump execution to call site
