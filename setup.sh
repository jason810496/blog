#/bin/bash

theme_repo="https://github.com/nunocoracao/blowfish.git"
theme_path="themes/blowfish"

# check hugo is installed
if ! [ -x "$(command -v hugo)" ]; then
  echo 'Error: hugo is not installed.' >&2
  exit 1
fi

# check theme is installed
if [ ! -d "$theme_path" ] || [ -z "$(ls -A $theme_path)" ]; then
  echo "Cloning theme from $theme_repo"
  git clone --depth=1 $theme_repo $theme_path
fi