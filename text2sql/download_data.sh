!/bin/bash
set -e -u

CONFIG_FILE="conf/config.json"

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

rm -rf db
wget https://www.mysqltutorial.org/wp-content/uploads/2023/10/mysqlsampledatabase.zip -P db
unzip db/mysqlsampledatabase.zip -d db

docker exec -i text2sql_mysql_1 sh -c "exec mysql -uroot -p$PASSWORD" < db/mysqlsampledatabase.sql
set +e +u
