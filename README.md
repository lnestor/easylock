# EasyLock

## Description

EasyLock is a tool to add various types of logic locking to a Verilog circuit. My resaerch requires me to test tools against circuits with multiple different types of locking implemented, so I added this tool to easily lock any circuit with different techniques.

## Installation

All dependencies can be installed with `pip3 install -r requirements.txt`. I recommend you use a virtual environment made with `venv` when running this project. Use `python3 -m venv .env` and then `source .env/bin/activate` to create and activate the virtual environment.

## Usage

To lock a circuit, you must provide the circuit file name and a configuration file as shown below. If a `-o` flag is specified, it will save the new circuit to the given output file. Otherwise, it will print it to `stdout`.

```
python3 easylock/easylock.py CIRCUIT_FILE --config CONFIG_FILE [-o OUTPUT_FILE]
```

### Configuration

The locking is controlled by the contents of the configuration file. This file determines what type of locking to add and how/where it is added. An example configuration file is shown below.

```
---
name: SARLock with 2 Multiplexers
passes:
  - name: SARLock
    locking-type: sarlock
    integration-node:
      type: output
    number-bits: 2
    primary-input-start: 0
  - name: Mux
    locking-type: multiplexer
    integration-node:
      type: previous
    control-type: normal
    number-to-add: 2
    primary-input-start: continuous
```

The tool works by locking the circuit in multiple passes, and the configuration file must reflect this. Each pass adds a new type of locking to the circuit. For example, in the configuration file above, the first pass adds a SARLock circuit, and the second pass adds two multiplexers to the circuit. The key words under each pass in the configuration file specify how the locking should be added. See `docs/CONFIGURATION.md` for a detailed explanation of each key word in the configuration file.

## Extending with New Locking Types

You are able to add your own locking techniques to be used with this tool. The `data/definitions.yaml` file contains all the available locking types, so to add your own type, you need to add to that file.

Each new locking type requires three keys in the `definitions.yaml` file:
 - `name`: a descriptive name of the locking
 - `key`: this is the name that will be recognized in the configuration file. For example, if you put "mylocking" for this field, you need to also put "mylocking" in the configuration file for EasyLock to recognize the locking technique
 - `module`: the location of the python module that contains the locking code. This module must contain two functions: `args_from_config` and `run`. The `args_from_config` function is used to convert the configuration to any arguments needed by your locking algorithm. The `run` method is used to actually run the locking algorithm.

## Notes

This project is finished and as such I can't guarentee it works as intended. It has worked in the use cases I have needed, but I have not exhaustively tested it.
