while True:
    n = input("enter height: ")
    #main logic

    try:
        n = int(n)
        if 1 <= n <= 8:
            break
        else:
          print("Height must be between 1 and 8.")

    except ValueError:
        # Rejects non-numeric input like "foo"
          print("Invalid Input. Please enter a whole number.")


for i in range(n):

  #calculates the amount of hashes the code generates
  hashes = i + 1

  #calculates the amount of spaces the code generates

  spaces = n - hashes

  #prints out all the functions needed to form the pyramid on the terminal
  print((" " * spaces) + ("#" * hashes) + (" " * 2) + ("#" * hashes))

"""
check50
cs50/problems/2025/x/sentimental/mario/more

:) mario.py exists.
Log
checking that mario.py exists...

:) rejects a height of -1
Log
running python3 mario.py...
sending input -1...
checking that input was rejected...

:) rejects a height of 0
Log
running python3 mario.py...
sending input 0...
checking that input was rejected...

:) handles a height of 1 correctly
Log
running python3 mario.py...
sending input 1...

:) handles a height of 2 correctly
Log
running python3 mario.py...
sending input 2...

:) handles a height of 8 correctly
Log
running python3 mario.py...
sending input 8...

:) rejects a height of 9, and then accepts a height of 2
Log
running python3 mario.py...
sending input 9...
checking that input was rejected...
sending input 2...
checking for output " # #\n## ##\n"...
checking that program exited with status 0...

:) rejects a non-numeric height of "foo"
Log
running python3 mario.py...
sending input foo...
checking that input was rejected...

:) rejects a non-numeric height of ""
Log
running python3 mario.py...
sending input ...
checking that input was rejected...
"""
