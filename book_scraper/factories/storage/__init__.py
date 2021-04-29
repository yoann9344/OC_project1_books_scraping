from .storage_factory import StorageFactory
from .local_storage import LocalStorage


storage_factory = StorageFactory()
storage_factory.register('local', LocalStorage)
# TODO implement cloud storage APIs
# storage_factory.register('google', GoogleDriveService)
# storage_factory.register('dropbox', DropboxService)
