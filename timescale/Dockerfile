FROM timescale/timescaledb:latest-pg17

# bug inside the 00_install_timescaledb.sh
# creates extensions for an non-existing database template1
# so we remove it
RUN sed -i 's/psql -U "${POSTGRES_USER}" template1 -f ${create_sql}//' \
    /docker-entrypoint-initdb.d/000_install_timescaledb.sh

EXPOSE 5432