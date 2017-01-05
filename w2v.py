from tables import *


class W2V:
    """
    The GoogleW2V simply accesses the GoogleNews.h5 file.
    It allows reading access to it, without loading it into the memory (which would take up to 8GB of ram..)

    The GoogleNews.h5 contains the same data as found in
    https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit
    and was converted by the convert-script in the data-directory
    """

    def __init__(self, fn="GoogleNews.h5"):
        """
        Initialize by loading the file and the table in the file
        """
        f = open_file(fn)
        self.table = f.root.vocabulary

    def __getitem__(self, key):
        """
        Return the 300-float vector representing the given word
        """
        return self.table.read_where("""word=={}""".format(key.encode(encoding="ISO-8859-1")))[0][0]

    def __contains__(self, key):
        try:
            self.__getitem__(key)
            return True
        except:
            pass
        return False