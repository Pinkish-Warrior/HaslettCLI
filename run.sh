#!/bin/bash
# Wrapper script for HaslettCLI to handle macOS library paths

# Check if on macOS and if homebrew is in /opt/homebrew
if [[ "$(uname)" == "Darwin" && -d "/opt/homebrew/lib" ]]; then
  export DYLD_LIBRARY_PATH="/opt/homebrew/lib"
fi

# Find the directory of the script and run the python script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
python3 "$DIR/haslettcli.py" "$@"
