# PyNamer
Just a python script that you can use to bulk rename files with editor of choice.\
By defualt, nvim is used, you can modify the constant at the top of the code, to use the editor you want.

To use it, you must have python installed, and no additional packages.\
It is recommended, to use newer versions of python, otherwise script might not work.\
You should also create an environment variable for this script, and use it outside of its directory.

### How to use
`pynamer.py -h` Print help on how to use the program.\
`pynamer.py --help` Same as the command above.

`pynamer.py` Bulk rename files in the current directory.\
`pynamer.py -p PATH` Bulk rename files for specific directory.\
`pynamer.py --path PATH` Same as the command above.

`pynamer.py -q` Run script in quiet mode, you won't get any output/confirmation promts.\
`pynamer.py --quiet` Same as the command above.

### Disclaimer
I am not responsible, for any damage that happens to your files/directories, while using this script.\
It is recommended to try this out on something not important first, in order understand how it works.\
