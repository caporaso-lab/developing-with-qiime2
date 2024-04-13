# Add a first visualizer

In the last section we created a first method for our plugin which performed pairwise alignment of DNA sequences.
We were able to run this to generate an alignment, but we didn't have any way to visualize the result without exporting it from QIIME 2.
In this lesson we'll address that by adding a simple {term}`Visualizer` to our plugin which takes a `TabularMSA` artifact as input (which is what our previous action generated as output), and generates a `Visualization` that we can review using [QIIME 2 View](https://view.qiime2.org).

(add-alignment-visualizer-commit)=
```{admonition} tl;dr
:class: tip
The complete code that I developed to add this visualizer to my plugin can be found [here](https://github.com/caporaso-lab/q2-dwq2/commit/1e802ea841ef40a40cfcdf53fca124061fcfccad).
```

## Write the visualizer function

As with adding our alignment method, the first thing we'll do to define a new visualizer is write the underlying Python function.
Visualizer functions, at a minimum, take an `output_dir` (directory where output files should be written) as a string as input, but they also generally take one or more QIIME 2 artifacts, as well as metadata, as input.
Our action will take the sequence alignment artifact that we generated as input, in addition to the `output_dir` parameter.

The main function of a visualizer is to write some content to `output_dir`.
This information will all be packaged as part of the output {term}`Visualization` that QIIME 2 creates when the visualizer is called.
When the visualization is viewed by a user using a QIIME 2 result viewer (such as [QIIME 2 View](https://view.qiime2.org)), the viewer looks for an `index` file in the directory content created by the visualization, and presents that through the viewer.
Most often, the `index` file is an HTML file (`index.html`), though technically other file types are possible.
Visualizers are intentionally very flexible.
As long as content can be packaged as HTML content and doesn't require a server, it should work ok in the visualizer.

Our task in writing this visualizer is to create some sort of useful, human-readable display of the alignment that is provided as input in an HTML file.
Luckily, scikit-bio's `TabularMSA` object has a built-in function for creating a text-based human-readable alignment summary through its `__repr__` function.
We'll use that here, even though the representation it creates is a little crude and it is only a summary rather than a display of the full alignment.
(Since our goal here is just to write a vizualizer --- not actually enable exploration of alignments --- this will suffice for our purposes.
I'll leave it as an exercise to you at the end of this section to expand on this visualization.)

Start by creating a new file, `_visualizers.py` in your module's top-level directory. For me, this file will be `q2-dwq2/q2_dwq2/_visualizers.py`. Add the following code to that file.

```python
import os.path

from skbio.alignment import TabularMSA


def summarize_alignment(output_dir: str, msa: TabularMSA) -> None:
    with open(os.path.join(output_dir, "index.html"), "w") as fh:
        fh.write(_html_template % repr(msa))


_html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Alignment summary</title>
    <style>
        body {
            padding: 20px;
        }
        p.alignment {
            font-family: 'Courier New', Courier, monospace;
        }
    </style>
</head>
<body>
    <pre>
%s
    </pre>
</body>
</html>
"""
```

The majority of the code in this file is the `_html_template` variable, which sets up the HTML file and leaves a format specifier (`%s`) for us to insert a string of text.
As templates like this get bigger or more complex, it often makes sense to store them in other files that are loaded by your visualizer code, but we'll keep the template in the same file for now to keep it simple.

The other bit of code in here is our viusalizer function.
As described above, this takes an `output_dir` (always the first parameter to a visualizer) and our multiple sequence alignment as input, and doesn't `return` anything.
As with all Python functions that get registered as plugin actions, our function employs type hints so that QIIME 2 knows what data type should be provided as input for each parameter.
In our case, `output_dir` is provided as a string (`str`), `msa` is provided as a `skbio.alignment.TabularMSA`, and the return type is `None`, indicating no return value.

Our visualizer code is short and sweet.
It opens a new file, `index.html` in `output_dir`.
It then writes the html template to file, replacing the format specifier in the template with the `__repr__` of our `msa`.

That's it for the underlying visualizer function.
Let's write a quick test of it before we hook it up to the plugin, to verify that the function works as expected.

## Unit testing the visualizer function

I wrote my test of this visualizer in a new file, `q2-dwq2/q2_dwq2/tests/test_visualizers.py`.
Create a file for your test in your plugin, and add the following content.

```python
import os.path

from skbio.alignment import TabularMSA
from skbio.sequence import DNA

from qiime2.plugin.testing import TestPluginBase

from q2_dwq2._visualizers import summarize_alignment


class SummarizeAlignmentTests(TestPluginBase):
    package = 'q2_dwq2.tests'

    def test_simple1(self):
        aligned_sequence1 = DNA('AAAAAAAAGGTGGCCTTTTTTTT')
        aligned_sequence2 = DNA('AAAAAAAAGG-GGCCTTTTTTTT')
        msa = TabularMSA([aligned_sequence1, aligned_sequence2])

        with self.temp_dir as output_dir:
            summarize_alignment(output_dir, msa)

            with open(os.path.join(output_dir, 'index.html'), 'r') as fh:
                observed = fh.read()

            self.assertIn('AAAAAAAAGGTGGCCTTTTTTTT', observed)
            self.assertIn('AAAAAAAAGG-GGCCTTTTTTTT', observed)

```

Our test again uses `qiime2.plugin.testing.TestPluginBase`, which is good practice for all tests of your QIIME 2 plugin functions as it provides some convenient functionality.
We then create a `TabularMSA`, similar to how we created our `expected` values in our `nw_align` tests in the previous section.
Then, we use `TestPluginBase`'s `temp_dir` property as an output directory, and call our `summarize_alignment` function providing the `output_dir` and the alignment as input.

Determining what to test with a visualizer is always a little tricker, as we don't want to make the test more fragile than it needs to be.
In this case, we do know what the entire HTML file is supposed to look like, so we could compare that as our `expected` to the `observed` value character by character and fail if any characters differ.
That could get a bit clunky though, as a lot of that test would just be ensuring that Python correctly wrote a string (our `_html_template`) variable to file, and any changes to our `_html_template` would require changes to the test code as well.
Instead, I'm just going to test that the expected aligned sequence strings were correctly written to file.
I do that using `assertIn`, which in this case is checking that a given string is `in` another given string (i.e., the first string is a substring of the second string).

Save this file, and run the tests using:

```shell
make test
```

This will generate a bunch of output, but if everything is working as expected you should see a line like:

```shell
q2_dwq2/tests/test_visualizers.py .
```

in the output. This indicates that one test ran and passed (indicated by the single `.` character - you'll have one `.` per test that passed) from the `q2_dwq2/tests/test_visualizers.py` file.

If the test didn't pass, take a few minutes to figure out what went wrong, and re-run the test until it passes.

If you get stuck, refer to [the code that I wrote for this section](add-alignment-visualizer-commit).

## Register your Python function as a plugin action

The last step in defining a visualizer for your plugin is to register the function we just wrote as a visualizer.
To do this, we'll go back to the `plugin_setup.py` file.

In that file, you'll first need to import your visualizer function so you can register it by adding the following line to the top of the file:

```python
from q2_dwq2._visualizers import summarize_alignment
```

Then, you'll call `plugin.visualizers.register_function`, as follows:

```python
plugin.visualizers.register_function(
    function=summarize_alignment,
    inputs={'msa': FeatureData[AlignedSequence]},
    input_descriptions={'msa': 'The multiple sequence alignment to summarize.'},
    parameters={},
    parameter_descriptions={},
    name='Summarize an alignment.',
    description='Summarize a multiple sequence alignment.',
)
```

This is very similar to how we registered our `nw_align` function, except that because this is a `visualizer`, we're calling `plugin.`**`visualizers`**`.register_function`, rather than `plugin.`**`methods`**`.register_function`.
We still provide the `function` we want to register, `inputs` and `input_descriptions`, `parameters` and `parameter_descriptions`, a `name`, a `description`, and `citations` if we had any (but we don't here).

If you now save this file, and call `qiime dev refresh-cache`, you should be able to see and use your visualizer.
Try out your new visualizer by providing one of the `FeatureData[AlignedSequence]` artifacts that you generated as output from calling your `nw-align` action.
To see what it looks like, load the visualizer with [QIIME 2 View](https://view.qiime2.org).
You should see something like this at QIIME 2 View:

```
TabularMSA[DNA]
-------------------------
Stats:
sequence count: 2
position count: 25
-------------------------
ACCGGTGGAACCGG-TAACACCCAC
ACCGGT--AACCGGTTAACACCCAC
```

While you're there, also take a minute to review the Provenance of your visualizer using the *Provenance* tab on that page.

## An optional exercise

As mentioned above, our visualizer is a little crude and if you try to summarize long alignments (longer than 80 positions) you won't see the full alignment.
Spend some time making it look a little nicer, and maybe even expanding this to see the full alignment for longer alignments.
For example, color the different nucleotide characters differently, or use colors or other formatting to indicate where there are matches, mismatches, and gaps in the alignment.
You don't have to use the `repr` function - you can access other parts of the `TabularMSA` API to display whatever information you'd like.



