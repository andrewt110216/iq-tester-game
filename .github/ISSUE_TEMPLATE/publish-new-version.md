---
name: Release
about: Release new version on PyPI and GitHub
title: '[vx.x.x DESCRIPTION]'
labels: ['release']
assignees: andrewt110216
---

**Update version references**
- [ ] Confirm version number. For guidance, see: https://blog.inedo.com/python-best-practices-for-versioning-python-packages-in-the-enterprise
- [ ] Update version in pyproject.toml
- [ ] Update version in README badge
- [ ] Update version and notes in CHANGELOG
- [ ] Remove placeholder comment for next version in CHANGELOG

**Final checks**
- [ ] Navigate to project root directory `cd ~/Documents/coding/iqtester`
- [ ] Run tests and linting: `flake8 src/iqtester && mypy src/iqtester`
- [ ] Make sure all changes are committed and pushed to remote main `git status`

**TestPyPI and PyPI**
- [ ] Generate new distribution files: `python3 -m build`
- [ ] Delete old distribution files
- [ ] Publish to TestPyPI: `twine upload -r testpypi dist/*`
- [ ] Review TestPyPI publication page
- [ ] Install from TestPyPI and test: `pip uninstall iqtester && pip install -i https://test.pypi.org/simple/ iqtester`
- [ ] Upload to PyPI: `twine upload dist/*`
- [ ] Test install from PyPI: `pip uninstall iqtester && pip install iqtester`

**GitHub Release**
- [ ] Draft new release on GH
- [ ] Create new tag for current version targeting main
- [ ] Release name format: vx.x.x SHORT DESCRIPTION
- [ ] Copy entire CHANGELOG file into description box
- [ ] Add distribution files (wheel and tar.gz)

**Update files in main branch to prepare for next release**
- [ ] Add back placeholder comment and next version header to CHANGELOG
- [ ] Update version in pyproject.toml
- [ ] Update version in README badge