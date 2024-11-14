# QIIME 2 Development and Release Cycle Structure

In the sections below, we will go through the development cycle structure and release process for QIIME 2.
The aim is to provide insight into our structure for other research software engineering teams that may want to utilize any/all of these processes, as well as to assist our community developers in knowing what timeline/deadlines they should be aware of within each development/release cycle.
If you have any questions on this process, please don't hesitate to reach out on our user forum under the [Developer Discussion](https://forum.qiime2.org/c/dev-discussion) category!

## QIIME 2 Release Cycle Structure

As of 2024.10, QIIME 2 Distributions are released bi-anually, on the first Wednesday of April and October.
This schedule provides us with ample development time between releases, and provides our developer community with at least a three month notice for any external dependency changes (i.e. bumping Python, removing a deprecated package, etc).

The following diagram outlines relevant timepoints between each release, with terms defined below.

```{figure} ../images/q2-dev-cycle-diagram.png
:align: center
:width: 300
```


- `20XX.REL`: The most current, released version of QIIME 2.
- `20XX.REL+1`: The upcoming release version for QIIME 2.
- `'Approved but Unscheduled' Project Board`: One of the QIIME 2 Github Project Boards, used to store issues/pull requests that we think are good ideas, but don't have the immediate bandwidth to address.
- `External dependency version changes`: Any changes to the external (non-QIIME 2) dependencies within any of our Distributions. These changes include bumping a dependency's version to either a newer/older pin, or removing/adding dependencies.
- `Development cycle environment files`: These can be found under the QIIME 2 Distributions repository under `20XX.REL+1/<distro>/passed/` (with `<distro>` being each QIIME 2 Distribution), and reflect our current development cycle (i.e. non-release versioned) environment files.
- `Repository freeze`: All plugin repositories within any QIIME 2 Distribution will not commit any code changes to the main branch from the Friday prior to the scheduled release date until the `20XX.REL+1` announcement goes live on the user forum.
