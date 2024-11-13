import psycopg2
from typing import List, Tuple

class Extract:
    def __init__(self, db_manager: "PostgreSQLManager"): # type: ignore
        self.db_manager = db_manager

    def extract_customer_data(self) -> List[Tuple]:
        """Extract customer data from the database."""
        customer_query = """
            SELECT customer_id as customer_key,
                first_name,
                last_name,
                email,
                a.address,
                a.address2,
                a.district,
                ci.city,
                co.country,
                a.postal_code,
                a.phone,
                c.active,
                c.create_date,
                NOW() as start_date,
                NOW() as end_date
            FROM customer c
            JOIN address a on a.address_id = c.address_id
            JOIN city ci on a.city_id = ci.city_id
            JOIN country co on co.country_id = ci.country_id;
        """
        try:
            return self.db_manager.select_query(customer_query)
        except Exception as e:
            print(f"Error extracting customer data: {e}")
            return []

    def extract_store_data(self) -> List[Tuple]:
        """Extract store data from the database."""
        store_query = """
            SELECT s.store_id as store_key,
                s.store_id,
                a.address,
                a.address2,
                a.district,
                ci.city,
                co.country,
                a.postal_code,
                st.first_name as manager_first_name,
                st.last_name as manager_last_name,
                now() as start_date,
                now() as end_date
            FROM store s
            JOIN address a on a.address_id = s.address_id
            JOIN city ci on ci.city_id = a.city_id
            JOIN country co on co.country_id = ci.country_id
            JOIN staff st on st.store_id = s.store_id;
        """
        try:
            return self.db_manager.select_query(store_query)
        except Exception as e:
            print(f"Error extracting store data: {e}")
            return []

    def extract_payment_data(self) -> List[Tuple]:
        """Extract payment data from the database."""
        payment_query = """
            SELECT 
                TO_CHAR(DATE(p.payment_date), 'YYYYMMDD')::INTEGER AS date_key,
                p.customer_id AS customer_key,
                i.film_id AS movie_key,
                i.store_id AS store_key,
                p.amount AS payment_amount
            FROM payment p
            JOIN rental r ON r.rental_id = p.rental_id
            JOIN inventory i ON i.inventory_id = r.inventory_id;
        """
        try:
            return self.db_manager.select_query(payment_query)
        except Exception as e:
            print(f"Error extracting payment data: {e}")
            return []
        
    def extract_movie_data(self) -> List[Tuple]:
        """Extract movie data from the database."""
        movie_query = """
            SELECT m.movie_id as movie_key,
                m.title,
                m.description,
                l.name as language,
                m.length,
                m.rating,
                m.special_features
            FROM movie m
            JOIN language l on m.language_id = l.language_id;
        """
        try:
            return self.db_manager.select_query(movie_query)
        except Exception as e:
            print(f"Error extracting movie data: {e}")
            return []
