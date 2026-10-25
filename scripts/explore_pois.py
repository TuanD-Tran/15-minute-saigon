import duckdb

print(
    duckdb.sql(
        """
        SELECT category, count(*) AS n, count(name) AS named_count
        FROM 'data/processed/poi_snapshot.parquet'
        GROUP BY category
        ORDER BY n DESC
        """
    )
)

print(
    duckdb.sql(
        """
        SELECT h3_cell, count(*) AS n
        FROM 'data/processed/poi_snapshot.parquet'
        GROUP BY h3_cell
        HAVING count(*) > 0 
        ORDER BY n DESC
        LIMIT 10
        """
    )
)
