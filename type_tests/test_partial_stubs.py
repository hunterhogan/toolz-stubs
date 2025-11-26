"""Verify that partial stubs are found for both toolz and tlz."""

import os

import tlz
import toolz

print("toolz location:", toolz.__file__)
print("tlz location:", tlz.__file__)

toolz_dir = os.path.dirname(toolz.__file__)
tlz_dir = os.path.dirname(tlz.__file__)

print("\ntoolz stub files:")
for file in os.listdir(toolz_dir):
    if file.endswith(".pyi"):
        print(f"  {file}")

print("\ntlz stub files:")
for file in os.listdir(tlz_dir):
    if file.endswith(".pyi"):
        print(f"  {file}")
