# Create a temporary container to back up the volume
docker run --rm -v postgres_data:/data -v $(pwd):/backup alpine \
    tar czvf /backup/postgres_backup.tar.gz -C /data .

# Restore the backup to the volume
docker run --rm -v postgres_data:/data -v $(pwd):/backup alpine \
    tar xzvf /backup/postgres_backup.tar.gz -C /data

docker exec -t postgres-container pg_dump -U overcat -F p -f /var/lib/postgresql/data/backup/stocks_backup.sql stocks

docker exec -t postgres-container pg_dump -U overcat -F c -b -v -f /var/lib/postgresql/data/backup/stocks_backup.dump stocks

docker exec -i postgres-container psql -U overcat -d stocks < /var/lib/postgresql/data/backup/stocks_backup.sql

docker exec -i postgres-container pg_restore -U overcat -d stocks /var/lib/postgresql/data/backup/stocks_backup.dump


