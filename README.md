# NTC Templates Dataset

This repository contains tools to generate a JSONL dataset by merging [NTC Templates](https://github.com/networktocode/ntc-templates) with their corresponding raw test files.

## Contents

-   `create_dataset.py`: Script to generate the dataset.
-   `verify_dataset.py`: Script to verify the generated dataset.
-   `ntc_templates_dataset.jsonl`: The generated dataset (approx. 1800 records).

## Usage

1.  Ensure you have `ntc-templates` cloned/available in the root directory (or update paths in scripts).
2.  Run generation:
    ```bash
    python create_dataset.py
    ```
3.  Run verification:
    ```bash
    python verify_dataset.py
    ```

## Requirements

-   Python 3+
-   `textfsm` (`pip install textfsm`)
