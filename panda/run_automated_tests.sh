#!/bin/bash
TEST_FILENAME=${TEST_FILENAME:-nosetests.xml}
if [ ! -f "/EON" ]; then
  TESTSUITE_NAME="Panda_Test-EON"
else
  TESTSUITE_NAME="Panda_Test-DEV"
fi

<<<<<<< HEAD
PYTHONPATH="." nosetests -v --with-xunit --xunit-file=./$TEST_FILENAME --xunit-testsuite-name=$TESTSUITE_NAME -s tests/automated/$1*.py
=======
cd boardesp
make flashall
cd ..


PYTHONPATH="." python $(which nosetests) -v --with-xunit --xunit-file=./$TEST_FILENAME --xunit-testsuite-name=$TESTSUITE_NAME -s tests/automated/$1*.py
>>>>>>> 7d5332833b11570db288f35657a963ed0d8cad0a
