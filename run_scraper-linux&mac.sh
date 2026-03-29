#!/bin/bash

SCRIPT_NAME="docs.py"
VENV_NAME="scraper_env"
REQ_FILE="requirements.txt"
REPO_OWNER="hanyu12138"
REPO_NAME="blueosdoc"
REPO_BRANCH="main"
CACHE_FILE=".blueosdoc-cdn-cache"

has_root_python_file() {
    find . -maxdepth 1 -type f -name "*.py" | grep -q .
}

build_raw_url() {
    local file_path="$1"
    echo "https://raw.githubusercontent.com/${REPO_OWNER}/${REPO_NAME}/${REPO_BRANCH}/${file_path}"
}

build_jsdelivr_url() {
    local file_path="$1"
    echo "https://cdn.jsdelivr.net/gh/${REPO_OWNER}/${REPO_NAME}@${REPO_BRANCH}/${file_path}"
}

build_ghproxy_url() {
    local file_path="$1"
    echo "https://ghproxy.net/$(build_raw_url "$file_path")"
}

build_url_by_source() {
    local source_name="$1"
    local file_path="$2"
    case "$source_name" in
        jsdelivr) build_jsdelivr_url "$file_path" ;;
        raw) build_raw_url "$file_path" ;;
        ghproxy) build_ghproxy_url "$file_path" ;;
        *) return 1 ;;
    esac
}

get_candidate_sources() {
    printf '%s\n' \
        "jsdelivr" \
        "raw" \
        "ghproxy"
}

download_with_curl() {
    local url="$1"
    local output="$2"
    local tmp_file="${output}.tmp.$$"
    if curl -L --fail --silent --show-error --connect-timeout 5 --max-time 30 -o "$tmp_file" "$url"; then
        mv "$tmp_file" "$output"
        return 0
    fi
    rm -f "$tmp_file"
    return 1
}

download_with_wget() {
    local url="$1"
    local output="$2"
    local tmp_file="${output}.tmp.$$"
    if wget -q -O "$tmp_file" --timeout=30 "$url"; then
        mv "$tmp_file" "$output"
        return 0
    fi
    rm -f "$tmp_file"
    return 1
}

get_cached_source() {
    if [ ! -f "$CACHE_FILE" ]; then
        return 1
    fi

    local cached_source
    cached_source="$(tr -d '\r\n' < "$CACHE_FILE")"
    if [ -z "$cached_source" ]; then
        return 1
    fi

    while IFS= read -r source; do
        if [ "$source" = "$cached_source" ]; then
            printf '%s\n' "$cached_source"
            return 0
        fi
    done <<EOF
$(get_candidate_sources)
EOF

    return 1
}

set_cached_source() {
    local source_name="$1"
    printf '%s\n' "$source_name" > "$CACHE_FILE"
}

clear_cached_source() {
    rm -f "$CACHE_FILE"
}

download_file_from_source() {
    local source_name="$1"
    local file_path="$2"
    local output="$3"
    local current_url=""

    current_url="$(build_url_by_source "$source_name" "$file_path")"

    if command -v curl >/dev/null 2>&1; then
        echo "Downloading ${output}: ${current_url}"
        download_with_curl "$current_url" "$output"
        return $?
    fi

    if command -v wget >/dev/null 2>&1; then
        echo "curl not found, using wget to download ${output}."
        echo "Downloading ${output}: ${current_url}"
        download_with_wget "$current_url" "$output"
        return $?
    fi

    echo "Error: neither curl nor wget is available, cannot download ${output}."
    return 1
}

download_required_files_from_source() {
    local source_name="$1"
    local files_to_download=""

    [ ! -f "$SCRIPT_NAME" ] && files_to_download="$files_to_download $SCRIPT_NAME"
    [ ! -f "$REQ_FILE" ] && files_to_download="$files_to_download $REQ_FILE"

    if [ -z "$files_to_download" ]; then
        return 0
    fi

    for file_name in $files_to_download; do
        if ! download_file_from_source "$source_name" "$file_name" "$file_name"; then
            echo "Download failed: $file_name (source: $source_name)"
            return 1
        fi
    done

    return 0
}

ensure_runtime_files() {
    local cached_source=""
    local source_name=""

    if [ -f "$SCRIPT_NAME" ] && [ -f "$REQ_FILE" ]; then
        return 0
    fi

    if ! has_root_python_file; then
        echo "No Python file found in the current directory, starting bootstrap download."
    else
        echo "Runtime files are missing, starting bootstrap download."
    fi

    if cached_source="$(get_cached_source)"; then
        echo "Trying cached source first: $cached_source"
        if download_required_files_from_source "$cached_source"; then
            return 0
        fi
        echo "Cached source is unavailable, trying built-in sources."
        clear_cached_source
    fi

    while IFS= read -r source_name; do
        echo "Trying source: $source_name"
        if download_required_files_from_source "$source_name"; then
            set_cached_source "$source_name"
            return 0
        fi
    done <<EOF
$(get_candidate_sources)
EOF

    echo "Error: failed to download required runtime files."
    exit 1
}

if ! command -v python3 >/dev/null 2>&1; then
    echo "Error: Python 3 was not found."
    exit 1
fi

echo "Python found: $(python3 --version)"

ensure_runtime_files

if [ ! -f "$SCRIPT_NAME" ]; then
    echo "Error: Python script '$SCRIPT_NAME' was not found."
    exit 1
fi

if [ -d "$VENV_NAME" ]; then
    if [ -f "$VENV_NAME/bin/python" ] && [ -s "$VENV_NAME/bin/python" ]; then
        echo "Reusing virtual environment '$VENV_NAME'."
    else
        echo "Broken virtual environment detected, recreating '$VENV_NAME'."
        rm -rf "$VENV_NAME"
    fi
fi

if [ ! -f "$VENV_NAME/bin/python" ]; then
    echo "Creating virtual environment: $VENV_NAME"
    python3 -m venv "$VENV_NAME"
    if [ $? -ne 0 ]; then
        echo "Failed to create virtual environment."
        exit 1
    fi
fi

echo "Activating virtual environment..."
source "$VENV_NAME/bin/activate"

echo "Upgrading pip..."
python -m pip install --upgrade pip

echo "Installing dependencies from $REQ_FILE..."
python -m pip install -r "$REQ_FILE"
if [ $? -ne 0 ]; then
    echo "Failed to install dependencies."
    deactivate
    exit 1
fi

echo "Starting script: $SCRIPT_NAME"
python "$SCRIPT_NAME"

deactivate
echo "Script completed."
