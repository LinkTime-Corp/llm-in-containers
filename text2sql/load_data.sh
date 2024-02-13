#!/bin/bash
set -e -u

CUR_PATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
CONFIG_FILE="${CUR_PATH}/conf/config.json"
DB_PATH="${CUR_PATH}/db"

find_password() {
    local file_path="$1"
    local found=0

    while IFS= read -r line; do
        if [[ "$line" == *'"database":'* ]]; then
            found=1
        fi
        if [[ $found -eq 1 && "$line" == *'"password":'* ]]; then
            PASSWORD=$(echo "$line" | sed -e 's/.*"password": *"\(.*\)".*/\1/')
            break
        fi
    done < "$file_path"
}

find_password "$CONFIG_FILE"

docker exec -i text2sql_mysql_1 sh -c "exec mysql -uroot -p$PASSWORD" < $DB_PATH/mysqlsampledatabase.sql
