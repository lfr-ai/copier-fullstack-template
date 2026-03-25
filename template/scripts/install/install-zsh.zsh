#!/usr/bin/env zsh
emulate -L zsh
setopt PIPE_FAIL ERR_EXIT


install_zsh() {
    emulate -L zsh
    setopt PIPE_FAIL ERR_EXIT

    if command -v zsh &>/dev/null; then
        print "Zsh already installed: $(zsh --version)"
    else
        print "Installing zsh..."

        if command -v apt-get &>/dev/null; then
            sudo apt-get update -qq
            sudo apt-get install -y -qq zsh
        elif command -v dnf &>/dev/null; then
            sudo dnf install -y zsh
        elif command -v brew &>/dev/null; then
            brew install zsh
        else
            print "ERROR: Unsupported package manager"
            return 1
        fi

        print "Zsh installed: $(zsh --version)"
    fi
}

install_oh_my_zsh() {
    emulate -L zsh
    setopt PIPE_FAIL ERR_EXIT

    local omz_dir="${HOME}/.oh-my-zsh"

    if [[ -d "${omz_dir}" ]]; then
        print "Oh My Zsh already installed at ${omz_dir}"
        return 0
    fi

    print "Installing Oh My Zsh..."
    sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended

    print "Oh My Zsh installed"
}

install_plugins() {
    emulate -L zsh

    local custom_dir="${ZSH_CUSTOM:-${HOME}/.oh-my-zsh/custom}"
    local plugins_dir="${custom_dir}/plugins"

    if [[ ! -d "${plugins_dir}/zsh-autosuggestions" ]]; then
        print "Installing zsh-autosuggestions..."
        git clone https://github.com/zsh-users/zsh-autosuggestions "${plugins_dir}/zsh-autosuggestions"
    else
        print "zsh-autosuggestions already installed"
    fi

    if [[ ! -d "${plugins_dir}/zsh-syntax-highlighting" ]]; then
        print "Installing zsh-syntax-highlighting..."
        git clone https://github.com/zsh-users/zsh-syntax-highlighting "${plugins_dir}/zsh-syntax-highlighting"
    else
        print "zsh-syntax-highlighting already installed"
    fi

    if [[ ! -d "${plugins_dir}/zsh-completions" ]]; then
        print "Installing zsh-completions..."
        git clone https://github.com/zsh-users/zsh-completions "${plugins_dir}/zsh-completions"
    else
        print "zsh-completions already installed"
    fi

    if ! command -v fzf &>/dev/null; then
        print "Installing fzf..."
        if command -v apt-get &>/dev/null; then
            sudo apt-get install -y -qq fzf
        elif command -v brew &>/dev/null; then
            brew install fzf
        fi
    else
        print "fzf already installed"
    fi
}

configure_zshrc() {
    emulate -L zsh

    local zshrc="${HOME}/.zshrc"

    if [[ ! -f "${zshrc}" ]]; then
        print "WARNING: ${zshrc} not found, skipping plugin configuration"
        return 0
    fi

    local desired_plugins="plugins=(git zsh-autosuggestions zsh-syntax-highlighting zsh-completions fzf docker)"

    if grep -q "^plugins=" "${zshrc}"; then
        local tmp_file="${zshrc}.tmp.$$"
        sed "s/^plugins=.*/${desired_plugins}/" "${zshrc}" > "${tmp_file}" && \
            mv "${tmp_file}" "${zshrc}"
        print "Updated plugins in ${zshrc}"
    else
        print "${desired_plugins}" >> "${zshrc}"
        print "Added plugins to ${zshrc}"
    fi
}

set_default_shell() {
    emulate -L zsh

    local zsh_path
    zsh_path="$(which zsh)"

    if [[ "${SHELL}" == "${zsh_path}" ]]; then
        print "Zsh is already the default shell"
        return 0
    fi

    print "Setting zsh as default shell..."
    if chsh -s "${zsh_path}" 2>/dev/null; then
        print "Default shell changed to zsh"
    else
        print "WARNING: Could not change default shell automatically"
        print "Run manually: chsh -s ${zsh_path}"
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

    print ""
    print "=== Zsh Setup Complete ==="
    print "Zsh:     $(zsh --version)"
    print "Shell:   ${SHELL}"
    print ""
    print "Restart your terminal or run: exec zsh"
}

main "$@"
