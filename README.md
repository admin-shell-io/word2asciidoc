## Installation

To work with the current development version, you can install the package directly from GitHub using Pip's Git feature:
```bash
pip install git+https://github.com/admin-shell-io/word2asciidoc.git@master
```

## Usage

To fix the adoc file, you need to invoke the ``fix_adoc.py`` script. If the output adoc file already exists, you need to
specify ``--force`` command-line argument in order to overwrite the existing files.

To fix an adoc file saved in ``/some/path/document.adoc`` and output the fixed adoc to ``/some/path/index.adoc``, run the following command:
```bash
    fix_adoc \
        --adoc_input /some/path/document.adoc \
        --adoc_output /some/path/index.adoc
```
If the previous method does not work try the following command:
```bash
    python -m word2asciidoc.fix_adoc \
        --adoc_input /some/path/document.adoc \
        --adoc_output /some/path/index.adoc
```
