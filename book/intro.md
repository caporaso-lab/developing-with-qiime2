# *Developing with QIIME 2*

**Your guide for writing, testing, and distributing QIIME 2 plugins, interfaces, and documentation.**

```{note}
*Developing with QIIME 2* remains in [very active development](https://github.com/caporaso-lab/developing-with-qiime2/commits/main/) between March and April of 2024.
It should be getting more complete by the day. 🚀

As of 13 March 2024, most of the content from the [old QIIME 2 Developer Documentation](https://dev.qiime2.org) has been transitioned to *Developing with QIIME 2*.
This book will be replacing the content at https://dev.qiime2.org shortly, and URLs are subject to change.

The [](plugin-tutorial-intro) chapter is where the focus is at the moment, and it'll stay there for the near future, though all of the [](plugins/intro.md) chapters have useful and up-to-date content in them.
You'll also find content in [](framework-explanations) and various other chapters throughout, but those are currently less thorough and generally need some updates.
Please [let us know](https://github.com/caporaso-lab/developing-with-qiime2/issues) if you find anything that is inaccurate or outdated.
```

**D**eveloping **w**ith **Q**IIME **2** (DWQ2) is split into multiple *Parts* covering topics in QIIME 2 development, including [](plugin-intro), [](interface-intro), and [](documentation-intro).
You do not need to read all of these parts to develop with QIIME 2.
If you are interested in creating plugins, then the only part you need to concern yourself with is [](plugin-intro).
Similarly, if you want to build an interface, you only need [](interface-intro).
Other parts, such as [](framework-intro) and [](ci-intro), are currently targeted primarily for the development team in the [Caporaso Lab](https://cap-lab.bio).
[](documentation-intro) is slated for a full re-write as we [adapt our approach to user documentation](users-docs-refactor).

The content in each part of this book is organized under the [Diátaxis](https://diataxis.fr/) framework {cite}`diataxis`.
This means that you can expect *Chapters* containing *Tutorials*, *How-To-Guides*, *Explanations*, and *References* in each part.
Each serves a different goal for the reader:

```{list-table}
:header-rows: 1

* - Chapter
  - Purpose

* - Tutorial
  - Provides a guided exploration of a topic for **learning**.

* - How To Guide
  - Provides step-by-step instructions on how to accomplish specific **goals**.

* - Explanation
  - Provides a discussion intended to aid in **understanding** a specific topic.

* - Reference
  - Provide specific **information** (e.g., an API reference).
```

Chapters are generally broken up into *Sections*.
For example, the [](plugin-tutorial-intro) chapter works through building a new QIIME 2 plugin from scratch.
It does this in a series of sections that focus on different plugin components.

## Getting Help
For the most up-to-date information on how to get help with QIIME 2, as a user or developer, see [here](https://github.com/qiime2/.github/blob/main/SUPPORT.md).

## Contributing
To get information on contributing to *Developing with QIIME 2*, see [](contributing-to-dwq2).

