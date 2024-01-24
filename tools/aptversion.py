from apt import apt_pkg

a='1:1.4.0-1~12.04'
b='1:1.3.1+2SNAPSHOT20150116220343~2c07fa~devissue6273dspacemets~12.04'
vc=apt_pkg.version_compare(a,b)
print ('a=',a)
print ('b=',b)
if vc > 0:
    print('version a > version b')
elif vc == 0:
    print('version a == version b')
elif vc < 0:
    print('version a < version b')   
