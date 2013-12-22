import string

x = 'negativeList1.txt'
y = 'negativeList2.txt'

z = 'nList.txt'

a = open(x,'r')
b = open(y,'r')

c = open(z,'w')


alist = a.readlines()
blist = b.readlines()

for word in alist:
    if word not in blist:
        blist.append(word)

for word in blist:
    c.write(word)

a.close()
b.close()
c.close()

print "Done! :3"
    
