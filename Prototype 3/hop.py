self.sp.rect[1]= min(round(self.sp.rect[1]+self.vel), 400)
self.vel += 4
if self.forceDone:
	self.sp.rect[1]= 400
if self.sp.rect[1] < 400:
	self.scriptsDone.append(False)