
.globl main
main:
    pushl %ebp        ## save caller’s base pointer
    movl %esp, %ebp   ## set our base pointer
    subl $4, %esp    ## allocate for local vars (replace 20 with the actual size needed)
    pushl %ebx        ## save callee saved registers
    pushl %esi
    pushl %edi

    popl %edi        ## restore callee saved registers
    popl %esi
    popl %ebx
    movl $0, %eax    ## set return value
    movl %ebp, %esp  ## restore esp
    popl %ebp        ## restore ebp (alt. “leave”)
    ret              ## jump execution to call site
