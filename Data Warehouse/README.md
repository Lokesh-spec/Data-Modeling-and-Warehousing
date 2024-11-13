# Data Warehouse Project

This project involves designing a data warehouse schema for a retail environment with a focus on movies, customers, stores, and sales transactions. It includes creating dimension and fact tables, populating them with data, and running optimized queries for reporting and analytics.


## Table of Contents
- [Schema Overview](#schema-overview)
    - [Date Dimension Table](#date-dimension-table)
    - [Movie Dimension Table](#movie-dimension-table)
    - [Customer Dimension Table](#customer-dimension-table)
    - [Store Dimension Table](#store-dimension-table)
    - [Sales Fact Table](#sales-fact-table)
- [Data Insertion](#data-insertion)
    - [Populating Date Dimension](#populating-date-dimension)
    - [Populating Customer Dimension](#populating-customer-dimension)
    - [Populating Movie Dimension](#populating-movie-dimension)
    - [Populating Store Dimension](#populating-store-dimension)
    - [Populating Sales Fact Table](#populating-sales-fact-table)
- [Sample Queries](#sample-queries)
    - [Direct Query on Source Tables](#direct-query-on-source-tables)
    - [Optimized Query on Fact and Dimension Tables](#optimized-query-on-fact-and-dimension-tables)

- [Conclusion](#conclusion)


## Schema Overview

The data warehouse schema follows a star schema with dimension tables for date, movie, customer, and store, and a sales_fact table that links these dimensions with transactional data.

### Date Dimension Table

The date_dim table stores various attributes of the date, enabling time-based analytics like year, quarter, month, and weekend analysis.

``` sql 
CREATE TABLE IF NOT EXISTS date_dim (
    date_key INTEGER PRIMARY KEY,
    date DATE NOT NULL,
    year SMALLINT NOT NULL,
    quarter SMALLINT NOT NULL,
    month SMALLINT NOT NULL,
    week SMALLINT NOT NULL,
    day SMALLINT NOT NULL,
    is_weekend BOOLEAN
);
```

### Movie Dimension Table

The movie_dim table provides movie-related details, enabling analysis based on title, genre, language, and ratings.

``` sql
CREATE TABLE IF NOT EXISTS movie_dim (
    movie_key INTEGER PRIMARY KEY,
    film_id SMALLINT NOT NULL,
    title VARCHAR NOT NULL,
    description TEXT NOT NULL,
    language VARCHAR NOT NULL,
    length SMALLINT NOT NULL,
    rating mpaa_rating,
    special_features VARCHAR
);
```

### Customer Dimension Table

The customer_dim table provides information about customers, enabling customer segmentation based on location and activity.

``` sql
CREATE TABLE IF NOT EXISTS customer_dim (
    customer_key SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR,
    address VARCHAR(50) NOT NULL,
    address2 VARCHAR(50),
    district VARCHAR(50) NOT NULL,
    city VARCHAR(50) NOT NULL,
    country VARCHAR(50) NOT NULL,
    postal_code VARCHAR(50),
    phone VARCHAR(50) NOT NULL,
    active SMALLINT NOT NULL,
    create_date DATE NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL
);
```

### Store Dimension Table

The store_dim table stores details about store locations and their managers, enabling regional sales analysis.

``` sql
CREATE TABLE IF NOT EXISTS store_dim (
    store_key SMALLINT PRIMARY KEY,
    store_id SMALLINT NOT NULL,
    address VARCHAR(50) NOT NULL,
    address2 VARCHAR(50),
    district VARCHAR(20) NOT NULL,
    city VARCHAR(20) NOT NULL,
    country VARCHAR(20) NOT NULL,
    postal_code VARCHAR(20),
    manager_first_name VARCHAR NOT NULL,
    manager_last_name VARCHAR NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL
);
```

### Sales Fact Table

The sales_fact table stores transactional data, with foreign keys linking to each dimension table.

``` sql
CREATE TABLE IF NOT EXISTS sales_fact (
    sales_key SERIAL PRIMARY KEY,
    date_key INTEGER REFERENCES date_dim(date_key),
    customer_key INTEGER REFERENCES customer_dim(customer_key),
    movie_key INTEGER REFERENCES movie_dim(movie_key),
    store_key SMALLINT REFERENCES store_dim(store_key),
    sales_amount INTEGER
);
```

## Data Insertion

### Populating Date Dimension

The date_dim table is populated with distinct date values extracted from the payment source table.

``` sql
INSERT INTO date_dim (date_key, date, year, quarter, month, week, day, is_weekend)
SELECT DISTINCT TO_CHAR(DATE(payment_date), 'YYYYMMDD')::INTEGER AS date_key,
       DATE(payment_date) as date, 
       EXTRACT(YEAR FROM payment_date) as year,
       EXTRACT(QUARTER FROM payment_date) as quarter, 
       EXTRACT(MONTH FROM payment_date) as month,
       EXTRACT(WEEK FROM payment_date) as week, 
       EXTRACT(DAY FROM payment_date) as day,
       EXTRACT(DOW FROM payment_date) IN (0, 6) as is_weekend
FROM payment;
```

### Populating Customer Dimension

The customer_dim table is populated by joining customer, address, city, and country tables.

``` sql 
INSERT INTO customer_dim (customer_key, first_name, last_name, email, address, address2, district, city, country, postal_code, phone, active, create_date, start_date, end_date)
SELECT customer_id as customer_key,
       first_name, last_name, email,
       a.address, a.address2, a.district, ci.city, co.country, a.postal_code, a.phone,
       c.active, c.create_date, NOW(), NOW()
FROM customer c
JOIN address a on a.address_id = c.address_id
JOIN city ci on a.city_id = ci.city_id
JOIN country co on co.country_id = ci.country_id;
```

### Populating Movie Dimension

The movie_dim table is populated with data from the film and language tables.

``` sql
INSERT INTO movie_dim (movie_key, film_id, title, description, language, length, rating, special_features)
SELECT f.film_id as movie_key, 
       f.film_id, f.title, 
       f.description, l.name, 
       f.length, 
       f.rating, 
       f.special_features
FROM film f
JOIN language l on l.language_id = f.language_id;
```

### Populating Store Dimension

The store_dim table is populated by joining the store, address, city, country, and staff tables.

``` sql
INSERT INTO store_dim (store_key, store_id, address, address2, district, city, country, postal_code, manager_first_name, manager_last_name, start_date, end_date)
SELECT s.store_id as store_key, 
       s.store_id, 
       a.address, 
       a.address2, 
       a.district, 
       ci.city, 
       co.country, 
       a.postal_code, 
       st.first_name, 
       st.last_name, 
       now(), 
       now()
FROM store s
JOIN address a on a.address_id = s.address_id
JOIN city ci on ci.city_id = a.city_id
JOIN country co on co.country_id = ci.country_id
JOIN staff st on st.store_id = s.store_id;
```

### Populating Sales Fact Table

The sales_fact table is populated by joining payment, rental, and inventory tables.

``` sql
INSERT INTO sales_fact (date_key, customer_key, movie_key, store_key, sales_amount)
SELECT TO_CHAR(DATE(p.payment_date), 'YYYYMMDD')::INTEGER AS date_key,
       p.customer_id, 
       i.film_id, 
       i.store_id, 
       p.amount
FROM payment p
JOIN rental r ON r.rental_id = p.rental_id
JOIN inventory i ON i.inventory_id = r.inventory_id;
```

## Sample Queries

### Direct Query on Source Tables

This query calculates total monthly sales per store directly on source tables.
**Execution Time: 122 ms**

``` sql 
SELECT EXTRACT(YEAR FROM payment.payment_date) AS year,
       EXTRACT(MONTH FROM payment.payment_date) AS month,
       store.store_id,
       SUM(payment.amount) AS total_sales
FROM payment
JOIN rental ON payment.rental_id = rental.rental_id
JOIN inventory ON rental.inventory_id = inventory.inventory_id
JOIN store ON inventory.store_id = store.store_id
GROUP BY year, month, store.store_id
ORDER BY year, month, store.store_id;
```
![Direct query From Source](images\Direct_query_from_source_table.png)

### Optimized Query on Fact and Dimension Tables

This query calculates total monthly sales per store using pre-joined fact and dimension tables for better performance.
**Execution Time: 70 ms**

``` sql
SELECT dd.year, 
       dd.month, 
       sd.store_id, 
       SUM(sf.sales_amount) AS total_sales
FROM sales_fact sf
JOIN date_dim dd ON sf.date_key = dd.date_key
JOIN store_dim sd ON sf.store_key = sd.store_key
GROUP BY dd.year, dd.month, sd.store_id
ORDER BY dd.year, dd.month, sd.store_id;
```

![Optimized query from Data warehouse](images\Optimized_query.png)

The optimized fact-dimension schema significantly improves query performance, reducing execution time by over 40%.

## Conclusion

This data warehouse project demonstrates how to structure and query data using a star schema model, facilitating improved data analysis and reporting. The schema optimizations provided notable performance gains, especially for complex analytical queries.






