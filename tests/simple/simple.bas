1 print chr$(147)
2 poke 53269,255
3 for c = 0 to 15
4 poke 646,c
5 print "testing 123..."
6 next
7 for n = 0 to 62 : poke 12288 + n, 255 : next n
8 for i = 0 to 7
10 v = 53248+i*2
40 poke 2040+i, 192
70 poke v, 100+i*10 : poke v + 1, 100+i*10
80 next
90 goto 90
