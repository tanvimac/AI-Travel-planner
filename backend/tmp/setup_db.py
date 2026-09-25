import psycopg2

def setup():
    conn = psycopg2.connect(host="localhost", port=5432, user="postgres", password="postgres", dbname="postgres")
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute("SELECT datname FROM pg_database;")
    dbs = [r[0] for r in cur.fetchall()]
    print("Databases:", dbs)
    if "travel_planner" not in dbs:
        cur.execute("CREATE DATABASE travel_planner;")
        print("Created database travel_planner")
    
    cur.execute("SELECT rolname FROM pg_roles;")
    roles = [r[0] for r in cur.fetchall()]
    print("Roles:", roles)
    if "travel_user" not in roles:
        cur.execute("CREATE USER travel_user WITH PASSWORD 'travel_password' SUPERUSER;")
        print("Created user travel_user")
    else:
        cur.execute("ALTER USER travel_user WITH PASSWORD 'travel_password' SUPERUSER;")
        print("Updated travel_user password")
    
    cur.execute("GRANT ALL PRIVILEGES ON DATABASE travel_planner TO travel_user;")
    cur.execute("ALTER DATABASE travel_planner OWNER TO travel_user;")
    print("Permissions granted!")
    conn.close()

if __name__ == "__main__":
    setup()
