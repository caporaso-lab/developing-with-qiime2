# *Developing with QIIME 2*

**Your guide for writing, testing, and distributing QIIME 2 plugins, interfaces, and documentation.**

```{admonition} Setting up your development environment
:class: tip, dropdown
If you just want to find instructions for creating your QIIME 2 development environment, see [](setup-dev-environment).
```

```{admonition} Development status of this content
:class: note
*Developing with QIIME 2* remains in [active development](https://github.com/caporaso-lab/developing-with-qiime2/commits/main/), and as a result some URLs may change.
It should be getting more complete by the day. 🚀

The canonical URL for this project is now https://develop.qiime2.org. [^old-docs]

The [](plugin-tutorial-intro) chapter is where the focus is for the near future, though all of the [](plugins/intro.md) chapters have useful and up-to-date content in them.
You'll also find content in [](framework-explanations) and various other chapters throughout, but those are currently less thorough and generally need some updates.
Please [let us know](https://github.com/caporaso-lab/developing-with-qiime2/issues) if you find anything that is inaccurate or outdated.
```

**D**eveloping **w**ith **Q**IIME **2** (DWQ2) is split into multiple *Parts* covering topics in QIIME 2 development, including [](plugin-intro), [](interface-intro), and [](documentation-intro).
You do not need to read all of these parts to develop with QIIME 2.
If you are interested in creating plugins, then the only part you need to concern yourself with is [](plugin-intro).
Similarly, if you want to build an interface, you only need [](interface-intro).
Other parts, such as [](framework-intro) and [](ci-intro), are currently targeted primarily for the development team in the [Caporaso Lab](https://cap-lab.bio).
[](documentation-intro) isn't really written yet, but you will find relevant and up-to-date (as of 2 July 2025) information here if you're interested in writing documentation for developers or users of QIIME 2.


The content in each part of this book is organized under the {{ diataxis }} framework.
This means that you can expect *Chapters* containing *Tutorials*, *How-To-Guides*, *Explanations*, and *References* in each part.
Each serves a different goal for the reader:

```{list-table}
:header-rows: 1

* - Chapter
  - Purpose

* - Tutorials
  - Provide a guided exploration of a topic for **learning**.

* - How To Guides
  - Provide step-by-step instructions on how to **accomplish specific goals**.

* - Explanations
  - Provide a discussion intended to aid in **understanding** a specific topic.

* - References
  - Provide specific **information** (e.g., an API reference).
```

Chapters are generally broken up into *Sections*.
For example, the [](plugin-tutorial-intro) chapter works through building a new QIIME 2 plugin from scratch.
It does this in a series of sections that focus on different plugin components.

(acknowledgements)=
## Acknowledgements
[The authors](contributing-to-dwq2) would like to thank [those who have contributed](https://github.com/caporaso-lab/developing-with-qiime2/graphs/contributors) to the writing of *Developing with QIIME 2*.

The template plugin used in [](plugin-tutorial-intro) was derived from [@misialq's plugin template](https://github.com/bokulich-lab/q2-plugin-template).

## Getting Help
For the most up-to-date information on how to get help with QIIME 2, as a user or developer, see [here](https://github.com/qiime2/.github/blob/main/SUPPORT.md).

## Contributing
To get information on contributing to *Developing with QIIME 2*, see [](contributing-to-dwq2).

## Funding

This work was funded in part by NIH National Cancer Institute Informatics Technology for Cancer Research grant [1U24CA248454-01](https://reporter.nih.gov/project-details/9951750), and by grant [DAF2019-207342](https://doi.org/10.37921/862772dbrrej) from the Chan Zuckerberg Initiative (CZI) DAF, an advised fund of Silicon Valley Community Foundation (CZI grant DOI: 10.37921/862772dbrrej; funder DOI 10.13039/100014989).

This book is built with MyST Markdown and Jupyter Book, which are supported in part with [funding](https://sloan.org/grant-detail/6620) from the Alfred P. Sloan Foundation.

Initial support for the development of QIIME 2 was provided through a [grant](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1565100) from the National Science Foundation.

## License

<p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/caporaso-lab/developing-with-qiime2/">Developing with QIIME 2 (DWQ2)</a> by <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://cap-lab.bio">Greg Caporaso and Evan Bolyen</a> is made available under the <a href="https://creativecommons.org/licenses/by-nc-nd/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">CC BY-NC-ND 4.0 license<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1" alt=""><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1" alt=""><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/nc.svg?ref=chooser-v1" alt=""><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/nd.svg?ref=chooser-v1" alt=""></a>.</p>

The QIIME 2 plugin [cookiecutter template](https://github.com/caporaso-lab/cookiecutter-qiime2-plugin) is made available under the BSD 3-Clause license.
Unlike DWQ2, derivative works of that template *are* allowed (i.e., you can build real plugins that you intend to distribute for any purpose, including commercial, from the template).

[^old-docs]: The "old developer documentation", which was previously hosted at `https://dev.qiime2.org`, is now deprecated.
 All content that is still relevant has been ported from that documentation to *Developing with QIIME 2*.
 If you want to access that archival content, you can find it in the [project's GitHub repository](https://github.com/qiime2/dev-docs).
