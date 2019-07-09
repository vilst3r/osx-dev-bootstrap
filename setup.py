#!/usr/bin/env python3

'''
Script to automate setup of unix environment with personal configurations and tools
'''

# System/Third-Party modules
import logging
import time

# Custom modules
from utils.setup_wrapper import SETUP
from utils.github_wrapper import GITHUB
import utils.powerline_helper as powerline_helper
import utils.git_helper as git_helper
import utils.ssh_helper as ssh_helper
import utils.brew_helper as brew_helper
import utils.vim_helper as vim_helper
import utils.bash_helper as bash_helper

LOGGER = logging.getLogger()

def install_brew_packages():
    '''
    Install brew packages 
    '''
    packages = brew_helper.get_uninstalled_brew_packages()

    for package in packages:
        brew_helper.install_that_brew(package)

    SETUP.print_process_step('Installation of brew packages are complete!')

def install_cask_packages():
    '''
    Reads brew-cask.txt file in child config directory to install all software applications
    '''
    packages = brew_helper.get_uninstalled_cask_packages()

    for package in packages:
        brew_helper.install_that_cask(package)

def install_homebrew():
    '''
    Install homebrew & cask if it doesn't exist in *nix environment and requires password input
    '''
    if brew_helper.brew_exists():
        SETUP.print_process_step('Homebrew is already installed!')
        return

    brew_helper.install_brew()
    brew_helper.tap_brew_cask()

    SETUP.print_process_step('Installation of homebrew is complete')

def configure_git_ssh():
    '''
    Configure git ssh key to user ssh agent
    '''
    if ssh_helper.public_key_exists():
        SETUP.print_process_step('Git SSH is already configured')
        return

    ssh_helper.generate_rsa_keypair()
    ssh_helper.start_ssh_agent()
    git_helper.update_ssh_config()
    ssh_helper.register_private_key_to_ssh_agent()

    current_public_key = ssh_helper.get_public_key()
    public_keys = GITHUB.get_public_keys().json()

    if git_helper.github_public_key_exists(current_public_key, public_keys):
        SETUP.print_process_step('Git SSH is already configured')
        return

    payload = {}
    payload['title'] = 'script-env-pub-key'
    payload['key'] = current_public_key
    GITHUB.create_public_key(payload)

    SETUP.print_process_step('SSH key for Git is configured')

def configure_vim():
    '''
    Configure vim settings
    '''
    vim_helper.pull_vim_settings()
    vim_helper.configure_vimrc()
    vim_helper.configure_color_themes()

    SETUP.print_process_step('Vim is now configured')

def configure_bash():
    '''
    Configure bash settings
    '''
    bash_helper.pull_bash_settings()
    bash_helper.configure_bash_profile()

    SETUP.print_process_step('Bash is now configured')

def install_powerline():
    '''
    Install powerline & configure it to bash & vim
    '''
    powerline_helper.install_powerline_at_user()
    powerline_helper.write_bash_daemon()
    powerline_helper.write_vim_config()
    powerline_helper.configure_user_config_directory()
    powerline_helper.install_fonts()

    powerline_helper.install_gitstatus_at_user()
    powerline_helper.config_git_colorscheme()
    powerline_helper.config_git_shell()

    SETUP.print_process_step('Powerline is installed & configured')

def pretty_print_wrapper(wrapper: object, title: str):
    '''
    Function to pretty print wrapper in beginning of setup
    '''
    LOGGER.debug(f'###### {title} #####')
    LOGGER.debug(f'{wrapper}')

def initialise_logger():
    '''
    Set up logging for writing stdout & stderr to files
    '''
    LOGGER.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    out_path = 'logs/setup_out.log'
    err_path = 'logs/setup_err.log'

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)

    out_handler = logging.FileHandler(f'{out_path}', 'w+')
    out_handler.setLevel(logging.DEBUG)
    out_handler.setFormatter(formatter)

    err_handler = logging.FileHandler(f'{err_path}', 'w+')
    err_handler.setLevel(logging.WARNING)
    err_handler.setFormatter(formatter)

    LOGGER.addHandler(out_handler)
    LOGGER.addHandler(err_handler)
    LOGGER.addHandler(stream_handler)

if __name__ == '__main__':
    initialise_logger()

    START = time.time()
    pretty_print_wrapper(SETUP, 'SetupWrapper')
    pretty_print_wrapper(GITHUB, 'GithubWrapper')

    configure_git_ssh()
    install_homebrew()
    install_brew_packages()
#    install_cask_packages()
    configure_vim()
    configure_bash()
    install_powerline()

    END = time.time()
    LOGGER.info(f'Setup time: {END - START} seconds')
