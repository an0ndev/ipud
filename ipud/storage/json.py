import ipud.storage.base as base
import json, copy

class JSONObjectStorage:
    def __init__ (self, internal_storage: base.DataSection, default):
        self.internal_storage = internal_storage

        self._obj = None
        if self._load ():
            for key, value in default.items (): self.setdefault (key, value)
            return
        self._obj = copy.deepcopy (default)
        self._save ()
    def get (self, key):
        return self._obj [key]
    def set (self, key, new_value):
        self._obj [key] = new_value
        self._save ()
    def apply (self, key, update_func):
        result = update_func (self.get (key))
        self._save ()
        return result
    def setdefault (self, key, default = None):
        if key in self._obj: return self._obj
        self._obj [key] = copy.deepcopy (default)
    def _load (self) -> bool: # success
        binary_json = self.internal_storage.read ()
        if binary_json is None: return False
        text_json = binary_json.decode ()
        self._obj = json.loads (text_json)
        return True
    def _save (self):
        text_json = json.dumps (self._obj)
        binary_json = text_json.encode ()
        self.internal_storage.write (binary_json)
