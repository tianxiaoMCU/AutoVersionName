import os
import sys
import xml.etree.ElementTree as ET
import re

version_file_path = sys.argv[1]

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

    elif line.startswith(r"#define BUILD"):
        build_flag = True
        rg = re.compile(re1+re2, re.IGNORECASE | re.DOTALL)
        m = rg.search(line)
        if m:
            build_value = m.group(1).strip('""')

    elif line.startswith(r"#define VERSION_CORE"):
        rg = re.compile(re1+re2, re.IGNORECASE | re.DOTALL)
        m = rg.search(line)
        if m:
            version_core_value = m.group(1).strip('""')

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


for entry in os.scandir():
    if entry.is_file():
        if entry.name.endswith('.eww'):

            # find current target
            wsdtfile = os.path.join(os.getcwd(), 'settings')
            wsdtfile = os.path.join(
                wsdtfile, entry.name.replace('.eww', '.wsdt'))

            if os.path.exists(wsdtfile):
                tree = ET.ElementTree(file=wsdtfile)
                ConfigDictionary = tree.find('ConfigDictionary')
                CurrentConfigs = ConfigDictionary.find('CurrentConfigs')
                TargetName = CurrentConfigs.find('Project').text.split('/')[1]

                tree = ET.ElementTree(file=entry.name.replace('.eww', '.ewp'))
                for tag in tree.findall('configuration'):
                    if TargetName == tag.find('name').text:
                        for settings in tag.findall('settings'):
                            if 'OBJCOPY' == settings.find('name').text:
                                data = settings.find('data')
                                for option in data.findall('option'):
                                    if 'OOCOutputFile' == option.find('name').text:
                                        OutputName = option.find(
                                            'state').text.split('.')[0]
                                        print(OutputName)
                                        break

                            if 'General' == settings.find('name').text:
                                data = settings.find('data')
                                for option in data.findall('option'):
                                    if 'ExePath' == option.find('name').text:
                                        OutputDirectory = os.path.join(
                                            os.getcwd(), option.find('state').text)
                                        print(OutputDirectory)
                                        break

                break

            print('Please build the project once')
            sys.exit(0)

        elif entry.name.endswith('.uvproj') or entry.name.endswith('.uvprojx'):

            if entry.name.endswith('.uvproj'):
                uvoptfile = entry.name.replace('.uvproj', '.uvopt')
            elif entry.name.endswith('.uvprojx'):
                uvoptfile = entry.name.replace('.uvprojx', '.uvoptx')

            tree = ET.ElementTree(file=uvoptfile)

            # find current target
            for tag in tree.findall('Target'):
                TargetOption = tag.find('TargetOption')
                OPTFL = TargetOption.find('OPTFL')
                IsCurrentTarget = int(OPTFL.find('IsCurrentTarget').text)
                if IsCurrentTarget:
                    TargetName = tag.find('TargetName').text
                    break

            # get output directory and outputname
            # ide is keil5
            tree = ET.ElementTree(file=entry.name)
            for tag in tree.find('Targets').findall('Target'):
                if tag.find('TargetName').text == TargetName:
                    TargetOption = tag.find('TargetOption')
                    TargetCommonOption = TargetOption.find(
                        'TargetCommonOption')
                    OutputDirectory = TargetCommonOption.find(
                        'OutputDirectory').text
                    OutputDirectory = os.path.normpath(
                        os.path.join(os.getcwd(), OutputDirectory))
                    OutputName = TargetCommonOption.find(
                        'OutputName').text

            break

# 将IDE生成的bin或者hex文件重命名为得到的版本号
fireware_hex_path = os.path.join(OutputDirectory, OutputName + '.hex')
fireware_bin_path = os.path.join(OutputDirectory, OutputName + '.bin')

if os.path.exists(fireware_hex_path):
    fireware_path = fireware_hex_path
    new_fireware_path = fireware_path.replace(
        os.path.basename(fireware_path), fireware_version + os.path.splitext(os.path.split(fireware_path)[1])[1])
elif os.path.exists(fireware_bin_path):
    fireware_path = fireware_bin_path
    new_fireware_path = fireware_path.replace(
        os.path.basename(fireware_path), fireware_version + os.path.splitext(os.path.split(fireware_path)[1])[1])
else:
    print('No hex or bin file')
    sys.exit(0)

os.replace(fireware_path, new_fireware_path)
