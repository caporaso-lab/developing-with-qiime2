# QIIME 2 Development and Release Cycle Structure

In the sections below, we will go through the development cycle structure and release process for QIIME 2.
The aim is to provide insight into our structure for other research software engineering teams that may want to utilize any/all of these processes, as well as to assist our community developers in knowing what timeline/deadlines they should be aware of within each development/release cycle.
If you have any questions on this process, please don't hesitate to reach out on our user forum under the [Developer Discussion](https://forum.qiime2.org/c/dev-discussion) category!

## QIIME 2 Release Cycle Structure

As of 2024.10, QIIME 2 Distributions are released bi-anually, on the first Wednesday of April and October.
This schedule provides us with ample development time between releases, and provides our developer community with at least a three month notice for any interface/API changes and any external dependency changes (i.e. bumping Python, removing a deprecated package, etc).

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

## QIIME 2 Development Cycle Structure

Our current development cycle structure aims to strike a balance between completing our team's grant funded deliverables and managing new/ongoing community contributions.
We have several project boards within the QIIME 2 Github Organization that aid in this, which we will outline below.


[**Triage Board**](https://github.com/orgs/qiime2/projects/36/views/1?sortedBy%5Bdirection%5D=asc&sortedBy%5BcolumnId%5D=Status&sortedBy%5Bdirection%5D=asc&sortedBy%5BcolumnId%5D=Repository)
 - This project board is what we use to 'catch' any new issues or pull requests we receive within the QIIME 2 Github Organization. Our team reviews this board once a week to determine if the given submission(s) are something we will/won't do, what the timeline for completion would be (i.e. current release or future release), and if we require any additional information before moving forward.

[**Approved but Unscheduled Board**](https://github.com/orgs/qiime2/projects/40)

- This project board is for issues or pull requests that contain improvements or new feature requests that we've approved conceptually, but that we don't currently have the bandwidth and/or funding to support work on. We will review this board at the beginning and middle of each development cycle (specific dates listed in the release cycle diagram above) as we are sorting through what each team member should be prioritizing for the upcoming release, and will move things from this board to the current release project board as we have time/funding.

**Current Dev Cycle Project Board (20XX.REL+1)**
- This project board is where we track all issues and pull requests that we aim to complete within the current *development* cycle (i.e. the *next* release of QIIME 2). This view of the board shows the following:
  - **Backlog**: Items that haven't been picked up by a developer yet.
  - **In Development**: Items that are currently in progress (i.e. someone on our team is actively working on them).
  - **Needs Review**: Items that require a code review before they can be merged.
  - **In Review**: Items that a member of our team are currently in the process of reviewing.
  - **Ready for Merge**: Items that have been reviewed and approved and are ready to be merged.
  - **Changelog Needed**: Items that have been merged but still need to be added to our development changelog.
  - **Completed**: Items that have been merged and added to our development changelog.

**Current Dev Cycle Assignments**
- This view of our current dev cycle project board shows which developer on our team is assigned to particular issues and/or pull requests, along with the type of project these assignments fall under. We do a weekly review of each team member's assignments, provide additional tasks to everyone as needed (capping anyone's current workload at ten assignments at any given time). Assignments can fall under the following project types:
  - **Urgent**: This is something that requires immediate attention (typically a bug that will warrant a patch release).
  - **Funded Objective**: This is something that is required for our current grant deliverables, and must be completed within the designated time frame.
  - **Maintenance**: This is something that is required for general software upkeep within the QIIME 2 ecosystem. Examples of this include documentation updates, changes to our packaging infrastructure, and general code updates related to deprecated dependency versions/actions/etc.
  - **Weekly**: This is something that doesn't fall in any of the categories above, but will be assigned to someone on our team as a weekly round-robin task. This is typically where our community contributions/requests will be managed on a more regular basis, so that we can continue integrating helpful ideas/features/requests from our developer community!

We hope this helps provide more insight into what's happening behind the scenes, and can help each of you to better understand what we're prioritizing and currently working on.

## Developmental Best Practices

These are a few of our recommendations to our developer community to help us to better address any incoming issues/pull requests you submit within the QIIME 2 Organization (i.e. any plugin repository housed under the QIIME 2 or caporaso-lab organizations on Github).

### Issue/Pull Request Prefixes

These prefixes help us to quickly review and organize any incoming issues or pull requests, based on the type of code change/request that they fall under.

#### Standard/plugin-specific development
- **NEW**: a new feature
- **IMP**: an improvement to an existing feature
- **MAINT**: general code maintenance
- **REF**: refactoring existing code/methods
- **TEST**: refactors or adds new tests
- **BUG**: self-explanatory (fixes a bug)
- **DEP**: adds/removes an external dependency within a specific plugin
- **PIN**: changes an existing version pin for an external dependency within a specific plugin

#### Misc/non-standard development
- **CI**: continuous integration/Github Actions
- **DOC**: documentation
