import os
import subprocess
import pexpect

print('Initializing Container')

if os.getenv('VPN_ENABLE', True):
    vpnAuth = os.getenv('VPN_AUTH', True)
    username = os.getenv('WINDSCRIBE_USERNAME', True)
    password = os.getenv('WINDSCRIBE_PASSWORD', True)
    location = "best"

    subprocess.run(["windscribe", "start"])

    child = pexpect.spawn('windscribe login')

    cond = child.expect(['Already Logged in', 'Windscribe Username: ', pexpect.EOF], timeout=50)
    if cond == 1:
        child.sendline(username)
        child.expect(['Windscribe Password: ', pexpect.EOF])
        child.sendline(password)

    child.wait()

    child = pexpect.spawn(f"windscribe connect {location}")
    cond = child.expect(['Please login to use Windscribe', 'Service communication error', pexpect.EOF], timeout=50)
    if cond == 0:
        raise Exception(f"Unable to properly connect to Windscribe. Make sure username/password is correct in the {vpnAuth} file.")
    elif cond == 1:
        raise Exception(f"Unable to properly connect to Windscribe service. Please restart docker.")

    child.wait()

    child = pexpect.spawn('windscribe firewall on')
    cond = child.expect(['Please login to use Windscribe', 'Service communication error', pexpect.EOF], timeout=50)
    if cond == 0:
        raise Exception(f"Unable to properly connect to Windscribe. Make sure username/password is correct in the {vpnAuth} file.")
    elif cond == 1:
        raise Exception(f"Unable to properly connect to Windscribe service. Please restart docker.")

# Sleep to allow for VPN to connect before trying to init python
print('Initializing Deluge')
subprocess.run(["/usr/bin/python3", "/usr/bin/run.py"])
