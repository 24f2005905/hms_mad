#!/bin/bash

TARGET_DB=${1}
INIT_SQL_DIR=${2}

set -x

mkdir -p $(dirname ${TARGET_DB})
rm -f ${TARGET_DB}

sqlite3 ${TARGET_DB} < ${INIT_SQL_DIR}/hms-ddl.sql
sqlite3 ${TARGET_DB} < ${INIT_SQL_DIR}/init/users.sql
sqlite3 ${TARGET_DB} < ${INIT_SQL_DIR}/init/doctor_slots.sql
sqlite3 ${TARGET_DB} < ${INIT_SQL_DIR}/init/departments.sql
sqlite3 ${TARGET_DB} < ${INIT_SQL_DIR}/init/doctor-dept.sql
sqlite3 ${TARGET_DB} < ${INIT_SQL_DIR}/init/appointments.sql
sqlite3 ${TARGET_DB} < ${INIT_SQL_DIR}/init/treatments.sql
set +x
