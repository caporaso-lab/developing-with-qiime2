(ci-how-to-maximize-compatibility)=
# Maximize compatibility between your plugin(s) and existing QIIME 2 distribution(s)

You can build your QIIME 2 tools in your own way.
Your new tool doesn't need to live in the [QIIME 2 GitHub organization](https://github.com/qiime2) or be part of one of the QIIME 2 distributions developed and maintained in the [Caporaso Lab](https://cap-lab.bio).

If you want your QIIME 2 plugin(s) or other tools to work with existing QIIME 2 {term}`distribution(s) <Distribution>`, your focus should be on maximizing compatibility between your plugin(s) and the relevant QIIME 2 distribution(s).
To do this, you can observe the {term}`artifact classes <Artifact class>` that are used in the target distribution(s), and make your functionality compatible with those.
Avoid defining new artifact classes when you can reuse existing ones, to maximize compatibility and interoperability (as well as reducing your own software development time!).
A complete list of artifact classes and formats available in a deployment of QIIME 2 can be accessed with the `qiime tools list-types` and `qiime tools list-formats` commands.
(Some are missing documentation - we'd [love your help addressing that](https://github.com/caporaso-lab/developing-with-qiime2/issues/97).)
If you do need to create new artifact classes, you can add these in your own plugin(s).

The Caporaso Lab is not taking on new responsibility for distributing plugins right now (i.e., integrating them in the distributions they develop and maintain), but we are curently (23 April 2024) developing new mechanisms for helping you share your plugin or other tools (see [](ci-how-to-publicize)) that will ultimately replace the [QIIME 2 Library](https://library.qiime2.org).

You can consider the existing distributions to be foundations that you can build on, or you can create and distribute your own conda metapackages.
Some guidance on each of these approaches:
   - Your install instructions can indicate that a user should install whichever distribution you depend on (e.g., `tiny`, `amplicon`, or `metagenome`) and then illustrate how to install your plugin(s) in that environment however it makes sense (e.g., `conda` or `pip`). Complete install instructions are drafted for you in the `README.md` of plugins that you build using our template (see [](plugin-from-template)).
   - Alternatively, you can compose and share your own distribution of plugins (e.g., building from the `tiny` distribution) that captures the set of functionality you’d like to share.

Either of these approaches is totally fine.
The former is an easier starting point.

The weekly development builds of the QIIME 2 distributions can help you make sure your code stays current with the distribution(s) you are targeting as you can automate your testing against them.
[](setup-dev-environment) will help you install the most recent successful development metapackage build (again, usually weekly, but sometimes the builds fail and take time to debug).

You can request feedback on your plugin as a whole from more experienced QIIME 2 developers by reaching out on the [Developer Discussion on the QIIME 2 Forum](https://forum.qiime2.org/c/dev-discussion).
However, be cognizant of the fact that doing code review takes a long time to do well: you should only request this when you feel like you have a final draft of the plugin that you'd like to release, and expect that the reviewer may point out that there is a bunch more work that should be done before you release.
Please have others who you work closely with -- ideally experienced software developers, and even more ideally experienced QIIME 2 plugin developers -- review it first.
If you have questions along the way, you can ask those whenever - just be sure to review *[Developing with QIIME 2](https://develop.qiime2.org/)* and search the forum in case your question has already been answered previously.