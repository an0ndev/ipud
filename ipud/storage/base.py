import abc, typing

Location = typing.Hashable
Size = int

class DataSection (abc.ABC):
    # def __init__ (self, location: Location): self.location = location
    @abc.abstractmethod
    def read (self) -> typing.Optional [bytes]: pass
    @abc.abstractmethod
    def write (self, new_value: bytes): pass

class DataProvider (abc.ABC):
    @abc.abstractmethod
    def allocate (self, size: Size) -> DataSection: pass
    @abc.abstractmethod
    def handle_at (self, location: Location) -> typing.Optional [DataSection]: pass
    @abc.abstractmethod
    def free (self, handle: DataSection): pass

"""
class HeapSection (DataSection):
    def __init__ (self, parent: "DataProvider", location: Location, size: Size):
        self.parent = parent
        self.location = location
        self.size = size
    def read (self) -> bytes:
        # noinspection PyProtectedMember
        return self.parent._read (self)
    def write (self, new_value: bytes):
        new_size = len (new_value)
        if new_size != self.size: self._reallocate (new_size)
        # noinspection PyProtectedMember
        self.parent._write (self, new_value)
    def _reallocate (self, new_size: Size):
        # noinspection PyProtectedMember
        self.parent._reallocate (self, new_size)
    def _copy_attribs_from (self, other: "HeapSection"):
        self.location = other.location
        self.size = other.size

# class BaseHeapProvider (DataProvider):
    @abc.abstractmethod
    def _read (self, handle: HeapSection) -> bytes: pass
    @abc.abstractmethod
    def _write (self, handle: HeapSection, new_value: bytes): pass
    def _reallocate (self, handle: HeapSection, new_size: Size):
        self.free (handle)
        new_handle = self.allocate (new_size)
        # noinspection PyProtectedMember
        handle._copy_attribs_from (new_handle)
"""
