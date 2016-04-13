from random import Random

R = Random()

digits = range(10)
number = range(10)

found = False
ntrials = 0
while not found:
    if not ntrials % 1000000: print ntrials, 'trials'
    found = True
    number = [ R.choice(digits) for i in digits ]
    for d in digits:
        if number.count(d) != number[d]:
            found = False
            break
    ntrials += 1

print number
