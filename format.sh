#!/bin/bash

black --line-length 120 --exclude protos app
ruff check app --fix-only