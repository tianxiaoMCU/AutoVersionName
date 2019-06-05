import os
import sys
import re

fireware_version = ''
version_file_path = r"D:\IPoverUSB\keil\version.h"

# 检查保存版本号的源文件是否存在
if os.path.exists(version_file_path) == False:
    print('Version file not exists!!!')
    sys.exit(0)

# 解析版本号源文件，获得版本号各个组成部分的值
re1 = '.*?'  # Non-greedy match on filler
re2 = '(".*?")'  # Double Quote String 1

pre_release_flag = False
build_flag = False

version_file = open(version_file_path, 'r')
for line in version_file.readlines():
    if line.startswith(r"#define PRE_RELEASE"):
        pre_release_flag = True
        rg = re.compile(re1+re2, re.IGNORECASE | re.DOTALL)
        m = rg.search(line)
        if m:
            pre_release_value = m.group(1).strip('""')
            print(pre_release_value)
    elif line.startswith(r"#define BUILD"):
        build_flag = True
        rg = re.compile(re1+re2, re.IGNORECASE | re.DOTALL)
        m = rg.search(line)
        if m:
            build_value = m.group(1).strip('""')
            print(build_value)
    elif line.startswith(r"#define VERSION_CORE"):
        rg = re.compile(re1+re2, re.IGNORECASE | re.DOTALL)
        m = rg.search(line)
        if m:
            version_core_value = m.group(1).strip('""')
            print(version_core_value)
    else:
        pass

version_file.close()

# 根据格式组装获取前面的值，得到完整的版本号
if pre_release_flag and build_flag:
    fireware_version = version_core_value + '-' + \
        pre_release_value + '+' + build_value
elif pre_release_flag:
    fireware_version = version_core_value + '-' + pre_release_value
elif build_flag:
    fireware_version = version_core_value + '+' + build_value
else:
    fireware_version = version_core_value

print(fireware_version)

# 将IDE生成的bin或者hex文件重命名为得到的版本号
fireware_path = r"D:\IPoverUSB\keil\Objects\IPoverUSB.hex"
new_fireware_path = fireware_path.replace(
    os.path.basename(fireware_path), fireware_version + os.path.splitext(os.path.split(fireware_path)[1])[1])

# os.path.normpath(new_fireware_path)
os.replace(fireware_path, new_fireware_path)
