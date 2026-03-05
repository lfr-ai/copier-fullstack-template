#!/usr/bin/env zsh
emulate -L zsh
setopt PIPE_FAIL ERR_EXIT

# Install zsh, oh-my-zsh, and useful plugins

install_zsh() {
    emulate -L zsh
    setopt PIPE_FAIL ERR_EXIT

    if command -v zsh &>/dev/null; then
        echo "Zsh already installed: $(zsh --version)"
    else
        echo "Installing zsh..."

        if command -v apt-get &>/dev/null; then
            sudo apt-get update -qq
            sudo apt-get install -y -qq zsh
        elif command -v dnf &>/dev/null; then
            sudo dnf install -y zsh
        elif command -v brew &>/dev/null; then
            brew install zsh
        else
            echo "ERROR: Unsupported package manager"
            return 1
        fi

        echo "Zsh installed: $(zsh --version)"
    fi
}

install_oh_my_zsh() {
    emulate -L zsh
    setopt PIPE_FAIL ERR_EXIT

    local omz_dir="${HOME}/.oh-my-zsh"

    if [[ -d "${omz_dir}" ]]; then
        echo "Oh My Zsh already installed at ${omz_dir}"
        return 0
    fi

    echo "Installing Oh My Zsh..."
    sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended

    echo "Oh My Zsh installed"
}

install_plugins() {
    emulate -L zsh

    local custom_dir="${ZSH_CUSTOM:-${HOME}/.oh-my-zsh/custom}"
    local plugins_dir="${custom_dir}/plugins"

    if [[ ! -d "${plugins_dir}/zsh-autosuggestions" ]]; then
        echo "Installing zsh-autosuggestions..."
        git clone https://github.com/zsh-users/zsh-autosuggestions "${plugins_dir}/zsh-autosuggestions"
    else
        echo "zsh-autosuggestions already installed"
    fi

    if [[ ! -d "${plugins_dir}/zsh-syntax-highlighting" ]]; then
        echo "Installing zsh-syntax-highlighting..."
        git clone https://github.com/zsh-users/zsh-syntax-highlighting "${plugins_dir}/zsh-syntax-highlighting"
    else
        echo "zsh-syntax-highlighting already installed"
    fi

    if [[ ! -d "${plugins_dir}/zsh-completions" ]]; then
        echo "Installing zsh-completions..."
        git clone https://github.com/zsh-users/zsh-completions "${plugins_dir}/zsh-completions"
    else
        echo "zsh-completions already installed"
    fi

    if ! command -v fzf &>/dev/null; then
        echo "Installing fzf..."
        if command -v apt-get &>/dev/null; then
            sudo apt-get install -y -qq fzf
        elif command -v brew &>/dev/null; then
            brew install fzf
        fi
    else
        echo "fzf already installed"
    fi
}

configure_zshrc() {
    emulate -L zsh

    local zshrc="${HOME}/.zshrc"

    if [[ ! -f "${zshrc}" ]]; then
        echo "WARNING: ${zshrc} not found, skipping plugin configuration"
        return 0
    fi

    local desired_plugins="plugins=(git zsh-autosuggestions zsh-syntax-highlighting zsh-completions fzf docker)"

    if grep -q "^plugins=" "${zshrc}"; then
        sed -i "s/^plugins=.*/${desired_plugins}/" "${zshrc}"
        echo "Updated plugins in ${zshrc}"
    else
        echo "${desired_plugins}" >> "${zshrc}"
        echo "Added plugins to ${zshrc}"
    fi
}

set_default_shell() {
    emulate -L zsh

    local zsh_path
    zsh_path="$(which zsh)"

    if [[ "${SHELL}" == "${zsh_path}" ]]; then
        echo "Zsh is already the default shell"
        return 0
    fi

    echo "Setting zsh as default shell..."
    if chsh -s "${zsh_path}" 2>/dev/null; then
        echo "Default shell changed to zsh"
    else
        echo "WARNING: Could not change default shell automatically"
        echo "Run manually: chsh -s ${zsh_path}"
    fi
}

main() {
    emulate -L zsh
    setopt PIPE_FAIL ERR_EXIT

    install_zsh
    install_oh_my_zsh
    install_plugins
    configure_zshrc
    set_default_shell

    echo ""
    echo "=== Zsh Setup Complete ==="
    echo "Zsh:     $(zsh --version)"
    echo "Shell:   ${SHELL}"
    echo ""
    echo "Restart your terminal or run: exec zsh"
}

main "$@"
