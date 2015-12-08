#!/usr/bin/env python3

from subprocess import check_output
import json, re, os.path, time

cache_filename = 'up-output.cache'

def yes_or_no(question):
    reply = str(input(question+' (y/n): ')).lower().strip()
    
    if len(reply) > 0 and reply[0] == 'y':
        return True
    if len(reply) > 0 and reply[0] == 'n':
        return False
    else:
        return yes_or_no("Please enter ")

# check for cached result
ask_to_query = False
if os.path.isfile(cache_filename):
    print("Found a cache file which is %d minutes old." % (int(time.time() - os.path.getmtime(cache_filename)) / 60))
    if yes_or_no("Do you want to use cached results?"):
        f = open(cache_filename, 'r')
        o = f.read()
    else:
        ask_to_query = True
else:
    ask_to_query = True

if ask_to_query:
    if yes_or_no("Cost: 250 sat. Would you like to query Up for available endpoints?"):
        o = check_output(["21", "buy", "--maxprice", "250", "url", "http://10.244.34.100:21411/up"], universal_newlines=True)
        f = open(cache_filename, 'w')
        f.write(o)
    else:
        print("No data available. Good-bye. :)")
        exit()

o = re.sub(r'You spent: .*$','', o)
data = json.loads(o)

again = True
while again:
    print("\n" + 60 * '-')
    print("   Up Browser - Browse live endpoints on the 21 network")
    print(60 * '-')
    count = 1
    choices = []
    for endpoint in data:
        if count > 20:
            continue
        print( "%d. %s - %s" % (count,endpoint['name'],endpoint['url']))
        count += 1
        choices.append(endpoint['url'])
    print(60 * '-')

    choice = -1
    while choice is None or choice < 1 or choice > len(choices):
        choice = input('Enter your choice [1-%s, q to quit] : ' % str(len(choices)) )
        if len(choice) == 0 or 'q' in choice.lower():
            print("\nGood-bye. :)")
            exit()    
        choice = int(choice)
      
    url = choices[choice-1]  
    #print("You chose %d. Going to visit %s" % (choice, url)

    print(check_output(["curl", url], universal_newlines=True))

    again = yes_or_no("Would you like to visit another?")

