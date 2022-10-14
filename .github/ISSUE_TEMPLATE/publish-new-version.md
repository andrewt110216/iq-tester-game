---
name: New Version
about: Publish new version on PyPI and add release on GitHub
title: '[vx.x.x DESCRIPTION]'
labels: ['release']
assignees: andrewt110216
---

- [ ] Determine appropriate versioning. See: https://blog.inedo.com/python-best-practices-for-versioning-python-packages-in-the-enterprise
- [ ] Check version in pyproject.toml
- [ ] Check version in README badge
- [ ] Update CHANGELOG
- [ ] Navigate to project root directory `cd ~/Documents/coding/iqtester`
- [ ] Run tests and linting: `flake8 src/iqtester && mypy src/iqtester`
- [ ] Make sure all changes are committed and pushed to remote main
- [ ] Update dist files: `python3 -m build`
- [ ] Publish to TestPyPI: `twine upload -r testpypi dist/*`
- [ ] Review TestPyPI publication page for any mistakes
- [ ] Download locally from TestPyPI and test: `pip install -i https://test.pypi.org/simple/ iqtester`
- [ ] Upload to PyPI: `twine upload dist/*`
- [ ] Publish Release on GH. Format for release name: [vx.x.x Description]

**Update files in main branch to prepare for next release**
- [ ] Add next version to CHANGELOG with TBD date and comment
- [ ] Update version in pyproject.toml
- [ ] Update README badge