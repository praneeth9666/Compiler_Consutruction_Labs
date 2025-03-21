
.globl main
main:
    pushl %ebp        ## save caller’s base pointer
    movl %esp, %ebp   ## set our base pointer
    subl $60, %esp    ## allocate for local vars (replace 20 with the actual size needed)
    pushl %ebx        ## save callee saved registers
    pushl %esi
    pushl %edi
    movl -4(%ebp), %ecx
    addl   $1, %ecx
    movl %ecx, -8(%ebp)
    movl -8(%ebp), %ecx
    addl   $2, %ecx
    movl %ecx, -12(%ebp)
    movl -12(%ebp), %ecx
    addl   $3, %ecx
    movl %ecx, -16(%ebp)
    movl -16(%ebp), %ecx
    addl   $4, %ecx
    movl %ecx, -20(%ebp)
    movl -20(%ebp), %ecx
    addl   $5, %ecx
    movl %ecx, -24(%ebp)
    movl -24(%ebp), %ecx
    addl   $6, %ecx
    movl %ecx, -28(%ebp)
    movl -28(%ebp), %ecx
    addl   $7, %ecx
    movl %ecx, -32(%ebp)
    movl -32(%ebp), %ecx
    addl   $8, %ecx
    movl %ecx, -36(%ebp)
    movl -36(%ebp), %ecx
    addl   $9, %ecx
    movl %ecx, -40(%ebp)
    movl -40(%ebp), %ecx
    addl   $10, %ecx
    movl %ecx, -44(%ebp)
    movl -44(%ebp), %ecx
    addl   $11, %ecx
    movl %ecx, -48(%ebp)
    movl -48(%ebp), %ecx
    addl   $12, %ecx
    movl %ecx, -52(%ebp)
    pushl -52(%ebp)
    call print_int_nl
    addl $4, %esp

    popl %edi        ## restore callee saved registers
    popl %esi
    popl %ebx
    movl $0, %eax    ## set return value
    movl %ebp, %esp  ## restore esp
    popl %ebp        ## restore ebp (alt. “leave”)
    ret              ## jump execution to call site
