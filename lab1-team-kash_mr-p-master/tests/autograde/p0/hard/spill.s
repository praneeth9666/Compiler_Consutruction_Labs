
.globl main
main:
    pushl %ebp        ## save caller’s base pointer
    movl %esp, %ebp   ## set our base pointer
    subl $56, %esp    ## allocate for local vars (replace 20 with the actual size needed)
    pushl %ebx        ## save callee saved registers
    pushl %esi
    pushl %edi
    movl $2, %ecx
    negl %ecx
    movl %ecx, -20(%ebp)
    movl -4(%ebp), %ecx
    addl -8(%ebp), %ecx
    movl %ecx, -32(%ebp)
    movl -32(%ebp), %ecx
    addl -12(%ebp), %ecx
    movl %ecx, -36(%ebp)
    movl -36(%ebp), %ecx
    addl -16(%ebp), %ecx
    movl %ecx, -40(%ebp)
    movl -40(%ebp), %ecx
    addl -24(%ebp), %ecx
    movl %ecx, -44(%ebp)
    movl -44(%ebp), %ecx
    addl -28(%ebp), %ecx
    movl %ecx, -48(%ebp)
    pushl -48(%ebp)
    call print_int_nl
    addl $4, %esp

    popl %edi        ## restore callee saved registers
    popl %esi
    popl %ebx
    movl $0, %eax    ## set return value
    movl %ebp, %esp  ## restore esp
    popl %ebp        ## restore ebp (alt. “leave”)
    ret              ## jump execution to call site
