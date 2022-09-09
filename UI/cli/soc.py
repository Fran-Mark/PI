from paramiko import SSHClient, AutoAddPolicy,Transport




# Alternativa si no anda en linux
# transport = Transport('192.168.0.22') 
# transport.connect()
# transport.auth_none('root')

def cat_config():
    stdin, stdout, stderr = soc.exec_command("cat /mnt/client_config")
    lines = stdout.readlines()

    #fancy print
    for line in lines:
        print(line.strip())

    print("connected!")

    #close everything
    stdin.close()
    stdout.close()
    stderr.close()
    soc.close()
    print("disconnected!")


def __init__():
    soc = SSHClient()

    try:
        soc.connect('192.168.0.22', username='root', password=None)	
    except Exception as err:
        print('using transport')
        soc.set_missing_host_key_policy(AutoAddPolicy())
        soc.get_transport().auth_none('root')

    return soc



if __name__ == 'soc':
    soc = __init__()

