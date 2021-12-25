export MAYA_BIN = C:\Program Files\Autodesk\Maya2022\bin
export MAYA_PY = ${MAYA_BIN}/mayapy.exe

clean:
	rm -fr ./build
	rm -fr ./dist

publish:
	rm -fr ./build
	rm -fr ./dist
	"${MAYA_PY}" -m pip install 'twine>=1.5.0'
	"${MAYA_PY}" setup.py sdist bdist_wheel
	"${MAYA_PY}" -m twine upload --repository pypi dist/*

test_publish:
	rm -fr ./build
	rm -fr ./dist
	"${MAYA_PY}" -m pip install 'twine>=1.5.0'
	"${MAYA_PY}" setup.py sdist bdist_wheel
	"${MAYA_PY}" -m twine upload --repository testpypi dist/*

dist:
	rm -fr ./build
	rm -fr ./dist
	"${MAYA_PY}" -m pip install 'twine>=1.5.0'
	"${MAYA_PY}" setup.py sdist bdist_wheel