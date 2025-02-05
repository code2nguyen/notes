---
title: Setup
---

## Python

#### pyenv

Simple Python Version Management.

Link: https://github.com/pyenv/pyenv

```sh title="Install pyenv"
brew update@@
brew install pyenv

echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
```

```sh title="Use pyenv"
# Install and swith to python 3.11.1
pyenv install 3.11.10
pyenv global 3.11.10

# Auto select current python version from current directory or its sub directories
pyenv local

exec "$SHELL"
```

## Terminal 

### Iterm
Link : https://iterm2.com/index.html
