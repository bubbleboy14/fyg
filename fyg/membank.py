import os
from .util import read, write

class MemBank(object):
	def __init__(self, bank="default"):
		self.name = bank
		self.path = os.path.join(".membank", bank)
		self.bank = {}
		self.load()

	def log(self, *msg):
		print("MemBank(%s)"%(self.name,), *msg)

	def load(self):
		if not os.path.isdir(".membank"):
			self.log("load() creating .membank/")
			movebank = os.path.isfile(".membank")
			movebank and self.log("load() renaming default")
			movebank and os.rename(".membank", ".membank-tmp")
			os.mkdir(".membank")
			movebank and os.rename(".membank-tmp", os.path.join(".membank", "default"))
		remembered = read(self.path)
		remembered and self.bank.update(remembered)
		self.log("loaded", self.name, "bank")

	def remember(self, key, data, ask=True):
		if ask and input("remember %s for next time? [Y/n] "%(key,)).lower().startswith("n"):
			return self.log("ok, not remembering", key)
		self.bank[key] = data
		write(self.path, membank)

	def recall(self, key):
		return self.bank.get(key, None)

	def get(self, key, default=None):
		val = self.recall(key)
		if not val:
			pstr = "%s? "%(key,)
			if default:
				pstr = "%s[default: %s] "%(pstr, default)
			val = input(pstr) or default
			self.remember(key, val)
		return val

membanks = {}

def getbank(name="default"):
	if name not in membanks:
		membanks[name] = MemBank(name)
	return membanks[name]

def remember(key, data, ask=True, bank="default"):
	getbank(bank).remember(data, ask)

def recall(key, bank="default"):
	return getbank(bank).recall(key)

def memget(key, default=None, bank="default"):
	return getbank(bank).get(key, default)