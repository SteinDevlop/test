[tox]
envlist = py313
skipsdist = True

[testenv]
deps =
    pytest
    coverage
commands =
    coverage run -m pytest
    coverage xml

[coverage:run]
relative_files = True
source = src/backend/app
branch = True
