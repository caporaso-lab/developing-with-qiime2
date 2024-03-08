(formats-explanation)=
# File Formats and Directory Formats

```{eval-rst}

:term:`Formats <Format>` are on-disk representations of :term:`semantic types
<Semantic Type>`, and are the materialized ``data/`` saved in the
:term:`payload <Payload>` by the :term:`framework <Framework>` when reading and
writing :term:`artifacts <Artifact>`.

QIIME 2 doesn't have much of an opinion on how data should be represented or
stored, so long as it *can* be represented or stored in an :term:`archive`.

File Formats
------------

The simplest ``Formats`` are the :class:`TextFileFormat
<qiime2.plugin.TextFileFormat>` and the :class:`BinaryFileFormat
<qiime2.plugin.BinaryFileFormat>`. These formats represent a single file with a
fixed on-disk representation.

Validation
..........

Both types of ``FileFormat`` support validation hooks --- this is (typically) a
small bit of code that is run when initially loading a file from an
:term:`archive` - it allows the framework to ensure that the the data contained
within the :term:`archive` at least *looks* like its declared :term:`type`.
This works very well for on-the-fly loading and saving, and goes a long way to
preventing corrupt or invalid data from persisting. The one "gotcha" here is
that in order to keep things quick, we typically recommend that "minimal"
validation occurs over a limited subset of the file (e.g. the first 10 records
in a FASTQ file). Because of this, formats allow for multiple levels of
sniffing to be defined (currently there are two levels, ``min`` and ``max``).

.. code-block:: python

   class IntSequenceFormat(TextFileFormat):
       """
       A sequence of integers stored on new lines in a file. Since this is a
       sequence, the integers have an order and repetition of elements is
       allowed. Sequential values must have an inter-value distance other than
       3 to be valid.
       """
       def _validate_n_ints(self, n):
           with self.open() as fh:
               last_val = None
               for idx, line in enumerate(fh, 1):
                   if n is not None and idx >= n:
                       break
                   try:
                       val = int(line.rstrip('\n'))
                   except (TypeError, ValueError):
                       raise ValidationError("Line %d is not an integer." % idx)
                   if last_val is not None and last_val + 3 == val:
                       raise ValidationError("Line %d is 3 more than line %d"
                                             % (idx, idx-1))
                   last_val = val

       # The hook is ``_validate_``, but the public method exposed by the
       # Framework is ``validate``.
       def _validate_(self, level):
           record_map = {'min': 5, 'max': None}
           self._validate_n_ints(record_map[level])

   format_instance = IntSequenceFormat(temp_dir.name, mode='r')
   format_instance.validate()  # Shouldn't error!

In the fictional format example above, when ``validate`` is called with
``level='min'``, the ``_validate_`` hook will check the first 5 records,
otherwise, when ``level='max'``, it will check the entire file.

Astute observers might notice that the method defined in the
``IntSequenceFormat`` is called ``_validate_``, but the method called on the
``format_instance`` was ``validate`` --- this is because defining format
validation is optional (although highly recommended!).  Every format has a
``validate`` method available to interfaces (for performing ad-hoc validation),
the framework will check for the presence of a ``_validate_`` method on the
format in question, and will include that method as part of more general
validations that the framework will perform. The aim here is that the framework
is capable of ensuring common basic patterns, like presence of required files,
while the ``_validate_`` method is the place for the format developer to
declare any special "business" logic necessary for ensuring the validity of
their format.

Text File Formats
.................

The :class:`TextFileFormat <qiime2.plugin.TextFileFormat>` is for creating
text-based formats (e.g. FASTQ, TSV, etc.). An example of one of these formats
is the |DNAFASTAFormat|_, used for storing FASTA data.

.. note:: This format defines a ``sniff`` hook, instead of ``_validate_`` -
   this is a now-deprecated form of validation that is being replaced with the
   multi-level validation supported with ``_validate_``.

Binary File Formats
...................

The :class:`BinaryFileFormat <qiime2.plugin.BinaryFileFormat>` is for creating
binary formats (e.g. BIOM, gzip, etc.). An example of one of these formats is
the |FastqGzFormat|_, the format for gzipped FASTQ files.

Directory Formats
-----------------

While many formats can accurately be described using a single file, many
formats exist that require the presence of more than one file present together
as a set.  QIIME 2 allows more than one ``FileFormat`` to be combined together
as a :class:`DirectoryFormat <qiime2.plugin.DirectoryFormat>`. The exciting
thing about this is that all of the sniffing, validation, and type-safety of
the individual file formats is multiplied by however many members are expected
to be present within the :class:`DirectoryFormat
<qiime2.plugin.DirectoryFormat>`!

Fixed Layouts
..............

Some directory layouts can be accurately described with a fixed number of
members. An example of this is the |EMPPairedEndDirFmt|_ --- this directory
format should always be composed of three |FastqGzFormat|_ files --- one for
the forward reads, one for the reverse reads, and one for the barcodes.  The
|FastqGzFormat|_ is defined once (the format doesn't need to know about the
sematic difference between biological reads and barcode reads).

.. code-block:: python

   class EMPPairedEndDirFmt(model.DirectoryFormat):
       forward = model.File(r'forward.fastq.gz', format=FastqGzFormat)
       reverse = model.File(r'reverse.fastq.gz', format=FastqGzFormat)
       barcodes = model.File(r'barcodes.fastq.gz', format=FastqGzFormat)

The individual members are defined using the :class:`File
<qiime2.plugin.model.File>` class.

Variable Layouts
................

While some layouts are accurately described with a fixed set of members, others
are highly variable, preventing formats from accurately knowing how many files
to expect in its :term:`payload`. An example of this kind of format are any of
the demultiplexed file formats --- when sequences are demultiplexed there is
one (or two) files per sample, but how many samples are there? One study might
have 5 samples, while another has 5000. For these situations the
:class:`DirectoryFormat <qiime2.plugin.DirectoryFormat>` can be configured to
watch for set pattern of filenames present in its :term:`payload`.

.. code-block:: python

   class CasavaOneEightSingleLanePerSampleDirFmt(model.DirectoryFormat):
       sequences = model.FileCollection(
           r'.+_.+_L[0-9][0-9][0-9]_R[12]_001\.fastq\.gz',
           format=FastqGzFormat)

       @sequences.set_path_maker
       def sequences_path_maker(self, sample_id, barcode_id, lane_number,
                                read_number):
           return '%s_%s_L%03d_R%d_001.fastq.gz' % (sample_id, barcode_id,
                                                    lane_number, read_number)

Single File Directory Formats
.............................

Currently QIIME 2 requires that all formats registered to a :term:`Semantic
Type` be a directory format, which would be a major pain in the case of the
single file formats detailed above. For those cases, there exists a factory for
quickly constructing directory layouts that contain *only a single file*. This
requirement might be removed in the future, but for now it is a necessary evil
(and also isn't too much extra work for format developers).

.. code-block:: python

   DNASequencesDirectoryFormat = model.SingleFileDirectoryFormat(
       'DNASequencesDirectoryFormat', 'dna-sequences.fasta', DNAFASTAFormat)

Associating Formats with a Type
-------------------------------

Formats on their own aren't of much use - it is only once they are registered
as a *representation* of a :term:`Semantic Type` that things become
interesting.

.. code-block:: python

   plugin.register_formats(EMPPairedEndDirFmt)
   # ``RawSequences`` is a Semantic Type
   plugin.register_semantic_types(RawSequences, EMPPairedEndSequences)

.. |DNAFASTAFormat| replace:: ``DNAFASTAFormat``
.. _`DNAFASTAFormat`: https://github.com/qiime2/q2-types/blob/master/q2_types/feature_data/_format.py#L133
.. |FastqGzFormat| replace:: ``FastqGzFormat``
.. _`FastqGzFormat`: https://github.com/qiime2/q2-types/blob/master/q2_types/per_sample_sequences/_format.py#L106
.. |EMPPairedEndDirFmt| replace:: ``EMPPairedEndDirFmt``
.. _`EMPPairedEndDirFmt`: https://github.com/qiime2/q2-demux/blob/master/q2_demux/_format.py
```