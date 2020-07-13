self.sp.rect[1]= min(round(self.sp.rect[1]+self.vel), 200)
self.vel += 4
if self.forceDone:
	self.sp.rect[1]= 200