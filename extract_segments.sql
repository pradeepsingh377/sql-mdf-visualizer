/*
    Extract MDF allocation usage in 4MB segments.
    Outputs a segment → MB_used table suitable for visualization.
*/

;WITH Alloc AS (
    SELECT 
        allocated_page_page_id AS page_id
    FROM sys.dm_db_database_page_allocations(
            DB_ID(), NULL, NULL, NULL, 'LIMITED'
    )
    WHERE allocated_page_file_id = 1   -- main MDF file only
),
Segments AS (
    SELECT 
        page_id,
        page_id / 512 AS segment_id    -- 512 pages * 8KB = 4MB
    FROM Alloc
)
SELECT 
    segment_id,
    COUNT(*) AS pages_used,
    COUNT(*) * 8 AS KB_used,
    (COUNT(*) * 8.0) / 1024 AS MB_used
FROM Segments
GROUP BY segment_id
ORDER BY segment_id;
