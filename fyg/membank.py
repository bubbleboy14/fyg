from .util import read, write

membank = {}
remembered = read(".membank")
remembered and membank.update(remembered)

def remember(key, data, ask=True):
	if ask and input("remember %s for next time? [Y/n] "%(key,)).lower().startswith("n"):
		return print("ok, not remembering", key)
	membank[key] = data
	write(".membank", membank)

def recall(key):
	return membank.get(key, None)

def memget(key, default=None):
	val = recall(key)
	if not val:
		pstr = "%s? "%(key,)
		if default:
			pstr = "%s[default: %s] "%(pstr, default)
		val = input(pstr) or default
		remember(key, val)
	return val

