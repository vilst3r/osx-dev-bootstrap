# OSX-Dev-Bootstrap
Python script to replicate your personal development environment across any OSX
machine with packaging, editor profiles & settings. This is currently partially
personalized to my settings, feel free to use, fork or extend this however you
wish.

# Requirements
- To communicate with the GitHub API, add `config/git-credentials.txt` in the
project if it doesn't exist (otherwise the script generates it for you upon
initial setup execution which will prompt you to configure this before
proceeding)
    - e.g. `config/git-credentials.txt`
    ```text
      username: vilst3r
      email: clifford.phan@gmail.com
      token: ****************************************  <- personal_access_token
    ```
    - For your personal access token, you can generate this under
    `Developer settings` on [GitHub](https://github.com/settings/tokens)

# Optional (Personalizing your settings)
- `config/brew/leaves`: will contain all the brew packages delimited by
 the newline character.
    - See the [Brew registry](https://formulae.brew.sh/formula/) for the list
     of OSX binaries that are available
    - Use `brew leaves > leaves` to capture a snapshot of an existing
      environment's brew dependencies to use for this script
    - E.g. `config/brew/leaves`
    ```text
    python
    go
    git
    postgresql
    node
    docker
    vim
    gcc
    ```

- `config/brew/casks`: Similarly will contain all the cask
 packages delimited by the newline character.
    - See the [Cask registry](https://formulae.brew.sh/cask/) for the list of
     system applications that are available
    - Use `brew list --cask > casks` to capture a snapshot of an existing
      environment's cask dependencies to use for this script
    - E.g. `config/brew/casks`
    ```text
    docker
    emacs
    google-chrome
    google-drive-file-stream
    intellij-idea-ce
    iterm2
    microsoft-office
    postman
    pycharm-ce
    slack
    spotify
    sublime-text
    visual-studio-code
    ```

- `config/pip/leaves`: will contain all the pip packages in a special format
    - See the [PyPi registry](https://pypi.org/project/registry/) for the list
      of python packages that are available
    - Use `pip list --user > leaves` to capture a snapshot of an existing
      environment's PIP dependencies to use for this script
    - **Note**: Manual extension is quite tricky but as long as you specify the
      package name and its corresponding version delimited by a white space,
      then it should be fine.
    - E.g. `config/brew/casks`
    ```text
    Package             Version
    ------------------- ----------
    autopep8            1.5
    black               19.10b0
    flake8              3.7.9
    importmagic         0.1.7
    jedi                0.16.0
    numpy               1.14.5
    pexpect             4.7.0
    pipenv              2018.11.26
    powerline-gitstatus 1.3.1
    powerline-status    2.7
    pylint              2.3.1
    requests            2.22.0
    rope                0.16.0
    wheel               0.34.2
    ```


- A `dotfiles` git repository to take advantage of vim, bash & emac
 configurations. As long as you have that specific github repository name &
  the following three files:
    - `.bash_profile`
    - `.vimrc`
    - `.emacs`

# How to use
- Run `sudo ./setup.sh` to automate the processes within the script
- Run `sudo ./clean.sh` to rollback any changes from the script

# Automated Process Summary
1. Configures your SSH settings to hook into GitHub
2. Installs all brew packages from './config/brew/leaves
3. Installs all cask packages from './config/brew/casks
4. (Optional) As fore mentioned, if your GitHub account contains the repository
 `dotfiles`, then it'll pull that file & configure your vim, bash & emacs
  settings
5. Installs the powerline-status & configures it accordingly with your vim
 & bash settings
6. Installs all other pip packages from './config/pip/leaves

# Notes & Issues
- Password is required when OS X prompts you to enter your password for the
    keychain access, choosing 'Always Allow' would make the whole process
    seamless without any prompts from then onwards
- If any issues arises during the process, log output is available to diagnose
 for either `logs/setup/*.log` or `logs/clean/*.log` & run `./cleanup` to
  undo automated installations
- An E2E test is availabe for simulation before you run the main script, just
  run `./e2e-test/setup.sh` from the root directory (*Recommended*)

# TODO (potentially)
- Add iTerm2 configuration in spare time in the future
- Add C++ bits/header to setup
