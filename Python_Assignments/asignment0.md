Assignment
Douglas Hofstadter’s Pulitzer-prize-winning book Gödel, Escher, Bach contains many interesting mathematical puzzles, many of which can be expressed in the form of computer programs. In Chapter XII, Hofstadter mentions a wonderful problem:



Pick some positive integer and call it n.

If n is even, divide it by two.

If n is odd, multiply it by three and add one.

Continue this process until n is equal to one.

Enter a number: 15
15 is odd, so I make 3n + 1: 46 
46 is even, so I take half: 23
23 is odd, so I make 3n + 1: 70
70 is even, so I take half: 35 
35 is odd, so I make 3n + 1: 106 
106 is even, so I take half: 53 
53 is odd, so I make 3n + 1: 160 
160 is even, so I take half: 80
80 is even, so I take half: 40 
40 is even, so I take half: 20 
20 is even, so I take half: 10 
10 is even, so I take half: 5
5 is odd, so I make 3n + 1: 16 
16 is even, so I take half: 8 
8 is even, so I take half: 4
4 is even, so I take half: 2
2 is even, so I take half: 1

As you can see from this example, the numbers go up and down, but eventually—at least for all numbers that have ever been tried—comes down to end in 1. In some respects, this process is reminiscent of the formation of hailstones, which get carried upward by the winds over and over again before they finally descend to the ground. Because of this analogy, this sequence of numbers is usually called the Hailstone

sequence, although it goes by many other names as well.