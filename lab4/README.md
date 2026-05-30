# Geography hash table project

A small educational project for a hash table with:

- linear probing collision resolution,
- CRUD operations,
- thematic data about geography,
- printable table state,
- unit tests.

## Run

```bash
py -m src.main
```

## Tests

```bash
py -m unittest discover -s tests -v
py -m coverage run -m pytest -q
py -m coverage report -m
```
