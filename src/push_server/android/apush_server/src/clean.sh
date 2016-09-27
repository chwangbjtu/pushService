#/bin/sh

cd ../lib/
rm -rf libconfig.a
rm -rf libctrl.a
rm -rf libhttp.a
rm -rf libmgmt.a
rm -rf libnetsvc.a
rm -rf libservice.a
rm -rf libuser_mgr.a
rm -rf libutil.a
rm -rf libvisitor.a
rm -rf libencrypt.a


cd ../src/
make clean
