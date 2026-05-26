WITH ROW_COUNT AS (
    SELECT
        'ROW_COUNT_NOT_NULL' AS TEST,
        COUNT(*) AS ROW_COUNT
    FROM READ_PARQUET('data/raw/laps.parquet')
),

PRIMARY_KEYS_NULL AS (
    SELECT
        'PRIMARY_KEYS_IS_NULL' AS TEST,
        COUNT(*) AS NULL_PKS
    FROM READ_PARQUET('data/raw/laps.parquet')
    WHERE meeting_key IS NULL
    OR session_key IS NULL
    OR driver_number IS NULL
    OR lap_number IS NULL
),

PRIMARY_KEYS_NOT_UNIQUE AS (
    SELECT
        'PRIMARY_NOT_UNIQUE' AS TEST,
        COUNT(*) AS NON_UNIQUE_PKS
    FROM (
        SELECT
            meeting_key,
            session_key,
            driver_number,
            lap_number
        FROM READ_PARQUET('data/raw/laps.parquet')
        GROUP BY meeting_key, session_key, driver_number, lap_number
        HAVING COUNT(*) > 1
    )
),

LIST_TO_VARCHAR AS (
    SELECT
        'LIST_TO_VARCHAR' AS TEST,
        COUNT(*) AS INVALID_TYPE
    FROM read_parquet('data/raw/laps.parquet')
    WHERE typeof(segments_sector_1) != 'VARCHAR'
    OR typeof(segments_sector_2) != 'VARCHAR'
    OR typeof(segments_sector_3) != 'VARCHAR'
)

SELECT * FROM (
    SELECT TEST, IF(ROW_COUNT > 0, 'PASS', 'FAIL') AS STATUS FROM ROW_COUNT
    UNION ALL
    SELECT TEST, IF(NULL_PKS = 0, 'PASS', 'FAIL') AS STATUS FROM PRIMARY_KEYS_NULL
    UNION ALL
    SELECT TEST, IF(NON_UNIQUE_PKS = 0, 'PASS', 'FAIL') AS STATUS FROM PRIMARY_KEYS_NOT_UNIQUE
    UNION ALL
    SELECT TEST, IF(INVALID_TYPE = 0, 'PASS', 'FAIL') AS STATUS FROM LIST_TO_VARCHAR
)
ORDER BY STATUS, TEST;