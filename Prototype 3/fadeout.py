self.curr_alpha= round(self.curr_frame*self.fade_spd)
self.mask.set_alpha(self.curr_alpha)
self.background= self.bg_copy.copy()
self.background.blit(self.mask, (0, 0))