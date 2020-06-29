# NodePad

------

A simple node edit for visual scripting.

![nodepad.png](https://bitbucket.org/repo/p8k4Lrr/images/160901691-nodepad.png)


## About

------

NodePad is a python based visual scripting tool.
The software is still in development, and current goal is to make NodePad simple and protable as a standalone application( such as Windows Notepad for text edit ).


## Features ##

------

As a standalone editor app, NodePad provides following basic features.

- Open/Save files
- Undo/Redo of operation
- Import/Export of node graph
- Copy(Cut)/Paste of node graph

Below features are also available for advanced editing (still in development).

- Group/Ungroup of node graph
- Command-line interpreter

## Requirements ##

------

Python environment with following configuration is required at minimum.

* python 3 ( 3.5 or later recommended ) 
* PyQt5

## Installation ##

------

direct install from git

```
pip install git+https://masayan1115@bitbucket.org/masayan1115/nodepad.git
```

install after cloning

```
git clone https://masayan1115@bitbucket.org/masayan1115/nodepad.git
cd nodepad
pip install .
```

## Usage ##

------

```
python -m nodepad
```

or

```
cd nodepad
python nodepad
```

## License

------

