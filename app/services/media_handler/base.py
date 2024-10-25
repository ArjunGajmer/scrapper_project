import abc


class MediaDataManager(abc.ABC):

    @abc.abstractmethod
    def get_load_add_save(self, url: str, file_save_path: str):
        pass
