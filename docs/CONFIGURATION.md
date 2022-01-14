# Configuration

## Description

The configuration file is a yaml file that contains the locking techniques to use and how/where it is added. This file explains the structure and key words for each locking technique. Any custom locking techniques you add can define their own key words.

## Structure

The configuration file is shown below. The top level `name` gives a descriptive name to the function of the configuration file. The actual locking passes are given as a list under a `passes` key word. Each pass must provide a descriptive name for the pass, a locking type, and then key words required by the locking technique. The locking type must match exactly what is listed in the `definitions.yaml` file explained in the readme.

```
---
name: Descriptive Name
passes:
  - name: Pass 1 Name
    locking-type: locking1
    key1: value1
    key2: value2
  - name: Pass 2 Name
    locking-type: locking2
    key1: value1
    key2: value2
```

## Locking Technique Key Words

### Shared

These key words are shared between all locking techniques.

The `integration-node` determines where the locking technique is placed in the circuit. Underneath the `integration-node` key word, use `type` to determine the type of net to place on. `output` means to place on a random output, while `net` means to place on a specific net. `previous` means to place it on the output net from the previous pass. The `name` key word is used in conjunction with a type `net` and contains the specific net name to place the locking on.

```
integration-node:
  type: output, net, previous
  name: net-name
```

The `interference` key word is used instead of the `integration-node` key word and also determines where to place the locking in the circuit. The `type` key word determines what type of interference to add. The `pass` key word references a previous pass. For example, having a pass of 1 means that the current pass should interfere with pass 1. The `distance` parameter determines how far away the two interfering key gates shouldbe placed. A distance of 3 means they should be 3 gate hops away.

```
interference:
  type: direct, indirect, none
  pass: 0, 1, etc.
  distance: 0, 1, etc.
```

The `primary-input-start` key word determines what index the first primary input used will be. Any locking technique that uses primary inputs can use this key word. If this key word is a number, it will be that index exactly. `continuous` means it will be the next index after the last one from the previous pass.

```
primary-input-start: 0, 1, etc., continuous
```

### SARLock

Adds a SARLock block to the circuit.

Key Words:
 - `number-bits`: the number of key bits to add to the SARLock block. This also determines the number of primary inputs that are used. The original SARLock paper uses the number of priamry inputs as the number of key bits.
 - `priamry-input-start`: the index of the first primary input to use in the SARLock block. Usually this is set to 0.

### Multiplexer

Adds a number of multiplexers to the circuit.

Key Words:
 - `control-type`: the type of circuit to use for the control bit of the multiplexers. Only `normal` is implemented currently. `normal` means the control bit is an XOR of a key input and primary input.
 - `number-to-add`: the number of multiplexers to add. They will be added one after another.

### Single XOR Key Gate

Adds a single XOR key gate to the circuit

There are no special key words for this technique.
