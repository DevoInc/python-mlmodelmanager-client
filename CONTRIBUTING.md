# Contributing to Devo

There are many ways to contribute to Devo. Here are some of them:


1. [Report bugs](#reporting-bugs) or request features in the [issue tracker](https://github.com/DevoInc/python-mlmodelmanager-client/issues).
2. [Submit patches](#submit-patch) for bug fixes and/or new features.

## Reporting bugs

Well-written bug reports are very helpful, keep in mind this guideline when 
reporting a new bug.

* Check the open issues to see if it has already been reported.
* Write complete, reproducible, specific bug reports: the smaller the test case,
 better. 
* Includes the output of the library with all the error information


## Submit patch
To be able to make a fork and the corresponding MR you have to accept Devo's CLA
The process to modify one package or script is the next:

1. Create your fork from main
2. Create a branch that determines the change. The branch name determines the versioning, if it starts with:
    - BREAK or MAJOR ⟶ MAJOR (1.2.3 ⟶ 2.0.0)
    - FEAT or MINOR ⟶ MINOR (1.2.3 ⟶ 1.3.0)
    - Anything else ⟶ PATCH (1.2.3 ⟶ 1.2.4)
3. Add to the `CHANGELOG.md`, in 
[`Unreleased`](#How_can_I_minimize_the_effort_required?) the tasks 
that you are going to take or are carrying out to be able to review at a quick 
glance the objective of the branch.
4. Make your awesome code
5. Never forget to **change the changelog**.  
4.1 [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
6. Create a Pull Request to master with correct version and tests passed.


## Keep a CHANGELOG
##### What’s a change log?
A change log is a file which contains a curated, chronologically ordered list of 
notable changes for each version of a project.

##### What’s the point of a change log?
To make it easier for users and contributors to see precisely what notable 
changes have been made between each release (or version) of the project.

##### Why should I care?
Because software tools are for people. If you don’t care, why are you 
contributing? Right, Devo pay you for it, but surely, there must be a kernel
 (ha!) of care somewhere in that lovely little brain of yours.

##### What makes a good change log?
A good change log sticks to these principles:

* It’s made for humans, not machines, so legibility is crucial.
* Easy to link to any section (hence Markdown over plain text).
* One sub-section per version.
* List releases in reverse-chronological order (newest on top).
* Write all dates in `YYYY-MM-DD` format. (Example: `2012-06-02` 
for `June 2nd, 2012`.) It’s international, sensible, and language-independent.
* Explicitly mention whether the project follows [Semantic Versioning](http://semver.org/spec/v2.0.0.html).
* Each version should:
  * List its release date in the above format.
  * Group changes to describe their impact on the project, as follows:
  * `Added` for new features.
  * `Changed` for changes in existing functionality.
  * `Deprecated` for once-stable features removed in upcoming releases.
  * `Removed` for deprecated features removed in this release.
  * `Fixed` for any bug fixes.
  * `Security` to invite users to upgrade in case of vulnerabilities.

##### How can I minimize the effort required?

Always have an `Unreleased` section at the top for keeping track of any changes.

This serves two purposes:
* People can see what changes they might expect in upcoming releases
* At release time, you just have to change "Unreleased" to the version number and add a new "Unreleased" 
header at the top.

**Feel free for update and improve this document content or format.**<br/>



## Development

This package is built and managed using Poetry. It can be downloaded and installed following the guides here [Python-Poetry.org](https://python-poetry.org/).

Once installed git clone this repository and run `poetry install` in the project root. This will install dependencies and devdependencies and you will then be ready to work on the project.

## Testing/Linting

- Type linting: `poetry run mypy <packages>`, `poetry run mypy devo_ml` `poetry run mypy --namespace-packages tests`

- Style linting: `poetry run flake8 <packages>`, `poetry run flake8 devo_ml`

- Testing: `poetry run pytest`

### Built package testing with tox

Install tox with pip.

Run `tox` to run all tests
Run `tox -e lint` to run all linting
