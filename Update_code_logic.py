import logging
import sqlite3
import pandas as pd


def update_table():
    """""
    This function updates the database table with new data from a csv file
    and logs the changes made to the table.

    - If the name already exists in the table, the function will update the age and city columns
    - If the name does not exist in the table, the function will insert the name, age and city into the table
    - The function will log the changes made to the table
    
    """

    # Set up the logging configuration
    logging.basicConfig(
        filename='update_table.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    # Boolean to check if the data was updated
    is_data_updated = False

    # List to store the names of the updated rows
    updated_rows = []


    try:
        logging.info('Initiating database table update...')
    
        # Set up the database connection, cursor and csv file
        df = pd.read_csv('Kunskapskontroll_2_1.csv')
        
        connection = sqlite3.connect('kunskaps_databas.db')
        db_cursor = connection.cursor()


        # Operations to update the table
        for index, row in df.iterrows():
            db_cursor.execute(''' 
            SELECT COUNT(*) FROM people WHERE name = ?;
            ''', (row['name'],))
    
            name_exists = db_cursor.fetchone()[0]

            if name_exists > 0:
                db_cursor.execute('''
                SELECT age, city FROM people WHERE name = ?;
                ''', (row['name'],))
                result = db_cursor.fetchone()

                if result:
                    db_age, db_city = result
                    if ((row['age'], row['city']) != (db_age, db_city)):
                       db_cursor.execute(''' 
                        UPDATE people
                        SET age = ?, city = ?
                        WHERE name = ?;
                        ''', (row['age'], row['city'], row['name']))
                       logging.info(f"Updated new data for: {row['name']}")
                       updated_rows.append(row['name']) 
                       is_data_updated = True

            else:
                db_cursor.execute('''
                INSERT INTO people (name, age, city)
                VALUES(?, ? ,?);
                ''',(row['name'], row['age'], row['city']))
                logging.info(f"Inserted new data for {row['name']}")
                updated_rows.append(row['name']) 
                is_data_updated = True


        if updated_rows:

            # Create placeholders for the updated rows
            placeholders = ', '.join('?' for _ in updated_rows)  
            db_cursor.execute(f'''
            SELECT * FROM people WHERE name IN ({placeholders});
            ''', tuple(updated_rows))
            updated_data_view = db_cursor.fetchall()
            logging.info(f"Updated or new rows:\n{updated_data_view}")
        

        connection.commit()
        connection.close()

        # Log the status of the table update operation
        if not is_data_updated:
            logging.info('No new data or updates were made, database is up-to-date')
        else:
            logging.info('Table updated successfully')

    except Exception as e:
        logging.error(f"Error have occurred: {e}", exc_info=True)