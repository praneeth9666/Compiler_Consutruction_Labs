
.globl main
main:
    pushl %ebp        ## save caller’s base pointer
    movl %esp, %ebp   ## set our base pointer
    subl $120, %esp    ## allocate for local vars (replace 20 with the actual size needed)
    pushl %ebx        ## save callee saved registers
    pushl %esi
    pushl %edi
    movl $1, %ecx
    addl -4(%ebp), %ecx
    movl %ecx, -8(%ebp)
    movl -12(%ebp), %ecx
    addl -12(%ebp), %ecx
    movl %ecx, -16(%ebp)
    movl -20(%ebp), %ecx
    addl -20(%ebp), %ecx
    movl %ecx, -24(%ebp)
    movl -28(%ebp), %ecx
    addl -28(%ebp), %ecx
    movl %ecx, -32(%ebp)
    movl -36(%ebp), %ecx
    addl -36(%ebp), %ecx
    movl %ecx, -40(%ebp)
    movl -44(%ebp), %ecx
    addl -44(%ebp), %ecx
    movl %ecx, -48(%ebp)
    movl -52(%ebp), %ecx
    addl -52(%ebp), %ecx
    movl %ecx, -56(%ebp)
    movl -60(%ebp), %ecx
    addl -60(%ebp), %ecx
    movl %ecx, -64(%ebp)
    movl -68(%ebp), %ecx
    addl -68(%ebp), %ecx
    movl %ecx, -72(%ebp)
    movl -12(%ebp), %ecx
    addl -20(%ebp), %ecx
    movl %ecx, -80(%ebp)
    movl -80(%ebp), %ecx
    addl -28(%ebp), %ecx
    movl %ecx, -84(%ebp)
    movl -84(%ebp), %ecx
    addl -36(%ebp), %ecx
    movl %ecx, -88(%ebp)
    movl -88(%ebp), %ecx
    addl -44(%ebp), %ecx
    movl %ecx, -92(%ebp)
    movl -92(%ebp), %ecx
    addl -52(%ebp), %ecx
    movl %ecx, -96(%ebp)
    movl -96(%ebp), %ecx
    addl -60(%ebp), %ecx
    movl %ecx, -100(%ebp)
    movl -100(%ebp), %ecx
    addl -68(%ebp), %ecx
    movl %ecx, -104(%ebp)
    movl -104(%ebp), %ecx
    addl -76(%ebp), %ecx
    movl %ecx, -108(%ebp)
    pushl -60(%ebp)
    call print_int_nl
    addl $4, %esp

    popl %edi        ## restore callee saved registers
    popl %esi
    popl %ebx
    movl $0, %eax    ## set return value
    movl %ebp, %esp  ## restore esp
    popl %ebp        ## restore ebp (alt. “leave”)
    ret              ## jump execution to call site
