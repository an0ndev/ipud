import ipud.storage.folder as folder # test_folder_backed
# import ipud.model, ipud.types # test_initialize

import pathlib, typing

class ipudTest:
    def __init__ (self, debug: bool = False):
        self.debug = debug

        self.model = None
    def _debug_exec (self, func: typing.Callable):
        if self.debug: func ()
    def test_folder_backed (self):
        folder_loc = pathlib.Path (__file__).parent / "folder_backed"
        folder_loc.mkdir ()

        test_data = b"test"

        try:
            provider = folder.FolderBackedStorageProvider (folder_loc)
            section_one = provider.allocate ()
            section_one.write (test_data)
            section_two = provider.handle_at (2, allow_empty = True)
            section_two.write (test_data)
            assert section_one.read () == section_two.read ()
            section_three = provider.allocate ()
            assert section_three.location == (folder_loc / "3")
            provider.free (section_two)

            self._debug_exec (lambda: input ("enter for cleanup: "))
            provider.free (section_one)
            provider.free (section_three)
            provider.destruct ()
        finally:
            self._debug_exec (lambda: input ("enter to complete cleanup: "))
            if folder_loc.exists (): folder.FolderBackedStorageProvider._rmdir_recursive (folder_loc)
    def test_initialize (self):
        self.model = ipud.model.Model ()
        def User_ctor (_self, *, _id: ipud.types.internal.MemoryAddr, username: str, password: str):
            _self.id = _id
            _self.username = username
            _self.password = password

        self.model.types.User = ipud.types.Composite (
            id = ipud.types.internal.UFLTable,
            username = str,
            password = str
        )

disabled_tests = ["test_initialize"]