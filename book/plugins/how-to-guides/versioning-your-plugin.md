# Define version numbers for your plugin

Once you are ready to create a formal 'released' version of your plugin for your users, you'll want to think about the versioning structure you'll use.
It's helpful to use a consistent structure for the released versions of your plugins, so users have an idea of what version they should install based on when the release occurred and/or what features they want to utilize.
There are two different versioning structures we recommend using for your plugin, each discussed below.

## Semantic Versioning

Semantic versioning has the general structure of `X.Y.Z` with `X`, `Y` and `Z` each being non-negative integers that don't contain any leading zeros.
An example of this could look like `1.1.0`.
`X` refers to the major version, `Y` is the minor version, and `Z` is the patch version (if applicable).
Each of these elements must increase numerically (i.e. `1.1.0` -> `1.2.0` -> `1.3.0`).
A major version is defined as a version that contains backwards incompatible changes (i.e. a 'breaking' change), while minor versions can contain any number of new features and/or bug fixes that don't contain any breaking changes.
A patch version should only be utilized if backwards incompatible bug fixes are introduced.

Here's a full example of what a few releases could look like under this structure:

- `Version 1.0.0` - your very first release (congrats!)
- `Version 1.1.0` - you've added some new features, but are still backwards compatible with 1.0.0
- `Version 1.1.1` - you discovered a bug that needed to be fixed that renders this version incompatible with 1.1.0 (which is okay, because this fixed incorrect behavior in that version)
- `Version 2.0.0` - you've added a couple of new breaking changes that aren't compatible with versions `1.*.*`

More information on the Semantic Versioning Specification can be found [here](https://semver.org).

## Date-Based Versioning

In the QIIME 2 Ecosystem, we have opted for date-based versioning rather than Semantic Versioning.
Our reasoning behind this decision was to reduce confusion from each individual plugin having separate releases and determining which ones were compatible with each other for a particular version.
Using date-based versioning simplifies release versions for larger collections of plugins because this is all based upon when the release occurred, rather than whether it contained a particular change set.
For the purposes of developing an individual plugin, there isn't one way that's particularly better than another, so this should be left to your preference.
If you're interested in date-based versioning, the structure is `YYYY.MM.PP` with `YYYY` and `MM` representing year and month of the release date, respectively, and `PP` representing the patch version (if applicable).

Here's an example of what a few releases could look like under this structure:

- `Version 2025.4.0` - April 2025 release
- `Version 2025.4.1` - patch release succeeding the April 2025 release for an emergency bug fix
- `Version 2025.10.0` - October 2025 release

## Versioning with git and Github

Regardless of the versioning structure you choose, you'll either need to utilize Github Releases to attach a version to a particular snapshot in time of your repository, or you'll need to create your own annotated tags with git.

More information on creating a release on Github can be found under [](release-on-gh).

If for whatever reason you choose not to utilize Github Releases, you can also create a new versioned release by creating an annotated git tag that points to the relevant commit (either the HEAD of your main branch, or a particular release branch that you've created for this purpose).

Here's an example of what creating an annotated git tag could look like for a release:

```
git tag -a 2025.4 -m "REL: 2025.4"
git push upstream --tags
```

More information on utilizing annotated tags via the git command line can be found [here](https://git-scm.com/book/en/v2/Git-Basics-Tagging).
