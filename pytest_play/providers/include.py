import os
from . import BaseProvider


class IncludeProvider(BaseProvider):
    """ PlayEngine wrapper """

    def command_include(self, command, **kwargs):
        """ Include scenario """
        file_path = os.path.normcase(command['path'])
        data = self.engine.get_file_contents(file_path)
        self.engine.execute_raw(data)
