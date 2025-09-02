unique_constraint_query = """
 SELECT
          tc.table_name,
          tc.constraint_name,
          STRING_AGG(kcu.column_name, ', ' ORDER BY kcu.ordinal_position) as column_names
        FROM information_schema.table_constraints tc
        JOIN information_schema.key_column_usage kcu
          ON tc.constraint_name = kcu.constraint_name
          AND tc.table_schema = kcu.table_schema
        WHERE tc.constraint_type = 'UNIQUE'
          AND tc.table_schema = 'public'
        GROUP BY tc.table_name, tc.constraint_name
        ORDER BY tc.table_name, tc.constraint_name;
"""