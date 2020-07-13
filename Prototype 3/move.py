self.sp.rect[0]= min(300, self.sp.rect[0] + 5)
if self.forceDone:
	self.sp.rect[0]= 300
if self.sp.rect[0] < 300:
	self.scriptsDone.append(False)