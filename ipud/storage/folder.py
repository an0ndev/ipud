import ipud.storage.base as base, ipud.storage.file as file, ipud.storage.json as json

import pathlib, typing
FolderLocation = pathlib.Path

FileID = int

class FileBackedDataSectionInFolder (file.FileBackedDataSection):
    def __init__ (self, path: file.FileLocation, _id: FileID):
        super ().__init__ (path)
        self.id = _id

class FolderBackedStorageProvider (base.DataProvider):
    def __init__ (self, folder: FolderLocation):
        self.folder = folder

        meta_file_handle = file.FileBackedDataSection (self.folder / "META")
        self.meta = json.JSONObjectStorage (
            internal_storage = meta_file_handle,
            default = {
                "next_new_id": 1,
                "freed_ids": [],
                "forced_open": []
            }
        )

    def allocate (self, size: base.Size = -1) -> FileBackedDataSectionInFolder:
        try:
            _id = self.meta.apply ("freed_ids", lambda x: x.pop (0))
        except IndexError:
            _id = self.meta.get ("next_new_id")
            while _id in self.meta.get ("forced_open"):
                self.meta.apply ("forced_open", lambda x: x.remove (_id))
                _id += 1
            self.meta.set ("next_new_id", _id + 1)

        path = self.folder / str (_id)
        with open (path, "wb+"): pass
        new_handle = FileBackedDataSectionInFolder (path, _id)

        return new_handle
    def handle_at (self, location: FileID, allow_empty: bool = False) -> typing.Optional [FileBackedDataSectionInFolder]:
        path = self.folder / str (location)
        if not path.exists ():
            if not allow_empty: return None
            if location not in self.meta.get ("forced_open"):
                self.meta.apply ("forced_open", lambda x: x.append (location))
        return FileBackedDataSectionInFolder (path, _id = location)
    def free (self, handle: FileBackedDataSectionInFolder):
        handle.location.unlink ()
        self.meta.apply ("freed_ids", lambda x: x.append (handle.id))
    def destruct (self):
        FolderBackedStorageProvider._rmdir_recursive (self.folder)
    @staticmethod
    def _rmdir_recursive (path: pathlib.Path):
        for item in path.iterdir ():
            if item.is_dir ():
                FolderBackedStorageProvider._rmdir_recursive (item)
            else:
                item.unlink ()
        path.rmdir ()
