import sqlite3

# Connection to the SQLite db
def get_connection():
    try:
        return sqlite3.connect("mlb_cleaned.db")
    except sqlite3.Error as e:
        print(f"Error connecting to DB: {e}")
        return None

# Function to display menu options in the terminal
def show_menu():
    print("\nChoose a query:")
    print("1. Top hitters by year")
    print("2. Players with AVG above a threshold")
    print("3. Players from a team")
    print("4. Exit")

# Query 1: Get top batting average players for a given year
def query_top_hitters_by_year(conn):
    try:
        year = input("Enter year (e.g., 2023): ").strip()
        cursor = conn.execute("""
            SELECT player, league, avg
            FROM batting_avg_leaders
            WHERE year = ?
            ORDER BY avg DESC
        """, (year,))
        results = cursor.fetchall()
        if results:
            print(f"\nTop hitters in {year}:")
            for row in results:
                print(f"  {row[0]} ({row[1]}) - AVG: {row[2]}")
        else:
            print("No data found.")
    except Exception as e:
        print(f" Error: {e}")

# Query 2: Show players with AVG above a user-defined threshold
def query_above_threshold(conn):
    try:
        threshold = float(input("Enter AVG threshold (e.g., 0.350): ").strip())
        cursor = conn.execute("""
            SELECT player, league, year, avg
            FROM batting_avg_leaders
            WHERE avg > ?
            ORDER BY avg DESC
        """, (threshold,))
        results = cursor.fetchall()
        if results:
            print(f"\nPlayers with AVG above {threshold}:")
            for row in results:
                print(f"  {row[0]} ({row[1]}, {row[2]}) - AVG: {row[3]}")
        else:
            print("No players above threshold.")
    except Exception as e:
        print(f"Error: {e}")

# Query 3: List all players from a specific team
def query_players_by_team(conn):
    try:
        team = input("Enter team name (e.g., Chicago): ").strip()
        cursor = conn.execute("""
            SELECT player, year, avg
            FROM batting_avg_leaders
            WHERE team LIKE ?
            ORDER BY year
        """, ('%' + team + '%',))
        results = cursor.fetchall()
        if results:
            print(f"\nPlayers from {team}:")
            for row in results:
                print(f"  {row[0]} ({row[1]}) - AVG: {row[2]}")
        else:
            print("No players found for team.")
    except Exception as e:
        print(f"Error: {e}")

# Main function to run the command-line interface
def main():
    conn = get_connection()
    if not conn:
        return

    while True:
        show_menu()
        choice = input("Enter option: ").strip()
        if choice == "1":
            query_top_hitters_by_year(conn)
        elif choice == "2":
            query_above_threshold(conn)
        elif choice == "3":
            query_players_by_team(conn)
        elif choice == "4":
            print("Bye!")
            break
        else:
            print("Invalid choice. Try again.")

    conn.close()

if __name__ == "__main__":
    main()
