self.sp.rect[0]= min(400, self.sp.rect[0] + 5)
if self.forceDone:
	self.sp.rect[0]= 400
if self.sp.rect[0] < 400:
	self.scriptsDone.append(False)