import ipud.storage.base as base

import pathlib, typing
FileLocation = pathlib.Path

class FileBackedDataSection (base.DataSection):
    def __init__ (self, path: FileLocation):
        self.location = path
    def read (self) -> typing.Optional [bytes]:
        if not self.location.exists (): return None
        with open (self.location, "rb") as file:
            return file.read ()
    def write (self, new_value: bytes):
        with open (self.location, "wb") as file:
            file.write (new_value)
