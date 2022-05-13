# HDU - lab 1 - variant 8

## Variant 8

Dictionary based on hash-map, open address

## laboratory work description

• Add a new element  (lst.add(3))
• Set an element with specific index / key (lst.set(1, 3)) if applicable.
• Remove an element by (lst.remove(3)):

- index for lists
- key for dictionaries - value for sets value

• Access:

- size (lst.size())
- is member (lst.member(3))
- reverse (lst.reverse() (if applicable)

• Conversion from/to built-in list :

- from_list (lst.from_list([12, 99, 37]))
- to_list (lst.to_list())

• Filter data structure by specific predicate (lst.filter(is_even))
• Map1 structure by specific function (lst.map(increment))
• Reduce2 – process structure elements to build a return value by specific functions(lst.reduce(sum))
• Data structure should be an iterator3 in Python style
• Data structure should be a monoid and implement empty and concat methods

## Project structure

- `Hashmap_mutable.py` -- implementation of `Dictionary` class with `add` etc.
- `test_mutable.py` -- unit and PBT tests for `Dictionary`.

## Features

- `to_list( )`
- `from_list(tlist)`
- `compute_index(key)`
- `delete_que_by_key(key)`
- `find(key)`
- `add(key, value)`
- `set(key, value)`
- `get(key)`
- `remove(key)`
- `size( )`
- `_contains_(item)`
- `contains_value(item)`
- `contain_key(item)`
- `filter(p)`
- `map(p)`
- `reduce(p)`
- `empty( )`
- `concat(other)`
- `reverse()`
- `__next__( )`
- `__iter__( )`
- PBT: `test_from_list_to_list_equality(a)`
- PBT: `test_python_len_and_list_size_equality(a)`

## Contribution

- Li ChangMinChen (212320023@hdu.edu.cn) -- Hashmap_mutable.py
- Li Xiao (212320022@hdu.edu.cn) -- README.md

## Changelog

- 13.05.2022 - 0
  - Initial commit

## Design notes

- Create `Myentry` class to implement key-value pairs.
- Create `MyIter` class to implement `__iter__` and `__next__`.
- Create `MyDictionary` class to implement the dictionary.
