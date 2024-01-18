import json

class Config(object):
	def __init__(self, cfg):
		self._cfg = {}
		for key, val in list(cfg.items()):
			self.update(key, val)

	def __getattr__(self, key):
		return self._cfg.get(key)

	def __getitem__(self, key):
		return self._cfg.get(key)

	def __setitem__(self, key, val):
		self._cfg[key] = val

	def __contains__(self, key):
		return key in self._cfg

	def obj(self):
		obj = {}
		for k, v in list(self.items()):
			if v.__class__ == Config:
				obj[k] = v.obj()
			else:
				obj[k] = v
		return obj

	def json(self):
		return json.dumps(self.obj(), indent=4)

	# dict compabitility
	def get(self, key, fallback=None):
		return self._cfg.get(key, fallback)

	def values(self):
		return list(self._cfg.values())

	def items(self):
		return list(self._cfg.items())

	def keys(self):
		return list(self._cfg.keys())

	def update(self, key, val={}):
		self._cfg[key] = isinstance(val, dict) and Config(val) or val

	def sub(self, key):
		if key not in self._cfg:
			self.update(key)
		return self._cfg.get(key)

config = Config({
	"membank": {
		"root": ".membank",
		"default": "default"
	}
})