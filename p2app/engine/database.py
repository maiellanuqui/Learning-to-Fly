from pathlib import Path
import sqlite3


def is_database(db_file: Path) -> bool:
    """Checks if the given file is an applicable database.
        Returns True if file is a database
        Returns False if file is not a database
    """
    try:
        con = sqlite3.connect(db_file)
        cur = con.execute("""
                PRAGMA foreign_keys = ON;
                """)
        cur.close()
        return True

    except:
        return False

def read_db(db_file: Path, statement, params) -> list:
    """Returns given data obtained from the sql statement and parameters"""
    result = []
    con = sqlite3.connect(db_file)
    con.execute("""
            PRAGMA foreign_keys = ON;
            """)
    cur = con.execute(statement, tuple(params))
    res = cur.fetchone()
    while res is not None:
        result.append(res)
        res = cur.fetchone()
    cur.close()

    return result
def is_editable(db_file: Path, statement, params) -> bool:
    """Checks if an edit to the database was able to commit.
        Returns True if edit was made
        Returns False if no edit was made
    """
    con = sqlite3.connect(db_file)
    con.execute("""
                PRAGMA foreign_keys = ON;
                """)
    try:
        con.execute(statement, tuple(params))
        con.commit()
        con.close()
        return True

    except:
        con.close()
        return False

