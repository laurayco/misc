"""
	Simulate CUDA's thread / block / grid system in serial.
	this is done as closely as possible with python with
	an OOP spin on things. This could easily be converted
	to actually be multi-threaded, but for the time being
	it helps to do this in serial for debugging purposes.
"""

def iter_tuple(t):
	z = 0
	while z < t[2]:
		y = 0
		while y < t[1]:
			x = 0
			while x < t[0]:
				yield x,y,z
				x+=1
			y+=1
		z+=1

def print_data(d):
	for row in d:
		print(*map("{:>3}".format,row))

class Kernel:
	def __init__(self,grid_dim,block_dim):
		self.grid_dim, self.block_dim = grid_dim, block_dim
	def __call__(self,*a,**k):
		for block in iter_tuple(self.grid_dim):
			shared = {}
			for thread in iter_tuple(self.block_dim):
				self.run(block,thread,shared,*a,**k)
			print("Block",block)
			print_data(shared['splat'])
	def run(self,block,thread):
		pass

if __name__=="__main__":
	from random import randint, seed;seed()

	class Halo(Kernel):
		def __init__(self):
			super().__init__((1,1,1),(10,10,1))
		def run(self,block,thread,shared,data):
			tx,ty,tz = thread
			bx,by,bz = block
			if tx==0 and ty==0 and tz==0:
				shared['splat'] = []
				for i in range(self.block_dim[1]+2):
					shared['splat'].append([0]*(self.block_dim[0]+2 ))
			splat = shared['splat']
			gx = bx*self.block_dim[0]+tx
			gy = by*self.block_dim[1]+ty
			splat[ty+1][tx+1] = data[gy][gx]

			if ty==0:
				if by==0:
					splat[0][tx+1] = 0
				else:
					splat[0][tx+1] = data[gy-1][gx]
			elif ty==self.block_dim[1]-1:
				if by==self.grid_dim[1]-1:
					splat[ty+1][tx+1] = 0
				else:
					splat[ty+1][tx+1]

			if tx==0:
				if bx==0:
					splat[ty+1][0] = 0
				else:
					splat[ty+1][0] = data[gy][gx-1]

			if tx==0 and ty==0: # top left
				if bx==0:
					splat[0][0] = 0
				else:
					splat[0][0] = data[gy-1][gx-1]

			elif tx==0 and ty==self.block_dim[1]-1: #bottom left
				if bx==self.grid_dim[1]-1:
					splat[ty+1][0] = 0
				else:
					splat[ty+1][0] = data[gy+1][gx]

			elif tx==self.block_dim[0]-1 and ty==self.block_dim[1]-1: #bottom right
				if bx==self.grid_dim[1]-1:
					splat[ty+1][tx+1] = 0
				else:
					splat[ty+1][tx+1] = data[gy+1][gx]
			
			elif tx==self.block_dim[0]-1 and ty==0: #top right
				if bx==self.grid_dim[1]-1:
					splat[0][tx+1] = 0
				else:
					splat[0][tx+1] = data[gy+1][gx]

	SIZE = 15
	data = [[randint(0,200) for i in range(SIZE)] for i in range(SIZE)]
	output = [x[:] for x in data]
	print("Original:")
	print_data(data)
	Halo()(data)

