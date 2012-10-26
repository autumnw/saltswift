#!/bin/sh

PROJECT='swift'
VERSION="6.1.0"
PKG=${PROJECT}_${VERSION}

EXIT_VAL=0
find ${PKG} -name .svn -exec rm -fr {} \; > /dev/null 2>&1
find ${PKG} -name .bzr -exec rm -fr {} \; > /dev/null 2>&1
find ${PKG} -name patches -exec rm -fr {} \; > /dev/null 2>&1

mv ${PKG}/debian .
tar -czf ${PKG}.orig.tar.gz ${PKG}
mv ./debian ${PKG}

echo "Start building....."
cd ${PKG}
debuild -uc -us
EXIT_VAL=$?
if [ $EXIT_VAL -ne 0 ]
then
	echo "Build package failed!"
	exit $EXIT_VAL
fi

PKG_ROOT="../packages"
PKG_PATH="$PKG_ROOT/${PKG}_`date +%m-%d-%y-%H-%M-%S`"
mkdir -p $PKG_PATH

echo "Move packages to $PKG_PATH ......."
mv ../*.deb $PKG_PATH
EXIT_VAL=$?
if [ $EXIT_VAL -ne 0 ]
then
	echo "Moving package failed!"
	exit $EXIT_VAL
fi

echo ""
echo ""
echo "==========================================================================="
echo "The follwoing packages were generated successfully:"
echo ""
for pkg in `ls $PKG_PATH/`
do
	echo $pkg
done
echo "==========================================================================="
echo ""
echo ""

exit $EXIT_VAL

