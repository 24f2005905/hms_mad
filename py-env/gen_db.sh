#!/bin/bash

#Set the environment variables
export PGHOST=${1}
export PGPORT=${2}
export PGUSER=${3}
export PGPASSWORD=${4}
export PGDATABASE=${5}
export INIT_SQL_DIR=${6}

set -x

#Drop database if it already exists
psql postgres --command "DROP DATABASE ${PGDATABASE};"

#Create database 
psql postgres --command "CREATE DATABASE ${PGDATABASE};"

#Run DDL

psql -d ${PGDATABASE} -f ${INIT_SQL_DIR}/hms-ddl.sql
psql -d ${PGDATABASE} -f ${INIT_SQL_DIR}/init/users.sql
psql -d ${PGDATABASE} -f ${INIT_SQL_DIR}/init/doctor_slots.sql
psql -d ${PGDATABASE} -f ${INIT_SQL_DIR}/init/departments.sql
psql -d ${PGDATABASE} -f ${INIT_SQL_DIR}/init/doctor-dept.sql
psql -d ${PGDATABASE} -f ${INIT_SQL_DIR}/init/appointments.sql
psql -d ${PGDATABASE} -f ${INIT_SQL_DIR}/init/treatments.sql
set +x
