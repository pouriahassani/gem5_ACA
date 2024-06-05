#include <stdio.h>

 int amul(int rs1, int rs2)
 {
     int rd = 0;
     asm __volatile__ (
        ".word 0x40B50577\n"  // Custom instruction (add16)
        "mv %0, a0\n"     // Move the result from a0 to rd
        : "=r" (rd)
        : "r" (rs1), "r" (rs2)
        : "x10", "x11", "a0"
    );
      return rd;
 }

void main()
{
   
    int result;
    for (int n = 0; n < 10; n++)
    {
        /* Used new approximate unsigned integer multiplier instruction to multiply n and n+1 for n from 0 to 10 */
        result = amul(n,n+1);
        printf("\n%d * %d = %d",n,n+1,result);
    }
}
