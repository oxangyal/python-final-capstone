import sqlite3

DB_PATH = "mlb_cleaned.db"

def get_connection():
    try:
        conn = sqlite3.connect(DB_PATH)
        print("\u2705 Connected to the database.")
        return conn
    except sqlite3.Error as e:
        print("\u274C Connection error:", e)
        return None

# 1. Top 5 stolen bases in selected year and league
def top_stolen_bases(conn, year, league):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT Player, Team, stolen_bases
            FROM stolen_bases
            WHERE Year = ? AND League = ?
            ORDER BY stolen_bases DESC
            LIMIT 5
        """, (year, league))
        rows = cursor.fetchall()
        for row in rows:
            print(f"Player: {row[0]}, Team: {row[1]}, SB: {row[2]}")
    except Exception as e:
        print(":x: Error:", e)

# 2. Top 10 total bases in a given year
def top_total_bases(conn, year):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT Player, Team, total_bases
            FROM total_bases
            WHERE Year = ?
            ORDER BY total_bases DESC
            LIMIT 10
        """, (year,))
        rows = cursor.fetchall()
        for row in rows:
            print(f"Player: {row[0]}, Team: {row[1]}, Total Bases: {row[2]}")
    except Exception as e:
        print(":x: Error:", e)

# 3. Players in top for both doubles and triples
def top_combined_doubles_triples(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT d.Year, d.Player, d.Team, d.doubles, t.triples
            FROM doubles d
            JOIN triples t ON d.Player = t.Player AND d.Year = t.Year
            ORDER BY (d.doubles + t.triples) DESC
            LIMIT 10
        """)
        rows = cursor.fetchall()
        for row in rows:
            print(f"Year: {row[0]}, Player: {row[1]}, Team: {row[2]}, Doubles: {row[3]}, Triples: {row[4]}")
    except Exception as e:
        print(":x: Error:", e)

# 4. All-time walk leaders
def top_walks_all_time(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT Player, SUM(base_on_balls) AS total_walks
            FROM base_on_balls
            GROUP BY Player
            ORDER BY total_walks DESC
            LIMIT 10
        """)
        rows = cursor.fetchall()
        for row in rows:
            print(f"Player: {row[0]}, Total Walks: {row[1]}")
    except Exception as e:
        print(":x: Error:", e)

# 5. Top 5 by slugging + OBP combined metric
def top_combined_slugging_obp(conn, year):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT sa.Player, sa.Team,
                   sa.slugging_average, obp.on_base_percentage,
                   (sa.slugging_average + obp.on_base_percentage) AS combined_metric
            FROM slugging_average sa
            JOIN on_base_percentage obp
              ON sa.Year = obp.Year AND sa.Player = obp.Player
            WHERE sa.Year = ?
            ORDER BY combined_metric DESC
            LIMIT 5
        """, (year,))
        rows = cursor.fetchall()
        for row in rows:
            print(f"Player: {row[0]}, Team: {row[1]}, SLG: {row[2]:.3f}, OBP: {row[3]:.3f}, Combined: {row[4]:.3f}")
    except Exception as e:
        print(":x: Error:", e)

def menu():
    print("""
=== Baseball Advanced Query CLI ===
1. Top 5 Stolen Bases (Year + League)
2. Top 10 Total Bases by Year
3. Combined Doubles + Triples
4. All-Time Leaders in Walks (Base on Balls)
5. Top 5 Combined Slugging + OBP (by Year)
0. Exit
""")

def main():
    conn = get_connection()
    if not conn:
        return

    while True:
        menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            year = input("Enter year: ")
            league = input("Enter league (AL or NL): ")
            top_stolen_bases(conn, year, league)
        elif choice == "2":
            year = input("Enter year: ")
            top_total_bases(conn, year)
        elif choice == "3":
            top_combined_doubles_triples(conn)
        elif choice == "4":
            top_walks_all_time(conn)
        elif choice == "5":
            year = input("Enter year: ")
            top_combined_slugging_obp(conn, year)
        elif choice == "0":
            print("\ud83d\udc4b Goodbye!")
            break
        else:
            print(":warning: Invalid input")

    conn.close()

if __name__ == "__main__":
    main()
