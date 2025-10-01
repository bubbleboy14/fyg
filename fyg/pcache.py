import getpass, dotenv
from base64 import b64encode, b64decode
from .util import read, write, confirm, error
from .config import config

class PCache(object):
	def __init__(self, cfg):
		self.fname = cfg
		self._cache = read(cfg, isjson=True, default={}, b64=True)

	def _enc(self, val, noenc=False):
		return b64encode(val if noenc else val.encode()).decode()

	def _dec(self, val, noenc=False):
		return b64decode(val if noenc else val.encode()).decode()

	def _save(self):
		write(self._cache, self.fname, isjson=True, b64=True)

	def _denv(self, key):
		denvkey = config.dotenv[key]
		if not denvkey:
			error('"%s" not in dotenv map!'%(key,))
		if not hasattr(self, "_demap"):
			self._demap = dotenv.dotenv_values()
		if denvkey not in self._demap:
			error("'%s' not in env!"%(denvkey,))
		return self._demap[denvkey]

	def __call__(self, key, password=True, overwrite=False):
		dk = self._enc(key)
		if overwrite or dk not in self._cache:
			if config.dotenv: # non-interactive!
				return self._denv(key)
			else: # normal
				p = (password and getpass.getpass or input)(key)
				if not confirm("store %s"%(password and "password" or "value",)):
					return p
				self._cache[dk] = self._enc(p)
				self._save()
		return self._dec(self._cache[dk], True)