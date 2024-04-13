(plugin-tutorial-add-2nd-transformer)=
# Add a second transformer

A couple of sections back (in [](plugin-tutorial-add-artifact-class)), I noted that adding transformers was an obscure step for a lot of new plugin developers.
Let's circle back to that now with the goal of developing a better understanding of the role of transformers in QIIME 2, and also to simplify the code for generating usage examples that we just wrote.

Take a minute to review the helper function we defined in our `_examples.py` file, and try to describe in a sentence or two what that code is doing.
Here it is again, for reference:

```python
def _create_seq_artifact(seq: skbio.DNA):
    ff = SingleRecordDNAFASTAFormat()
    seq.write(str(ff.path))
    return qiime2.Artifact.import_data("SingleDNASequence", ff)
```

```{dropdown} Here's my description of what this is doing, but come up with your own before looking at this.

This code is transforming (or converting) an `skbio.DNA` object into a `q2_dwq2.SingleRecordDNAFASTAFormat` object, and then importing that format into a QIIME 2 artifact.
```

Transformers in QIIME 2 are designed to handle converstions between objects behind the scenes, so that users don't ever have to think about this, and developers can think about it as infrequently as possible.
In this section, we'll do a small refactor of the code we wrote in the previous section.

```{admonition} tl;dr
The code that I wrote for this section can be found [here](https://github.com/caporaso-lab/q2-dwq2/commit/93a3098b4e18796e8c33cd35088bf2a3623eed20).
```

## Define a transformer from `skbio.DNA` to `q2_dwq2.SingleRecordDNAFASTAFormat`

The first transformer that we wrote transforms our `q2_dwq2.SingleRecordDNAFASTAFormat` object to an `skbio.DNA` object, so that we can view artifacts of class `SingleDNASequence` as `skbio.DNA` objects when we work with them.
As a developer, `skbio.DNA` objects are easier to create and use than `q2_dwq2.SingleRecordDNAFASTAFormat` objects, because they have convenient APIs.
Once we have a helper function for creating `q2_dwq2.SingleRecordDNAFASTAFormat` objects from `skbio.DNA` objects, like the `_create_seq_artifact` function we wrote, `q2_dwq2.SingleRecordDNAFASTAFormat` objects are also trivial to create, but it still tends to be more convenient to create and use those via an `skbio.DNA` object since we then don't have to directly deal with reading and writing files.
QIIME 2 enables us to define and register functions that convert between object types as transformers, making them universally accessible in deployments where the plugin that defines and registers them is installed.

We can adapt the code from our `_create_seq_artifact` function into a new transformer in our `_transformers.py` file as follows:

```python
@plugin.register_transformer
def _2(seq: DNA) -> SingleRecordDNAFASTAFormat:
    ff = SingleRecordDNAFASTAFormat()
    seq.write(str(ff.path))
    return ff
```

If you don't recall exactly what this is doing, review [the text that described this when we defined `_create_seq_artifact`](_create_seq_artifact_helper_function).
The only difference here is that we're returning the `SingleRecordDNAFASTAFormat`, where in `_create_seq_artifact` we imported this into a `qiime2.Aritfact` as well.

This new transformer enables us to adapt our factory functions in `_examples.py` to look like the following:

```python
def seq1_factory():
    seq = skbio.DNA("AACCGGTTGGCCAA", metadata={"id": "seq1"})
    return qiime2.Artifact.import_data(
        "SingleDNASequence", seq, view_type=skbio.DNA)


def seq2_factory():
    seq = skbio.DNA("AACCGCTGGCGAA", metadata={"id": "seq2"})
    return qiime2.Artifact.import_data(
        "SingleDNASequence", seq, view_type=skbio.DNA)
```

With this code, we're still importing to a `SingleDNASequence` artifact class, but this time we're doing it directly from an `skbio.DNA` view type.
Under the hood, QIIME 2 checks to see if any transfomers are registered that transform a `skbio.DNA` to a `skbio.SingleRecordDNAFASTADirectoryFormat` (the format we [associated with our artifact class](register-artifact-class)).
It finds a transformer from `skbio.DNA` to `skbio.SingleRecordDNAFASTAFormat`, and a transformer from `skbio.SingleRecordDNAFASTAFormat` to `skbio.SingleRecordDNAFASTADirectoryFormat`, so it applies that chain of transformers to import into the `SingleDNASequence` artifact class with the `skbio.DNA` object that we provided.
Cool! 😎

At this point, we can delete the `_create_seq_artifact` function from `_examples.py` as we have centralized the functionality for performing the transformation that it did, and we moved the import step into the factories.

## Add unit tests of the new transfomer

As always, before this new code is ready for use, we need to write some unit tests.
Here are the tests that I wrote in `test_transformers.py`:

```python
    def test_DNA_to_single_record_fasta_simple1(self):
        in_ = DNA('ACCGGTGGAACCGGTAACACCCAC',
                  metadata={'id': 'example-sequence-1', 'description': ''})
        tx = self.get_transformer(DNA, SingleRecordDNAFASTAFormat)

        observed = tx(in_)
        # confirm "round-trip" of DNA -> SingleRecordDNAFASTAFormat -> DNA
        # results in an observed sequence that is the same as the starting
        # sequence
        self.assertEqual(observed.view(DNA), in_)

    def test_DNA_to_single_record_fasta_simple2(self):
        in_ = DNA('ACCGGTAACCGGTTAACACCCAC',
                  metadata={'id': 'example-sequence-2', 'description': ''})
        tx = self.get_transformer(DNA, SingleRecordDNAFASTAFormat)

        observed = tx(in_)
        self.assertEqual(observed.view(DNA), in_)
```

Review those to make sure that you understand them, and then copy/paste those into your plugin or write your own.
Run `make test` to confirm that everything is working as expected.

