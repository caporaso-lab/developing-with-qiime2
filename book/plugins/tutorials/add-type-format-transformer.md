(plugin-tutorial-add-type-format-transformer)=
# Adding a type, format, and transfomer

Now that we've built a basic method and a basic visualizer, let's step into some of the other unique aspects of developing with QIIME 2: defining semantic types, formats, and transformers.
For most of the new QIIME 2 developers who I've worked with, this is the most obscure step.
However it's what gives QIIME 2 a lot of its power (for example, its ability to be accessed through different interfaces and to help users avoid analytic errors) and flexibility (for example, its ability to load the same artifact into different data types, depending on what you want to do with it).