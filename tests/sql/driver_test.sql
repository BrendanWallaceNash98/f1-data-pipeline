WITH ROW_COUNT AS (
    SELECT
        'ROW_COUNT_NOT_NULL' AS TEST,
        COUNT(*) AS ROW_COUNT
    FROM READ_PARQUET('data/raw/drivers.parquet')
),

PRIMARY_KEYS_NULL AS (
    SELECT
        'PRIMARY_KEYS_IS_NULL' AS TEST,
        COUNT(*) AS NULL_PKS
    FROM READ_PARQUET('data/raw/drivers.parquet')
    WHERE meeting_key IS NULL
    OR session_key IS NULL
    OR driver_number IS NULL
),

PRIMARY_KEYS_NOT_UNIQUE AS (
    SELECT
        'PRIMARY_NOT_UNIQUE' AS TEST,
        COUNT(*) AS NON_UNIQUE_PKS
    FROM (
        SELECT
            meeting_key,
            session_key,
            driver_number
        FROM READ_PARQUET('data/raw/drivers.parquet')
        GROUP BY meeting_key, session_key, driver_number
        HAVING COUNT(*) > 1
    )
)

SELECT * FROM (
    SELECT TEST, IF(ROW_COUNT > 0, 'PASS', 'FAIL') AS STATUS FROM ROW_COUNT
    UNION ALL
    SELECT TEST, IF(NULL_PKS = 0, 'PASS', 'FAIL') AS STATUS FROM PRIMARY_KEYS_NULL
    UNION ALL
    SELECT TEST, IF(NON_UNIQUE_PKS = 0, 'PASS', 'FAIL') AS STATUS FROM PRIMARY_KEYS_NOT_UNIQUE
)
ORDER BY STATUS, TEST;