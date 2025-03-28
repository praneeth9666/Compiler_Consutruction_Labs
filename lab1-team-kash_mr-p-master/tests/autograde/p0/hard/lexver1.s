
.globl main
main:
    pushl %ebp        ## save caller’s base pointer
    movl %esp, %ebp   ## set our base pointer
    subl $36, %esp    ## allocate for local vars (replace 20 with the actual size needed)
    pushl %ebx        ## save callee saved registers
    pushl %esi
    pushl %edi
    movl $6, %ecx
    negl %ecx
    movl %ecx, -8(%ebp)
    movl -4(%ebp), %ecx
    addl -12(%ebp), %ecx
    movl %ecx, -20(%ebp)
    movl -20(%ebp), %ecx
    addl -16(%ebp), %ecx
    movl %ecx, -24(%ebp)
    pushl -24(%ebp)
    call print_int_nl
    addl $4, %esp
    movl -12(%ebp), %ecx
    addl -16(%ebp), %ecx
    movl %ecx, -28(%ebp)
    pushl -28(%ebp)
    call print_int_nl
    addl $4, %esp

    popl %edi        ## restore callee saved registers
    popl %esi
    popl %ebx
    movl $0, %eax    ## set return value
    movl %ebp, %esp  ## restore esp
    popl %ebp        ## restore ebp (alt. “leave”)
    ret              ## jump execution to call site
