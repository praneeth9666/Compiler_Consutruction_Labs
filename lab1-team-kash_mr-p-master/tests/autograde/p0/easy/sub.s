
.globl main
main:
    pushl %ebp        ## save caller’s base pointer
    movl %esp, %ebp   ## set our base pointer
    subl $16, %esp    ## allocate for local vars (replace 20 with the actual size needed)
    pushl %ebx        ## save callee saved registers
    pushl %esi
    pushl %edi
    movl $2, %ecx
    negl %ecx
    movl %ecx, -4(%ebp)
    movl $1, %ecx
    addl -4(%ebp), %ecx
    movl %ecx, -8(%ebp)
    pushl -8(%ebp)
    call print_int_nl
    addl $4, %esp

    popl %edi        ## restore callee saved registers
    popl %esi
    popl %ebx
    movl $0, %eax    ## set return value
    movl %ebp, %esp  ## restore esp
    popl %ebp        ## restore ebp (alt. “leave”)
    ret              ## jump execution to call site
