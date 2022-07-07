import sys
sys.path.insert(0, '../')

from Pedigrad import (
  Proset, SegmentObject, MorphismOfSegments,
  CategoryOfSegments, PointedSet, Environment,
  Sequence, Table
)

def print_with_margin(x: str):
  print()
  print(x)
  print()


Omega = Proset.from_file("omega.yml")
print(Omega.relations)
print(Omega.mask)
Omega.close()
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

print_with_margin('-' * 24)

domain = 20
t = []
c = []
for i in range(domain):
  t.append((i, i))
  c.append('?' if i % 15 == 11 else str((i % 2) + 1))

s = SegmentObject(domain, t, c)
print(f"{s = }")
print(f"{s.colors = }")

s1 = s.merge([(0, 3, 9), (10, 2, 14), (15, 3, 19)], Omega.inf)
print(f"{s1 = }")
print(f"{s1.topology = }")
print(f"{s1.colors = }")

s2 = s.merge([(0, 3, 9), (10, 2, 14)], Omega.inf)
print(f"{s2 = }")

s2 = s2.remove([5, 23])
print(f"{s2 = }")

s2.domain += 4
print(f"{s2 = }")
print(f"{s2.colors = }")

s3 = s.merge([(0, 3, 9), (10, 2, 14)], Omega.inf)
print(f"{s3 = }")
s3 = s3.remove([1, 5, 6, 8, 10])
print(f"{s3 = }")
s3.topology.append((24, 24))
s3.colors.append(5)

s3.domain += 5
print(f"{s3 = }")
print(f"{s3.colors = }")

m = MorphismOfSegments(s2, s3, list(range(s2.domain)), Omega.geq)
print(m.defined)
print(f"{m.source = }")
print(f"{m.target = }")
print(f"{m.f0 = }")

print_with_margin('-' * 24)

Seg = CategoryOfSegments(Omega)

s = Seg.initial(18, '1')
s = s.merge([(2, 2, 8)], Omega.inf)

print(Seg.identity(s, s))

t = Seg.initial(20, '1')
t = t.merge([(2, 3, 10), (15, 2, 18)], Omega.inf)

print(Seg.identity(s, t))

print(f"{s = }")
print(f"{t = }")

h = Seg.homset(s, t)
for i, item in enumerate(h):
  print(f"{i}) well-defined = {item.defined}")
  print(f"f1 = {item.f1}")
  print(f"f0 = {item.f0}")

print_with_margin('-' * 24)

E = PointedSet(list('-ACGT'), 0)

Env = Environment(Seg, E, 5, ['4'] * 5) #[] = white nodes
print(Env.Seg.proset.relations)
print(Env.pset.symbols)
print(Env.pset.point())
print(Env.spec)
print(Env.b)

s4 = Env.segment(list('ACGTTPCA-CT'), '1')
print(s4)

print_with_margin('-' * 24)

Seqali = Env.seqali("align.fa")

print_with_margin("Database")

print(Seqali.indiv)
for i, (x, y) in enumerate(zip(Seqali.base, Seqali.database)):
  print(f"{i}) color: {x.colors[x.parse]}")
  print(x)
  for x in y:
    for xx in x:
      print(xx)
    print()

print_with_margin("Image")

for i, item in enumerate(Seqali.base):
  print(f"base[{i}]")
  print(item)
  sal = Seqali.eval(item)
  for x in sal:
    for y in x:
      print(y)
    print()

print_with_margin("Extending category")

l = Seqali.extending_category(Seqali.base[0])
for i, m in l:
  print(i)
  print(m.f1)
  print(m.f0)

print_with_margin("Extending category")

l = Seqali.extending_category(Seqali.base[1])
for i, m in l:
  print(i)
  print(m.f1)
  print(m.f0)

print_with_margin('-' * 24)

a = list('AGCTAGCTGA')
b = list('GTGGATCGATGA')

A = Sequence('a', a, '1')
B = Sequence('b', b, '1')

table = Table(A, B)
print()
print("incidence")
table.incidence()
table.stdout()
print()
print("fillout")
table.fillout()
table.stdout()
table.write("dprog.fa", mode = 'w', debug = False, display = True)

print_with_margin('-' * 24)

Env = Environment(Seg, E, 2, [1] * 2) #[] = white nodes
Seqali = Env.seqali("dprog.fa")

print_with_margin("Image")

print(Seqali.indiv)
print(Seqali.base[0])
sal = Seqali.eval(Seqali.base[0])
for x in sal:
  for y in x:
    print(y)
  print()
