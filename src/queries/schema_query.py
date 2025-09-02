schema_query = """
SELECT 
          t.table_name,
          c.column_name,
          c.data_type,
          c.is_nullable,
          c.column_default,
          CASE 
            WHEN pk.column_name IS NOT NULL THEN true 
            ELSE false 
          END as is_primary_key,
          COALESCE(
            (SELECT COUNT(*) FROM information_schema.tables t2 WHERE t2.table_name = t.table_name AND t2.table_schema = 'public'),
            0
          ) as table_exists
        FROM information_schema.tables t
        LEFT JOIN information_schema.columns c ON t.table_name = c.table_name 
          AND t.table_schema = c.table_schema
        LEFT JOIN (
          SELECT ku.table_name, ku.column_name
          FROM information_schema.table_constraints tc
          JOIN information_schema.key_column_usage ku
            ON tc.constraint_name = ku.constraint_name
            AND tc.table_schema = ku.table_schema
          WHERE tc.constraint_type = 'PRIMARY KEY'
        ) pk ON c.table_name = pk.table_name AND c.column_name = pk.column_name
        WHERE t.table_schema = 'public' 
          AND t.table_type = 'BASE TABLE'
        ORDER BY t.table_name, c.ordinal_position;
"""

