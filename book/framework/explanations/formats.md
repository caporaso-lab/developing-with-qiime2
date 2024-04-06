(formats-explanation)=
# File Formats and Directory Formats

{term}`Formats <Format>` in QIIME 2 are on-disk representations of data.
When associated with an {term}`artifact class`, they define how data are stored in or read from the `data/` directory of {term}`artifacts <Artifact>`.

QIIME 2 doesn't have much of an opinion on how data should be represented or stored, so long as it *can* be represented or stored in an {term}`archive`.

## File Formats

The simplest `Formats` are the `TextFileFormat` (`qiime2.plugin.TextFileFormat`) and the `BinaryFileFormat` (`qiime2.plugin.BinaryFileFormat`).
These formats represent a single file with a fixed on-disk representation.

(formats-validation-explanation)=
### Validation

Both types of `FileFormat` support validation.
This is (typically) a small bit of code that is run when initially loading a file from an {term}`archive` that allows the framework to ensure that the the data contained within the {term}`archive` at least *looks* like its declared {term}`type`.
This works very well for on-the-fly loading and saving, and goes a long way to preventing corrupt or invalid data from persisting.
The one "gotcha" here is that in order to keep things quick, we typically recommend that "minimal" validation occurs over a limited subset of the file (e.g. the first 10 records in a FASTQ file).
Because of this, formats allow for multiple levels of sniffing to be defined.
As of this writing (March 2024) there currently there are two validation levels: `min` and `max`.

Here we provide an example of a `TextFileFormat` definition, with a focus on the `_validate_` function.

```python
class IntSequenceFormat(TextFileFormat):
    """
    A sequence of integers stored on new lines in a file.
    To make validation more interesting, values in the list can be any integer as long
    as that integer is not equal to the previous value plus 3
    (i.e., `line[i] != (line[i-1]) + 3`).
    """
    def _validate_n_ints(self, n):
        with self.open() as fh:
            previous_val = None
            for idx, line in enumerate(fh, 1):
                if n is not None and idx >= n:
                    # we have passed the min validation level,
                    # so bail out
                    break
                try:
                    val = int(line.rstrip('\n'))
                except (TypeError, ValueError):
                    raise ValidationError(
                        f"Line {idx} contains {val}, but must be an integer.")
                if previous_val is not None and previous_val + 3 == val:
                    raise ValidationError(
                        f"Value on line {idx} is 3 more than the value on "
                        f"line {idx-1}.")
                previous_val = val

    # `_validate_` is exposed through the public method `validate`.
    def _validate_(self, level):
        record_map = {'min': 5, 'max': None}
        self._validate_n_ints(record_map[level])

format_instance = IntSequenceFormat(temp_dir.name, mode='r')
format_instance.validate()  # Shouldn't error!
```

In the `IntSequenceFormat` example, when `validate` is called with `level='min'`, `_validate_` will check the first 5 records.
Otherwise, when `level='max'`, it will check the entire file.

Astute observers might notice that the method defined in the `IntSequenceFormat` is called `_validate_`, but the method called on the `format_instance` was `validate`.
This is because defining format validation is optional (although highly recommended!).

```{warning}
We consider skipping validation all together when defining formats to be a plugin development anti-pattern.
For more information, see [](antipattern-skipping-validation).
```

Every format has a `validate` method available to interfaces (for performing ad-hoc validation).
The framework will check for the presence of a `_validate_` method on the format in question, and if it exists it will include that method as part of more general validations that the framework will perform.
The aim here is that the framework is capable of ensuring common basic patterns, like presence of required files, while the `_validate_` method is the place for the format developer to declare any special "business" logic necessary for ensuring the validity of their format.

### Text File Formats

