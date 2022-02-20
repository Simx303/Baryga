import random

def response():
    type = input("as> ")
    read = False
    resp =[]
    for l in open(".//responses"):
        if l.startswith('#') or l[0].strip() == '':
            continue
        elif l.startswith('$'+type):
            read = True
            continue
        elif l.startswith('$'):
            read=False
        else:
            if read:
                resp.append(l.replace("\\n","\n"))
    print(resp)
    response()
response()