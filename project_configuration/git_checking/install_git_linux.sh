#!/bin/bash

# Оригинал: https://ilhicas.com/2018/08/08/bash-script-to-install-packages-multiple-os.html

declare -A osInfo;
osInfo[/etc/debian_version]="apt-get install -y"
osInfo[/etc/alpine-release]="apk --update add"
osInfo[/etc/centos-release]="yum install -y"
osInfo[/etc/fedora-release]="dnf install -y"
osInfo[/etc/SuSE-release]="zypper install -y"

RED='\033[0;31m' # код цвета для красного текста
NC='\033[0m' # сброс цвета

# shellcheck disable=SC2068
for f in ${!osInfo[@]}
do
    if [[ -f $f ]];then
        package_manager=${osInfo[$f]}
    fi
done

package="git"

if [ -n "$package_manager" ]; then
    ${package_manager} ${package} || { echo -e "${RED}Не получилось установить git, проверьте интернет-соединение.${NC}"; exit 1; }
else
    echo -e "${RED}Не поддерживаемый дистрибутив. Пожалуйста, установите git вручную.${NC}"
    exit 1;
fi
