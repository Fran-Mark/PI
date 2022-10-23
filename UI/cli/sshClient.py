import paramiko
import re

class ShellHandler:
    def __init__(self):
        self.ssh = paramiko.SSHClient()
        try:
            self.ssh.connect('192.168.0.22', username='root', password=None, timeout=1)
        except Exception as _:
            try:
                self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self.ssh.get_transport().auth_none('root')
                print('Connection established')
            except Exception as _:
                print('Unable to connect to CIAA')
                return

        channel = self.ssh.invoke_shell()
        self.stdin = channel.makefile('wb')
        self.stdout = channel.makefile('r')

    def __del__(self):
        self.ssh.close()

    @staticmethod
    def _print_exec_out(cmd, out_buf, err_buf):
        print(cmd)
        if len(out_buf) > 0:
            for line in out_buf:
                print(line.strip())
        if len(err_buf) > 0:
            for line in err_buf:
                print(line.strip())
        pass

    def execute(self, cmd):
        """

        :param cmd: the command to be executed on the remote computer
        :examples:  execute('ls')
                    execute('finger')
                    execute('cd folder_name')
        """
        cmd = cmd.strip('\n')
        self.stdin.write(cmd + '\n')
        finish = 'end of stdOUT buffer. finished with exit status'
        echo_cmd = 'echo {} $?'.format(finish)
        self.stdin.write(echo_cmd + '\n')
        shin = self.stdin
        self.stdin.flush()

        shout = []
        sherr = []
        exit_status = 0
        for line in self.stdout:
            if str(line).startswith(cmd) or str(line).startswith(echo_cmd):
                # up for now filled with shell junk from stdin
                shout = []
            elif str(line).startswith(finish):
                # our finish command ends with the exit status
                exit_status = int(str(line).rsplit(maxsplit=1)[1])
                if exit_status:
                    # stderr is combined with stdout.
                    # thus, swap sherr with shout in a case of failure.
                    sherr = shout
                    shout = []
                break
            else:
                # get rid of 'coloring and formatting' special characters
                shout.append(re.compile(r'(\x9B|\x1B\[)[0-?]*[ -/]*[@-~]').sub('', line).
                             replace('\b', '').replace('\r', ''))

        # first and last lines of shout/sherr contain a prompt
        if shout and echo_cmd in shout[-1]:
            shout.pop()
        if shout and cmd in shout[0]:
            shout.pop(0)
        if sherr and echo_cmd in sherr[-1]:
            sherr.pop()
        if sherr and cmd in sherr[0]:
            sherr.pop(0)

        self._print_exec_out(cmd=cmd, out_buf=shout, err_buf=sherr)
        return shin, shout, sherr

if __name__ == '__main__':
    shell = ShellHandler()
    while True:
        cmd = input()
        shell.execute(cmd)