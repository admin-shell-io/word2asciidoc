# word2asciidoc

`word2asciidoc` is a comprehensive Python toolkit designed to support the conversion of Word documents to AsciiDoc files. Using the `pandoc` capabilities for the initial conversion, this package provides a set of post-processing scripts that enhance and refine the resulting output, improving the formatting, readability and compatibility of the final AsciiDoc document.

## Features

- **Image Conversion**: Converts EMF images to PNG and updates document references.
- **Character Escaping**: Escapes double angle brackets to avoid tag misinterpretation.
- **Note Styling**: Enhances the visibility of note boxes.
- **Bibliography Anchors**: Adds anchors to bibliography entries for in-document references.
- **Caption Fixing**: Ensures image captions use the correct block tag.
- **Bracket Escaping**: Prevents misinterpretation of square brackets by AsciiDoc processors.

## Converting Word Documents to AsciiDoc

### Online Conversion (Variant A)

1. Visit the [issue creation page](https://github.com/admin-shell-io/word2asciidoc/issues/new/choose) and select the "Transform Word Document to AsciiDoc" template.
2. Upload your Word file and submit the issue.
3. An AsciiDoc file will be generated from your Word file, and the package scripts will be applied to it. 
4. Once the conversion is complete, you'll receive a notification.
5. Download the converted AsciiDoc file from the link in the notification comment.
6. Do manual adjustments as needed (see [Manual Adjustments](#manual-adjustments)).

### Local Conversion (Variant B)

For local conversion:

1. Install [Pandoc](https://pandoc.org/installing.html).
2. Create a directory for your Word file, AsciiDoc output, and media.
3. Convert your document with Pandoc:
   ```shell
   pandoc [YOUR_DOCUMENT].docx -f docx -t asciidoctor --wrap=none --markdown-headings=atx --extract-media=[MEDIA_DIRECTORY] -o [OUTPUT_DIRECTORY]/[YOUR_DOCUMENT].adoc
   ```
4. Install `word2asciidoc` using pip:
```bash
pip install git+https://github.com/admin-shell-io/word2asciidoc.git@master
```
5. Apply `word2asciidoc` scripts to refine the AsciiDoc file with the following command:
    ```bash
    fix_adoc --adoc_input /path/to/input.adoc --adoc_output /path/to/output.adoc
    ```
    
    If you encounter issues, try running the script as a module:
    
    ```bash
    python -m word2asciidoc.fix_adoc --adoc_input /path/to/input.adoc --adoc_output /path/to/output.adoc
    ```
6. Do manual adjustments as needed (see [Manual Adjustments](#manual-adjustments)).

### Manual Adjustments

After running the scripts, manually check `[YOUR_DOCUMENT].adoc` for any unresolved issues. Refer to the [AsciiDoc User Manual](https://docs.asciidoctor.org/asciidoc/latest/) for guidance.

Common manual tasks include:

- **Table of Contents**: Remove or adjust the placement.
- **Document Attributes**: Set up necessary AsciiDoc attributes at the beginning of the file.
- **Table Formatting**: Ensure tables have headers and are formatted correctly.
- **Image Text Flow**: Verify that text flows correctly around images.

Example of setting document attributes:

```asciidoc
:toc: left
:toc-title: Table of Contents
:stylesheet: style.css
:favicon: favicon.png
:nofooter:

= Document Title
:author: Your Name
:revnumber: 1.0
:revdate: January 2023
:revremark: Initial release
```

## License

This project is under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.
