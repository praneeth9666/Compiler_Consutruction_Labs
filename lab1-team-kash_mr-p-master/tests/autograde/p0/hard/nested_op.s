
.globl main
main:
    pushl %ebp        ## save caller’s base pointer
    movl %esp, %ebp   ## set our base pointer
    subl $48, %esp    ## allocate for local vars (replace 20 with the actual size needed)
    pushl %ebx        ## save callee saved registers
    pushl %esi
    pushl %edi
    movl $2, %ecx
    negl %ecx
    movl %ecx, -12(%ebp)
    movl -4(%ebp), %ecx
    addl -12(%ebp), %ecx
    movl %ecx, -16(%ebp)
    movl -8(%ebp), %ecx
    addl -16(%ebp), %ecx
    movl %ecx, -20(%ebp)
    movl -4(%ebp), %ecx
    negl %ecx
    movl %ecx, -24(%ebp)
    movl -20(%ebp), %ecx
    addl -24(%ebp), %ecx
    movl %ecx, -28(%ebp)
    movl -28(%ebp), %ecx
    negl %ecx
    movl %ecx, -32(%ebp)
    movl $2, %ecx
    addl -32(%ebp), %ecx
    movl %ecx, -36(%ebp)
    movl $3, %ecx
    addl -36(%ebp), %ecx
    movl %ecx, -40(%ebp)
    pushl -40(%ebp)
    call print_int_nl
    addl $4, %esp

    popl %edi        ## restore callee saved registers
    popl %esi
    popl %ebx
    movl $0, %eax    ## set return value
    movl %ebp, %esp  ## restore esp
    popl %ebp        ## restore ebp (alt. “leave”)
    ret              ## jump execution to call site
