## Creating a new release of your plugin on Github
As you add new features into your plugin, you may wish to create 'release' versions to share with your users. We’ve created helpful GitHub workflow automation that runs each time you publish a new release on your plugin’s repository. If you used our plugin template, this automation is already included!

A Github workflow is included upon creation of your plugin (using our plugin template) that will automatically run when a new Github release is published on your plugin's repository.
This workflow will mint a new 'release' environment file that includes the latest QIIME 2 release of the given distribution you specified upon plugin creation, as well as the newly minted release version of your plugin.
Once this new environment file is created, a pull request will get opened on your plugin's repository that contains these changes.
An additional automated check will then run to test out installation of this newest version of your plugin, and a comment will be added on that pull request that will provide the status of this check (either success or failure).
```{figure} ../images/release-env-PR-overview.png
:align: center
```

If the check was successful, you can go ahead and merge this pull request.
```{figure} ../images/release-env-PR-passed.png
:align: center
```

If the check was unsuccessful, a link to the error log is provided for you to review and troubleshoot.
```{figure} ../images/release-env-PR-failed.png
:align: center
```

If you are stuck and need help interpreting these logs, you can always ask for help on the [QIIME 2 Forum](https://forum.qiime2.org).

## How to publish a Github release
Released versions of software are helpful for bundling a cohesive grouping of new functionality and any relevant bug fixes into a particular snapshot in time, so that users know what to expect when they install a particular version of your plugin.
When you are ready to create a 'released' version of your plugin, you can do so by creating an official release on Github.
This process will create a unique tag that you define, and this tag will be attached to the latest commit on your main branch (or another branch, if you would like to create and specify release branches).

Before creating your first release, you'll need to update some permissions on your plugin's Github repository in order for our automated checks to run.
You can update these permissions by navigating to your plugin repository's Settings page -> Actions -> General.
```{figure} ../images/settings-general.png
:align: center
```

From this page, you'll scroll down to the 'Workflow permissions' section, and select 'Read and write permissions' and 'Allow Github Actions to create and approve pull requests'.
```{figure} ../images/settings-gha-permissions.png
:align: center
```

Now that you've updated your Github repository's settings, you should be ready to publish your first Github release!

Github Documentation offers a helpful walkthrough of creating a new release, which you can find [here](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository#creating-a-release).
