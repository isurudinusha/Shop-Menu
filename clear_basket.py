from view_basket import basket

def clear_basket(db, cursor, shopper_id):
    """
    It clears the basket of a shopper
    
    :param db: the database connection
    :param cursor: the cursor object
    :param shopper_id: the id of the shopper whose basket you want to clear
    """
    select_baskets = """
        SELECT basket_id 
        FROM shopper_baskets
        WHERE shopper_id = ?
        """
    cursor.execute(
        select_baskets,
        (shopper_id,),
    )
    baskets = cursor.fetchall()

    for basket_data in baskets:

        delete_contents = """
            DELETE FROM basket_contents
            WHERE basket_id = ?
            """
        cursor.execute(
            delete_contents,
            (basket_data[0],),
        )
        db.commit()

    delete_baskets = """
        DELETE FROM shopper_baskets
        WHERE shopper_id = ?
        """
    cursor.execute(
        delete_baskets,
        (shopper_id,),
    )
    db.commit()

    print("\nBasket cleard successfully!")


def checkout_clear(db, cursor, shopper_id):
    clear_basket(db, cursor, shopper_id)


def delete(db, cursor, shopper_id):
    if basket(db, cursor, shopper_id):
        clear_basket(db, cursor, shopper_id)
