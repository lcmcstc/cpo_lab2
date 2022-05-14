# HDU - lab2 - variant8

## Variant 8

Dictionary based on hash-map, open address

## laboratory work description

| Description                                 | Function style API           |
|---------------------------------------------|------------------------------|
| Add a new element                           | x = cons(lst, 3)             |
| Remove an element by value                  | x = remove(lst, 3)           |
| Size                                        | n = length(lst)              |
| Is member                                   | b = member(lst, v)           |
| Reverse(for ordered)                        | x = reverse(lst)             |
| Intersection(for sets)                      | b = intersection(lst1, lst2) |
| To built-in list                            | l = to_list(lst)             |
| From built-in list                          | x = from_list([12])          |
| Find element by specific predicate          | v = find(lst, is_even)       |
| Filter data structure by specific predicate | x = filter(lst, is_even)     |
| Map structure by specific function          | x = map(lst,increment)       |
| Reduce                                      | v = reduce(lst, sum)         |
| Function style iterator                     | i = iterator(lst)            |
| a monoid and implement `empty`              | x = empty()                  |
| a monoid and implement `concat`             | x = concat(lst1, lst2)       |
| Check equality method                       | \_\_eq\_\_                   |
| String serialization method                 | \_\_str\_\_                  |

## Project structure

- `HMOpenAddressDict.py` -- implementation of `Dictionary` class with `add` etc.
- `HMOpenAddressDict_test.py` -- unit and PBT tests for `Dictionary`.

## Features

- `__str__()`
- `__eq__(other)`
- `__iter()__`
- `cons(key, value, m)`
- `remove(m, key)`
- `length(m)`
- `member(key, m)`
- `reverse(li)`
- `to_list(m)`
- `from_list(m)`
- `find(li, key)`
- `filter(li, f)`
- `mmap(li,p)`
- `iterator(li)`
- `mempty()`
- `mconcat(m, o)`
- `exchangeDic2Tuples(d)`

- PBT:`test_from_list_to_list_equality(self, a)`
- PBT:`test_monoid_identity(self, a, b, c)`
- PBT:`test_python_len_and_list_size_equality(self, a)`

## Contribution

- Li ChangMinChen (212320023@hdu.edu.cn) -- HMOpenAddressDict.py
- Li Xiao (212320022@hdu.edu.cn) -- README.md and HMOpenAddressDict_test.py

## Changelog

- 13.05.2022 - 0
  - Initial commit
- 13.05.2022 - 1
  - Update README.md

## Design notes

- Create `Entry` class to implement key-value pairs.
- Create `Next` class to implement `__iter__` and `__next__`.
- Create `HMOpenAddressDict` class to implement the dictionary.
