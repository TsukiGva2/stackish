import stackish_forth as sf

code = ": cat 1 2 3 ; : abc cat 2 3 ; : foo abc cat 3 4 ; foo foo : gol foo foo abc cat 3 2 ;"
s = sf.System()
print(s.do_string(code))

