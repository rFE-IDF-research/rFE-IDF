def decrypt_new(pp, skx, cty, max_innerprod):

  (k1, k2) = skx
  (c1, c2) = cty

  t1 = innerprod_pair(c1, k1)
  t2 = pair(c2, k2)
  
  return solve_dlog_bsgs_new(t2, t1, max_innerprod+1)

def solve_dlog_bsgs_new(g, h, dlog_max):

  alpha = int(math.ceil(math.sqrt(dlog_max))) + 1
  g_inv = g ** -1
  tb = {}
  s = h
  t = g ** alpha
  m = 1
  dec_a = time.time()
  for i in range(alpha + 1):
    tb[m.__str__()] = i
    m = m * t
  dec_b = time.time()
  for j in range(alpha + 1):
    k = s.__str__()
    if k in tb:
      i = tb[k]
      return i * alpha + j
    s = s * g_inv
  return -1
  

