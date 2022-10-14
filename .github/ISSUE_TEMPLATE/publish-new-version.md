---
name: Publish New Version
about: Publish a new version of iqtester on PyPI and add release on GitHub
title: ''
labels: 'Release'
assignees: andrewt110216

---

- [ ] Determine appropriate versioning. See: https://blog.inedo.com/python-best-practices-for-versioning-python-packages-in-the-enterprise
- [ ] Update version in pyproject.toml
- [ ] Update README badge
- [ ] Update CHANGELOG
- [ ] Navigate to project root directory `cd ~/Documents/coding/iqtester`
- [ ] Run tests and linting: `flake8 src/iqtester && mypy src/iqtester`
- [ ] Update dist files: `python3 -m build`
- [ ] Publish to TestPyPI: `twine upload -r testpypi dist/*`
- [ ] Review TestPyPI publication page for any mistakes
- [ ] Download locally from TestPyPI and test: `pip install -i https://test.pypi.org/simple/ iqtester`
- [ ] Upload to PyPI: `twine upload dist/*`
- [ ] Publish Release on GH. Format for release name: [vx.x.x Description]