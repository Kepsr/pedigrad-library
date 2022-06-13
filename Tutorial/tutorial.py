import sys
sys.path.insert(0, '../')

from Pedigrad import (
  PreOrder, SegmentObject, MorphismOfSegments,
  CategoryOfSegments, PointedSet, Environment,
  Sequence, Table
)


Omega = PreOrder.from_file("omega.yml")
print(Omega.relations)
print(Omega.mask)
print(Omega.cartesian)
Omega.closure()
print("--after:")
print(Omega.relations)
print("--relation:")
print(Omega.geq('1', '2'))
print(Omega.geq('2', '1'))
print(Omega.geq('4', '3'))
print(Omega.geq('?', '3'))
print(Omega.geq('?', '?'))
print("--infimum:")
print(Omega.inf('2', '3'))
print(Omega.inf('1', '2'))
print(Omega.inf('?', '3'))
print("--presence test:")
print('3' in Omega)
print('1' in Omega)
print('?' in Omega)

print("\n------------------------\n")

t = []
c = []
for i in range(20):
  t.append((i, i))
  c.append('?' if i % 15 == 11 else str((i % 2) + 1))

s = SegmentObject(20, t, c)
sys.stdout.write("s = ")
s.display()
print(f"colors = {s.colors}")

s1 = s.merge([(0, 3, 9), (10, 2, 14), (15, 3, 19)], Omega.inf)
sys.stdout.write("s1 = ")
s1.display()
print(f"topology = {s1.topology}")
print(f"colors = {s1.colors}")

s2 = s.merge([(0, 3, 9), (10, 2, 14)],Omega.inf)
sys.stdout.write("s2 = ")
s2.display()

s2 = s2.remove([5, 23])
sys.stdout.write("s2 = ")
s2.display()

s2.domain += 4
sys.stdout.write("s2 = ")
s2.display()
print(f"colors = {s2.colors}")

s3 = s.merge([(0, 3, 9), (10, 2, 14)], Omega.inf)
sys.stdout.write("s3 = ")
s3.display()
s3 = s3.remove([1, 5, 6, 8, 10])
sys.stdout.write("s3 = ")
s3.display()
s3.topology = s3.topology + [(24, 24)]
s3.colors = s3.colors + ['5']

s3.domain = s3.domain+5
sys.stdout.write("s3 = ")
s3.display()
print(f"colors= {s3.colors}")

m = MorphismOfSegments(s2, s3, 'id', Omega.geq)
print(m.defined)
sys.stdout.write("s = ")
m.source.display()
sys.stdout.write("t = ")
m.target.display()
print(f"f0 = {m.f0}")

print("\n------------------------\n")

Seg = CategoryOfSegments(Omega)

s = Seg.initial(18, '1')
s = s.merge([(2, 2, 8)], Omega.inf)

print(Seg.identity(s, s))

t = Seg.initial(20, '1')
t = t.merge([(2, 3, 10), (15, 2, 18)], Omega.inf)

print(Seg.identity(s, t))

sys.stdout.write("s = ")
s.display()
sys.stdout.write("t = ")
t.display()

h = Seg.homset(s, t)
for i, item in h:
  print(f"{i}) well-defined = {item.defined}")
  print(f"f1 = {item.f1}")
  print(f"f0 = {item.f0}")

print("\n------------------------\n")

E = PointedSet(list('-ACGT'), 0)

Env = Environment(Seg, E, 5, ['4'] * 5) #[] = white nodes
print(Env.Seg.preorder.relations)
print(Env.pset.symbols)
print(Env.pset.point())
print(Env.spec)
print(Env.b)

s4 = Env.segment(list('ACGTTPCA-CT'), '1')
s4.display()

print("\n------------------------\n")

Seqali = Env.seqali("align.fa")

print("\nDatabase\n" )

print(Seqali.indiv)
for i, item in enumerate(Seqali.base):
  print(f"{i}) color: {item.colors[item.parse]}")
  item.display()
  for x in Seqali.database[i]:
    for y in x:
      print(y)
    print("")

print("\nImage\n" )
for i, item in enumerate(Seqali.base):
  print(f"base[{i}]")
  item.display()
  sal = Seqali.eval(item)
  for x in sal:
    for y in x:
      print(y)
    print("")

print("\nExtending category\n" )
l = Seqali.extending_category(Seqali.base[0])
for i, m in l:
  print(i)
  print(m.f1)
  print(m.f0)

print("\nExtending category\n" )
l = Seqali.extending_category(Seqali.base[1])
for i, m in l:
  print(i)
  print(m.f1)
  print(m.f0)

print("\n------------------------\n")

a = list('AGCTAGCTGA')
b = list('GTGGATCGATGA')

A = Sequence('a', a, '1')
B = Sequence('b', b, '1')

table = Table(A, B)
print("\nincidence")
table.incidence()
table.stdout()
print("\nfillout")
table.fillout()
table.stdout()
table.write("dprog.fa", mode = 'w', debug = False, display = True)

print("\n------------------------\n")

E = PointedSet(list('-ACGT'), 0)

Env = Environment(Seg, E, 2, ['1'] * 2) #[] = white nodes
Seqali = Env.seqali("dprog.fa")

print("\nImage\n" )

print(Seqali.indiv)
Seqali.base[0].display()
sal = Seqali.eval(Seqali.base[0])
for x in sal:
  for y in x:
    print(y)
  print("")
