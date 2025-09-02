
check_constraint_query = """
  SELECT
          tc.table_name,
          tc.constraint_name,
          cc.check_clause
        FROM information_schema.table_constraints tc
        JOIN information_schema.check_constraints cc
          ON tc.constraint_name = cc.constraint_name
          AND tc.constraint_schema = cc.constraint_schema
        WHERE tc.constraint_type = 'CHECK'
          AND tc.table_schema = 'public'
        ORDER BY tc.table_name, tc.constraint_name;
"""
