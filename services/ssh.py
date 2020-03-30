"""
Module delegated to handling ssh logic
"""

# Native Modules
import sys
import logging
from subprocess import call, Popen, PIPE, DEVNULL

# Custom Modules
from singletons.setup import SetupSingleton
from singletons.github import GithubSingleton

SETUP: SetupSingleton = SetupSingleton.get_instance()
GITHUB: GithubSingleton = GithubSingleton.get_instance()
LOGGER = logging.getLogger()


def public_key_exists() -> bool:
    """
    Check if public key exists to confirm whether ssh is already configured
    """
    command = f'find {SETUP.home_dir}/.ssh/id_rsa.pub'
    file_found = call(command.split(), stdout=DEVNULL, stderr=DEVNULL) == 0

    if not file_found:
        LOGGER.info('Git SSH hasn\'t been configured locally')
    else:
        LOGGER.info('Git SSH has been configured locally')

    return file_found


def generate_rsa_keypair():
    """
    Generate asymmetric public/private keypair for ssh use
    """
    command = f'ssh-keygen -t rsa -b 4096 -C \"{GITHUB.email}\" -N foobar'
    with Popen(command.split(), stdin=PIPE, stdout=PIPE, stderr=PIPE) \
            as process:
        out, err = process.communicate(input=b'\ny\n')

        if err:
            LOGGER.error(err.decode('utf-8'))
            LOGGER.error('RSA keypair for SSH has failed to generated')
            sys.exit()
        else:
            LOGGER.debug(out.decode('utf-8'))
            LOGGER.info('RSA keypair for SSH has successfully been generated')


def start_ssh_agent():
    """
    Start ssh-agent process in local machine
    """
    def find_ssh_process(line):
        """
        Processes output to log the ssh agent process
        """
        if not line:
            return

        user, pid = line.split()[:2]

        if 'egrep' not in line and user == SETUP.username:
            LOGGER.debug(f'Existing ssh-agent pid - {pid}')
            LOGGER.debug(f'{line}')

    command = 'ps aux'
    ps_process = Popen(command.split(), stdout=PIPE)

    command = 'egrep ssh-agent'
    with Popen(command.split(), stdin=ps_process.stdout, stdout=PIPE) \
            as process:
        out, err = process.communicate()
        grepped = process.returncode == 0
        ps_process.communicate()

        if err and not grepped:
            LOGGER.error(err.decode('utf-8'))
            LOGGER.error('Failed to grep')
            sys.exit()

        parsed_output = out.decode('utf-8').split('\n')

    list(lambda x: find_ssh_process(x), parsed_output)

    command_list = ['sh', '-c', f'eval \"$(ssh-agent -s)\"']
    with Popen(command_list, stdout=PIPE, stderr=PIPE) as process:
        out, err = process.communicate()

        if err:
            LOGGER.error(err.decode('utf-8'))
            LOGGER.error('SSH-agent process has failed to start')
            sys.exit()
        else:
            LOGGER.debug(out.decode('utf-8'))
            LOGGER.info('SSH-agent process has successfully started')


def register_private_key_to_ssh_agent():
    """
    Add ssh private key to ssh-agent
    """
    command = f'ssh-add -K {SETUP.home_dir}/.ssh/id_rsa'
    ssh_added = call(command.split(), stdout=DEVNULL) == 0

    if ssh_added:
        LOGGER.info('SSH private key has successfully been added to the '
                    'ssh-agent')
    else:
        LOGGER.error('SSH private key has failed to be added to the ssh-agent')
        sys.exit()


def get_public_key() -> str:
    """
    Return utf-8 string of ssh public key
    """
    command = f'cat {SETUP.home_dir}/.ssh/id_rsa.pub'
    with Popen(command.split(), stdout=PIPE, stderr=PIPE) as process:
        out, err = process.communicate()

        if err:
            LOGGER.error(err.decode('utf-8'))
            LOGGER.error('SSH public key is missing')
            sys.exit()

        LOGGER.debug(out.decode('utf-8'))
        parsed_output = out.decode('utf-8').split()
        key_type = parsed_output[0]
        key_data = parsed_output[1]

        public_key = f'{key_type} {key_data}'
        return public_key


def delete_ssh_rsa_keypair():
    """
    Delete both public and private key configured for ssh
    """
    command_list = ['sh', '-c', f'rm {SETUP.home_dir}/.ssh/id_rsa*']

    with Popen(command_list, stdout=PIPE, stderr=PIPE) as process:
        out, err = process.communicate()

        if err:
            LOGGER.error(err.decode('utf-8'))
            LOGGER.error('Failed to remove RSA keypairs configured for SSH')
            sys.exit()
        else:
            LOGGER.debug(out.decode('utf-8'))
            LOGGER.info('RSA keypairs configured for SSH has successfully been '
                        'removed')


def stop_ssh_agent():
    """
    Stop process responsible for ssh connections
    """
    command = 'ps aux'
    ps_process = Popen(command.split(), stdout=PIPE)

    command = 'egrep ssh-agent'
    egrep_process = Popen(command.split(), stdin=ps_process.stdout, stdout=PIPE)

    out, err = egrep_process.communicate()
    grepped = egrep_process.returncode == 0

    if err and not grepped:
        LOGGER.error(err.decode('utf-8'))
        LOGGER.error('Failed to grep')
        sys.exit()

    ps_process.communicate()

    pids_to_kill = []
    parsed_output = out.decode('utf-8').split('\n')
    for line in parsed_output:
        if not line:
            continue

        user, pid = line.split()[:2]

        if 'egrep' not in line and user == SETUP.username:
            LOGGER.debug(f'Existing ssh-agent pid - {pid}')
            LOGGER.debug(f'{line}')
            pids_to_kill.append(pid)

    for pid in pids_to_kill:
        command = f'kill {pid}'
        with Popen(command.split(), stdout=PIPE, stderr=PIPE) as process:
            out, err = process.communicate()

            if err:
                LOGGER.error(err.decode('utf-8'))
                LOGGER.error('Failed to stop ssh-agent process')
                sys.exit()
            else:
                LOGGER.debug(out.decode('utf-8'))
                LOGGER.debug('SSH-agent pid {pid} has been terminated')

    LOGGER.info('SSH-agent process has successfully been stopped')