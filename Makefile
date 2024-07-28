.PHONY: clean make_rst_from_markdown dist publish test_publish
.IGNORE: clean

clean:
	powershell Remove-Item -Recurse -Force ./build
	powershell Remove-Item -Recurse -Force ./dist

make_rst_from_markdown:
	pandoc -f markdown -t rst  README.md -o README.rst

dist: clean make_rst_from_markdown
	py -3.10 -m pip install 'twine>=1.5.0'
	py -3.10 -m build

check_dist: dist
	py -3.10 -m twine check dist/*

publish: dist check_dist
	py -3.10 -m twine upload --repository pypi dist/*

test_publish: dist check_dist
	py -3.10 -m twine upload --repository testpypi dist/*
