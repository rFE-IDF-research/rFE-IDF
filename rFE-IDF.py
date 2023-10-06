import sys, os
sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(1, os.path.abspath('..'))

import math, random, time, hashlib, numpy as np
from fhipe import ipe
from numpy import random

n = 10 # the dimension of vector H(r) and k
ell = 6 # the message length

q = 65537 # the value of parameter q
p = 257 # the value of parameter p

m = [random.randint(0, 255) for i in range(ell)] # the input message

def hash(r):
	"""
	Solve hash value of r using SHA160 algorithm
	"""
	string_r = str(r).encode('utf-8')

	r_hash_object = hashlib.sha1(string_r)
	r_hash = r_hash_object.hexdigest()
  
	r_arr = []
	r_s = ""

	for i in range(len(r_hash)):
		r_s += r_hash[i]
		if (i+1)%4 == 0: # partition a SHA160 digest into a vector of length 10
			int_hex = int(r_s, 16)
			r_arr.append(int_hex)
			r_s = ""
	return(r_arr)

def KHPRF(k,r):
	"""
	Compute KHPRF value with k and r
	"""
	hash_arr = hash(r)
	if len(k) != len(hash_arr):
		print("Wrong array dimension!")
  	
	s = 0
	for i in range(len(k)):
		s += k[i]*hash_arr[i]
	s = round((float(p)/float(q))*(s % q))
	return s


def setup():
	"""
	Setup all parameters required
	"""
	k = [random.randint(0, q) for i in range(n)] # master key k
	
	(pk, msk) = ipe.setup(n+4) # invoke FPL-FE setup
		
	pp = (pk)
	mk = (msk,k)
		
	return (pp,mk)

def encrypt(pp,mk,m):
	"""
	Encrypt a message
	"""
	pk = pp
	(msk,k) = mk

	r = [random.randint(0, q) for i in range(len(m))] # public parameter r
		
	c = []
	h = []
	
	for i in range(len(m)):
		c.append((m[i] + KHPRF(k,r[i])) % p)
		e = random.normal(loc=0, scale=2, size=(1,1)) # sample a Gaussian noise with standard deviation equals 2
		r_arr = hash(r[i])
		r_arr.append(round(float(e)))
		r_arr.append(0)
		r_arr.append(0)
		r_arr.append(0)
		h.append(ipe.encrypt(msk, r_arr))
	ct = (c,h,r)
	return ct

def keygen(mk):
	(msk,k) = mk
	k1 = [random.randint(0, q) for i in range(n)]
	k2 = []
	for i in range(n):
		k2.append((k[i] - k1[i]) % q)
	k2.append(1)
	k2.append(0)
	k2.append(0)
	k2.append(0)
	g = ipe.keygen(msk, k2)
	sk = (k1, g)
	return sk
	
def decrypt(pp, ct, sk):
	(c, h, r) = ct
	(k1, g) = sk
	m_prime = []
	total = 0
	for i in range(len(m)):
		dec_a = time.time()
		prod = ipe.decrypt_new(pp, g, h[i], q*q*n) # invoke FPL-FE decryption algorithm
		dec_b = time.time()
		KHPRF2 = round((float(p)/float(q))*(prod % q)) # rounding the decrypted result to domain Z_p
		m_prime.append((c[i] - KHPRF(k1,r[i]) - KHPRF2) % p)
		total = total + (dec_b-dec_a)
		print("The " + str(i) + "-th item is decrypted: " + str(prod) + ", and the decryption time is: " + str(dec_b-dec_a))
	print("Total decryption time: " + str(total))
	return m_prime
	

setup_a = time.time()
(pp, mk) = setup()
setup_b = time.time()
print("The input message: " + str(m) + ", and the setup time is: " + str(setup_b-setup_a))
enc_a = time.time()
ct = encrypt(pp,mk,m)
(c, h, r) = ct
enc_b = time.time()
print("The encrypted message: " + str(c) + ", and the encryption time is: " + str(enc_b-enc_a))
keygen_a = time.time()
sk = keygen(mk)
keygen_b = time.time()
print("The decryption key is generated, and the keygen time is: " + str(keygen_b-keygen_a))
dec_a = time.time()
m_prime = decrypt(pp,ct,sk)
dec_b = time.time()
print("The decrypted message: " + str(m_prime) + ", and the total decryption time is: " + str(dec_b-dec_a))

