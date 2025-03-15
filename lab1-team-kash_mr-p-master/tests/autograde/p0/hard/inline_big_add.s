
.globl main
main:
    pushl %ebp        ## save caller’s base pointer
    movl %esp, %ebp   ## set our base pointer
    subl $40, %esp    ## allocate for local vars (replace 20 with the actual size needed)
    pushl %ebx        ## save callee saved registers
    pushl %esi
    pushl %edi
    movl -4(%ebp), %ecx
    addl -4(%ebp), %ecx
    movl %ecx, -8(%ebp)
    movl -8(%ebp), %ecx
    addl -4(%ebp), %ecx
    movl %ecx, -12(%ebp)
    movl -12(%ebp), %ecx
    addl -4(%ebp), %ecx
    movl %ecx, -16(%ebp)
    movl -16(%ebp), %ecx
    addl -4(%ebp), %ecx
    movl %ecx, -20(%ebp)
    movl -20(%ebp), %ecx
    addl -4(%ebp), %ecx
    movl %ecx, -24(%ebp)
    movl -24(%ebp), %ecx
    addl -4(%ebp), %ecx
    movl %ecx, -28(%ebp)
    movl -28(%ebp), %ecx
    addl -4(%ebp), %ecx
    movl %ecx, -32(%ebp)
    pushl -32(%ebp)
    call print_int_nl
    addl $4, %esp

    popl %edi        ## restore callee saved registers
    popl %esi
    popl %ebx
    movl $0, %eax    ## set return value
    movl %ebp, %esp  ## restore esp
    popl %ebp        ## restore ebp (alt. “leave”)
    ret              ## jump execution to call site
