# Feast + Denormalized Example

This repo contains an example showing how to use [denormalized](https://github.com/probably-nothing-labs/denormalized) to stream features into a feast online store.
Tested with python v3.12.4 and feast v0.40.1.

## Setup

- Run the [emit_measurements.rs](https://github.com/probably-nothing-labs/denormalized/blob/main/examples/examples/emit_measurements.rs) script from the denormalized repository (This involves running kafka in docker)
- Initialize the feast repo by running `feast apply` in the `src/feast_example/feature_repo` directory
- run `python src/feast_example/main.py`
