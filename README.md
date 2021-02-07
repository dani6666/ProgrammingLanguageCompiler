# ProgrammingLanguageCompiler

The app is a compiler developed as a project for studies. It compiles given simple imperative language and returns a sequence of instructions for a given virtual machine. This version was the second fastest compiler (in terms of time needed to run generated code) out of 90 compilers on the whole year.

Requirements:  
* Python 3.8.5
* SLY 0.4  

To run compiler:  
`python compiler.py input.txt output.txt`

## Language  

Laguage operates only on natural numbers.  
  
Declaration `tab(10:100)` creates a table of 91 elements with indexes from 10 do 100 inclusive.  
  
Number of iterations of `FOR` loop is determined at the begining of the loop and remains the same even when variables given as start and the end of the loop are changed inside the loop. The iterator can't be changed inside the loop.  
  
`REPEAT-UNTIL` loop always executes at least once.  
  
Comments must be placed in square brackets e.g. `[comment]`  

### Language grammar
<pre>
program     -> DECLARE declarations BEGIN commands END  
            |  BEGIN commands END  
  
declarations-> declarations , pidentifier  
            |  declarations , pidentifier (num :num )  
            |  pidentifier  
            |  pidentifier (num :num )  
  
commands    -> commands command  
            |  command  
  
command     -> identifier := expression ;  
            |  IF condition THEN commands ELSE commands ENDIF  
            |  IF condition THEN commands ENDIF  
            |  WHILE condition DO commands ENDWHILE  
            |  REPEAT commands UNTIL condition ;  
            |  FOR pidentifier FROM value TO value DO commands ENDFOR  
            |  FOR pidentifier FROM value DOWNTO value DO commands ENDFOR  
            |  READ identifier ;  
            |  WRITE value ;  
  
expression  -> value  
            |  value + value  
            |  value - value  
            |  value * value  
            |  value / value  
            |  value % value  
  
condition   -> value = value  
            |  value != value  
            |  value < value  
            |  value > value  
            |  value <= value  
            |  value >= value  
  
value       -> num  
            |  identifier  
  
identifier  -> pidentifier  
            |  pidentifier ( pidentifier )  
            |  pidentifier (num )  
</pre>

## Virtual machine
Virtual machine operates on 6 registers (r<sub>a</sub>, r<sub>b</sub>, r<sub>c</sub>, r<sub>d</sub>, r<sub>e</sub>, r<sub>f</sub>) and sequence of memory cells (p<sub>1</sub>, p<sub>2</sub>,...).  
It executes the `k`-th command starting from 0 until it reaches command `HALT`.  

## Table of virtual machine commands

| Command   | Interpretation                                                        | Time needed  |
| --------- | --------------------------------------------------------------------- | - |
|`GET x`    | Stores given number in p<sub>r<sub>x</sub></sub><br>k ← k + 1         |100|
|`PUT x`    | Displays the value stored in p<sub>r<sub>x</sub></sub> <br> k ← k + 1        |100|
|`LOAD x y` | r<sub>x</sub> ← p<sub>r<sub>y</sub></sub> <br> k ← k + 1              |20 |
|`STORE x y`| p<sub>r<sub>y</sub></sub> ← r<sub>x</sub> <br> k ← k + 1              |20 |
|`ADD x y`  | r<sub>x</sub> ← r<sub>x</sub> + r<sub>y</sub> <br> k ← k + 1          |5  |
|`SUB x y`  | r<sub>x</sub> ← max(r<sub>x</sub> − r<sub>y</sub>, 0) <br> k ← k + 1  |5  |
|`RESET x`  | r<sub>x</sub> ← 0 <br> k ← k + 1                                      |1  |
|`INC x`    | r<sub>x</sub> ← r<sub>x</sub> + 1 <br> k ← k + 1                      |1  |
|`DEC x`    | r<sub>x</sub> ← max(r<sub>x</sub> − 1, 0) <br> k ← k + 1              |1  |
|`SHR x`    | r<sub>x</sub> ← r<sub>x</sub> / 2 <br> k ← k + 1                      |1  |
|`SHL x`    | r<sub>x</sub> ← r<sub>x</sub> * 2 <br> k ← k + 1                      |1  |
|`JUMP j`   | k ← k + j                                                             |1  |
|`JZERO x j`| if r<sub>x</sub> = 0<br> then k ← k + j<br>else k ← k + 1             |1  |
|`JODD x j` | if r<sub>x</sub> is odd <br> then k ← k + j<br> else k ← k + 1        |1  |
|`HALT`     | Stop program                                                          |0  |

