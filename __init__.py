import subprocess

import ranger.api.commands


class airdrop(ranger.api.commands.Command):
    """
    :airdrop [paths...]

    Share files with Apple devices using AirDrop.
    If no paths, share %s
    """

    def execute(self):
        paths = self.args[1:] or []

        if len(paths) == 0:
            paths = self.fm.get_macros()['s']

        if len(paths) == 0:
            self.fm.notify('empty directory', bad=True)
            return
        self._airdrop(paths)

    def _airdrop(self, paths):
        try:
            cmd = subprocess.Popen(['airdrop', *paths],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE
                                   )
            stdout, stderr = cmd.communicate()
            if cmd.returncode == 0:
                self.fm.notify(self._output_last_line(stdout))
            else:
                self.fm.notify(self._output_last_line(stderr), bad=True)
        except Exception as e:
            self.fm.notify(e, bad=True)

    @staticmethod
    def _output_last_line(output):
        if not output:
            return ''
        lines = output.decode('utf-8').strip().splitlines()
        if len(lines) == 0:
            return ''
        return lines[-1]
