import sys

def sortkey(x):
  return -sum([1 << (31-i) for i in range(0,32) if x & (1 << i)])

# Perform Gaussian elimination to get linear combinations
# to obtain each standard basis vector from given basis vectors
def invert (vectors):
  vectors = [(vec & 0xffffffff) | (1 << (32+i)) for i,vec in enumerate(vectors)]
  vectors = sorted(vectors,key=sortkey)
  for i,vec in enumerate(vectors):
    vectors[i+1:len(vectors)] = sorted(vectors[i+1:len(vectors)],key = sortkey)
    for j in range (i+1,len(vectors)):
      if vectors[j] & lowbit(vectors[i]):
        vectors[j] ^= vectors[i]
  vectors = sorted(vectors,key=sortkey)
  for i,vec in reversed(list(enumerate(vectors))):
    for j in range(i-1,-1,-1):
      if vectors[j] & lowbit(vectors[i]):
        vectors[j] ^= vectors[i]
  return vectors

def getRepresentationOfVector(vec,basis):
  result = 0
  for i in range(0,32):
    if vec & (1 << i):
      result ^= basis[i] >> 32
  return result

def bitposns(x):
  l = []
  i = 0
  while x >> i:
    if x & (1 << i):
      l.append(i)
    i += 1
  return l

def printbits (x):
  for i in range(0,32):
    print x >> (63-i) & 1,
  print " ",
  for i in range(32,64):
    print x >> (63-i) & 1,
  print

def printbasis (l):
  for item in l:
    printbits(item)

def lowbit (x):
  for i in range (0,32):
    y = x & (1 << i)
    if y:
      return y
  return 0

def xorsum (l):
  result = 0
  for i in l:
    result ^= (i & 0xFFFFFFFF)
  return result

def gethashes (f):
  fh = open(f)
  sonnets = []
  hashes = []
  for line in fh:
    x = line.split()
    sonnets.append(x[0])
    hashes.append(int(x[1]))
  fh.close()
  return sonnets[0], hashes[0], sonnets[1:], hashes[1:]

def getrepresentation (f,goal):
  basesonnet, basehash, sonnets, hashes = gethashes(f)
  basis = invert(hashes)
  x = getRepresentationOfVector(goal^basehash,basis)
  return basehash,hashes,basesonnet,sonnets,bitposns(x)

def getsonnet (f,goal):
  basehash,hashes,basesonnet,sonnets,bps = getrepresentation(f,goal)
  #print (xorsum([hashes[i] for i in bps]))
  #print (bps)
  basesonnet = open(basesonnet).read()
  result = list(basesonnet)
  for j in bps:
    s = open(sonnets[j]).read()
    for i, c in enumerate(s):
      if basesonnet[i] != s[i]:
        result[i] = s[i]
  result = ''.join(result)
  print result,
  return result

if __name__ == '__main__':
  getsonnet("hfile",int(sys.argv[1], 16))