The `TextFileFormat` (`qiime2.plugin.TextFileFormat`) is for creating text-based formats (e.g. FASTQ, TSV, etc.).
An example of one of these formats is the [`DNAFASTAFormat`](https://github.com/qiime2/q2-types/blob/e25f9355958755343977e037bbe39110cfb56a63/q2_types/feature_data/_format.py#L147), used for storing FASTA data.


### Binary File Formats

The `BinaryFileFormat` (`qiime2.plugin.BinaryFileFormat`) is for creating binary formats (e.g. BIOM, gzip, etc.).
An example of one of these formats is the [`FastqGzFormat`](https://github.com/qiime2/q2-types/blob/e25f9355958755343977e037bbe39110cfb56a63/q2_types/per_sample_sequences/_format.py#L236), a format for storing gzipped FASTQ files.

## Directory Formats

While many formats can accurately be described using a single file, many formats exist that require the presence of more than one file present together as a set.
QIIME 2 allows more than one `FileFormat` to be combined together as a `DirectoryFormat` (`qiime2.plugin.DirectoryFormat`).

### Fixed Layouts

Some directory layouts can be accurately described with a fixed number of members.
An example of this is the [`EMPPairedEndDirFmt`](https://github.com/qiime2/q2-demux/blob/6e9a0cc8841a9cfbb5f517a256872700c7b75732/q2_demux/_format.py#L28).
This directory format is always composed of three [`FastqGzFormat`](https://github.com/qiime2/q2-types/blob/e25f9355958755343977e037bbe39110cfb56a63/q2_types/per_sample_sequences/_format.py#L236) files: one for the forward reads (`forward.fastq.gz`), one for the reverse reads (`reverse.fastq.gz`), and one for the barcodes (`barcodes.fastq.gz`).
The underlying `FastqGzFormat` is defined once --- it doesn't need to know about the sematic difference between biological reads and barcode reads, unlike the `EMPPairedEndDirFmt` which must be able to differentiate these.

```python
   class EMPPairedEndDirFmt(model.DirectoryFormat):
       forward = model.File(r'forward.fastq.gz', format=FastqGzFormat)
       reverse = model.File(r'reverse.fastq.gz', format=FastqGzFormat)
       barcodes = model.File(r'barcodes.fastq.gz', format=FastqGzFormat)
```

The component files of this `DirectoryFormat` are defined using the `File` (`qiime2.plugin.model.File`) class.

### Variable Layouts

While some layouts are accurately described with a fixed set of members, others are highly variable, preventing formats from accurately knowing how many files to expect in its {term}`payload`.
An example of this kind of format are any of the demultiplexed file formats --- when sequences are demultiplexed there is one (or two) files per sample, but how many samples are there?
One study might have 5 samples, while another has 5000.
For these situations the `DirectoryFormat` (`qiime2.plugin.DirectoryFormat`) can be configured to watch for set pattern of filenames present in its {term}`payload`.
An example of this is the [`CasavaOneEightSingleLanePerSampleDirFmt`](https://github.com/qiime2/q2-types/blob/e25f9355958755343977e037bbe39110cfb56a63/q2_types/per_sample_sequences/_format.py#L292) class, which stores demultiplexed sequence data in files named with a pattern used by Illumina's Casava v1.8 software.

```python
class CasavaOneEightSingleLanePerSampleDirFmt(model.DirectoryFormat):
    sequences = model.FileCollection(
        r'.+_.+_L[0-9][0-9][0-9]_R[12]_001\.fastq\.gz',
        format=FastqGzFormat)

    @sequences.set_path_maker
    def sequences_path_maker(self, sample_id, barcode_id, lane_number,
                            read_number):
        return '%s_%s_L%03d_R%d_001.fastq.gz' % (sample_id, barcode_id,
                                                lane_number, read_number)
```

## Single File Directory Formats
Currently QIIME 2 requires that all formats registered to an {term}`artifact class` be a directory format.
For those cases, there exists a factory for quickly constructing directory layouts that contain *only a single file*.
This requirement might be removed in the future, but for now it is a necessary evil (and also isn't too much extra work for format developers).

```python
DNASequencesDirectoryFormat = model.SingleFileDirectoryFormat(
    'DNASequencesDirectoryFormat', 'dna-sequences.fasta', DNAFASTAFormat)
```

## Associating Formats with a Type

Formats on their own aren't of much use.
It is only once they are associated with a {term}`semantic type` to define an *artifact class* that things become interesting.
Artifact classes define the data that can be provided as input or generated as output by QIIME 2 `Actions`.
An example of this can be seen in the [registration of the `SampleData[PairedEndSequencesWithQuality]` artifact class](https://github.com/qiime2/q2-types/blob/e25f9355958755343977e037bbe39110cfb56a63/q2_types/per_sample_sequences/_type.py#L66).
