import mysql.connector


yhteys = mysql.connector.connect(
    host='127.0.0.1',
    port=3306,
    database='flight_game',
    user='root',
    password='Maria1/26!',
    autocommit=True
)


def move_and_get_name(game_id, airport_ident):
    cursor = yhteys.cursor()

    # päivitetään pelaajan lokaatio
    update_sql = "UPDATE game SET location = %s WHERE id = %s"
    cursor.execute(update_sql, (airport_ident, game_id))

    # haetaan nimi airport taulusta
    select_sql = "SELECT name FROM airport WHERE ident = %s"
    cursor.execute(select_sql, (airport_ident,))
    result = cursor.fetchone()

    cursor.close()

    if result:
        return result[0]
    return "tietämätön lentokenttä"



if __name__ == "__main__":
    target_id = 1
    target_airport = 'EFHK'

    airport_name = move_and_get_name(target_id, target_airport)
    print(f" Olet paikassa: {airport_name}")