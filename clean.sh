#!bash
rm -rf $(cat .gitignore | sed "s/\n//g")
git restore README.md
clear -x
