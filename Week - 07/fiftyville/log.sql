-- Keep a log of any SQL queries you execute as you solve the mystery.

-- the crime took place on July 28th, 2024 on humpfrey street


SELECT *
FROM crime_scene_reports
WHERE year = 2024 and month = 7 and day = 28;

+-----+------+-------+-----+-----------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| id  | year | month | day |     street      |                                                                                                       description                                                                                                        |
+-----+------+-------+-----+-----------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 293 | 2024 | 7     | 28  | Axmark Road     | Vandalism took place at 12:04. No known witnesses.                                                                                                                                                                       |
| 294 | 2024 | 7     | 28  | Boyce Avenue    | Shoplifting took place at 03:01. Two people witnessed the event.                                                                                                                                                         |
| 295 | 2024 | 7     | 28  | Humphrey Street | Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery. Interviews were conducted today with three witnesses who were present at the time – each of their interview transcripts mentions the bakery. |
| 296 | 2024 | 7     | 28  | Widenius Street | Money laundering took place at 20:30. No known witnesses.                                                                                                                                                                |
| 297 | 2024 | 7     | 28  | Humphrey Street | Littering took place at 16:36. No known witnesses.                                                                                                                                                                       |
+-----+------+-------+-----+-----------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

SELECT *
FROM bakery_security_logs
WHERE year = 2024 and month = 7 and day = 28 and hour = 10;

+-----+------+-------+-----+------+--------+----------+---------------+
| id  | year | month | day | hour | minute | activity | license_plate |
+-----+------+-------+-----+------+--------+----------+---------------+
| 258 | 2024 | 7     | 28  | 10   | 8      | entrance | R3G7486       |
| 259 | 2024 | 7     | 28  | 10   | 14     | entrance | 13FNH73       |
| 260 | 2024 | 7     | 28  | 10   | 16     | exit     | 5P2BI95       |
| 261 | 2024 | 7     | 28  | 10   | 18     | exit     | 94KL13X       |
| 262 | 2024 | 7     | 28  | 10   | 18     | exit     | 6P58WS2       |
| 263 | 2024 | 7     | 28  | 10   | 19     | exit     | 4328GD8       |
| 264 | 2024 | 7     | 28  | 10   | 20     | exit     | G412CB7       |
| 265 | 2024 | 7     | 28  | 10   | 21     | exit     | L93JTIZ       |
| 266 | 2024 | 7     | 28  | 10   | 23     | exit     | 322W7JE       |
| 267 | 2024 | 7     | 28  | 10   | 23     | exit     | 0NTHK55       |
| 268 | 2024 | 7     | 28  | 10   | 35     | exit     | 1106N58       |
| 269 | 2024 | 7     | 28  | 10   | 42     | entrance | NRYN856       |
| 270 | 2024 | 7     | 28  | 10   | 44     | entrance | WD5M8I6       |
| 271 | 2024 | 7     | 28  | 10   | 55     | entrance | V47T75I       |
+-----+------+-------+-----+------+--------+----------+---------------+

SELECT *
FROM interviews
WHERE year = 2024 and month = 7 and day = 28;

+-----+---------+------+-------+-----+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| id  |  name   | year | month | day |                                                                                                                                                     transcript                                                                                                                                                      |
+-----+---------+------+-------+-----+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 158 | Jose    | 2024 | 7     | 28  | “Ah,” said he, “I forgot that I had not seen you for some weeks. It is a little souvenir from the King of Bohemia in return for my assistance in the case of the Irene Adler papers.”                                                                                                                               |
| 159 | Eugene  | 2024 | 7     | 28  | “I suppose,” said Holmes, “that when Mr. Windibank came back from France he was very annoyed at your having gone to the ball.”                                                                                                                                                                                      |
| 160 | Barbara | 2024 | 7     | 28  | “You had my note?” he asked with a deep harsh voice and a strongly marked German accent. “I told you that I would call.” He looked from one to the other of us, as if uncertain which to address.                                                                                                                   |
| 161 | Ruth    | 2024 | 7     | 28  | Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away. If you have security footage from the bakery parking lot, you might want to look for cars that left the parking lot in that time frame.                                                          |
| 162 | Eugene  | 2024 | 7     | 28  | I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at Emma''s bakery, I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.                                                                                                 |
| 163 | Raymond | 2024 | 7     | 28  | As the thief was leaving the bakery, they called someone who talked to them for less than a minute. In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow. The thief then asked the person on the other end of the phone to purchase the flight ticket. |
| 191 | Lily    | 2024 | 7     | 28  | Our neighboring courthouse has a very annoying rooster that crows loudly at 6am every day. My sons Robert and Patrick took the rooster to a city far, far away, so it may never bother us again. My sons have successfully arrived in Paris.                                                                        |
+-----+---------+------+-------+-----+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

SELECT *
FROM atm_transactions
WHERE year = 2024 AND month = 7 AND day = 28 AND atm_location LIKE 'Legget%' AND transaction_type like 'withdraw%';

+-----+----------------+------+-------+-----+----------------+------------------+--------+
| id  | account_number | year | month | day |  atm_location  | transaction_type | amount |
+-----+----------------+------+-------+-----+----------------+------------------+--------+
| 246 | 28500762       | 2024 | 7     | 28  | Leggett Street | withdraw         | 48     |
| 264 | 28296815       | 2024 | 7     | 28  | Leggett Street | withdraw         | 20     |
| 266 | 76054385       | 2024 | 7     | 28  | Leggett Street | withdraw         | 60     |
| 267 | 49610011       | 2024 | 7     | 28  | Leggett Street | withdraw         | 50     |
| 269 | 16153065       | 2024 | 7     | 28  | Leggett Street | withdraw         | 80     |
| 288 | 25506511       | 2024 | 7     | 28  | Leggett Street | withdraw         | 20     |
| 313 | 81061156       | 2024 | 7     | 28  | Leggett Street | withdraw         | 30     |
| 336 | 26013199       | 2024 | 7     | 28  | Leggett Street | withdraw         | 35     |
+-----+----------------+------+-------+-----+----------------+------------------+--------+

SELECT flights.id, flights.day, flights.hour, flights.minute,
    OA.city AS origin_city,           -- Select the origin city
    DA.city AS destination_city       -- Select the destination city
FROM flights
-- Join for ORIGIN airport and alias it OA
JOIN airports AS OA ON flights.origin_airport_id = OA.id
-- Join for DESTINATION airport and alias it DA
JOIN airports AS DA ON flights.destination_airport_id = DA.id
WHERE
    flights.day > 28
    AND OA.city = 'Fiftyville'
ORDER BY
    flights.day, flights.hour, flights.minute;

+----+-----+------+--------+-------------+------------------+
| id | day | hour | minute | origin_city | destination_city |
+----+-----+------+--------+-------------+------------------+
| 36 | 29  | 8    | 20     | Fiftyville  | New York City    |
| 43 | 29  | 9    | 30     | Fiftyville  | Chicago          |
| 23 | 29  | 12   | 15     | Fiftyville  | San Francisco    |
| 53 | 29  | 15   | 20     | Fiftyville  | Tokyo            |
| 18 | 29  | 16   | 0      | Fiftyville  | Boston           |
| 54 | 30  | 10   | 19     | Fiftyville  | Dallas           |
| 11 | 30  | 13   | 7      | Fiftyville  | Delhi            |
| 44 | 30  | 13   | 19     | Fiftyville  | Los Angeles      |
| 10 | 30  | 13   | 55     | Fiftyville  | New York City    |
| 7  | 30  | 18   | 5      | Fiftyville  | Chicago          |
| 31 | 30  | 20   | 21     | Fiftyville  | Los Angeles      |
| 8  | 30  | 20   | 56     | Fiftyville  | Beijing          |
+----+-----+------+--------+-------------+------------------+

SELECT DISTINCT people.name
FROM people
JOIN bakery_security_logs
    ON people.license_plate = bakery_security_logs.license_plate
JOIN bank_accounts
    ON people.id = bank_accounts.person_id
JOIN atm_transactions
    ON bank_accounts.account_number = atm_transactions.account_number
WHERE
    -- 1. Vehicle Exit Criteria (10:16 - 10:25 AM)
    bakery_security_logs.year = 2024
    AND bakery_security_logs.month = 7
    AND bakery_security_logs.day = 28
    AND bakery_security_logs.hour = 10
    AND bakery_security_logs.minute BETWEEN 16 AND 25
    AND bakery_security_logs.activity = 'exit'
    -- 2. ATM Transaction Criteria (Leggett St. Withdrawal)
    AND atm_transactions.year = 2024
    AND atm_transactions.month = 7
    AND atm_transactions.day = 28
    AND atm_transactions.atm_location = 'Leggett Street'
    AND atm_transactions.transaction_type = 'withdraw';

+-------+
| name  |
+-------+
| Luca  |
| Bruce |
| Iman  |
| Diana |
+-------+

SELECT people.name
FROM people
JOIN passengers
    ON people.passport_number = passengers.passport_number
WHERE passengers.flight_id = 36;

+--------+
|  name  |
+--------+
| Doris  |
| Sofia  |
| Bruce  |
| Edward |
| Kelsey |
| Taylor |
| Kenny  |
| Luca   |
+--------+

SELECT people.name
FROM people
JOIN phone_calls
    ON people.phone_number = phone_calls.caller
WHERE
    phone_calls.year = 2024
    AND phone_calls.month = 7
    AND phone_calls.day = 28
    AND phone_calls.duration < 60;

+---------+
|  name   |
+---------+
| Sofia   |
| Kelsey  |
| Bruce   |
| Kelsey  |
| Taylor  |
| Diana   |
| Carina  |
| Kenny   |
| Benista |
+---------+

SELECT name
FROM people
WHERE phone_number = (
    -- Find the name linked to the receiver's phone number
    SELECT receiver
    FROM phone_calls
    WHERE caller = (
        -- 1. Find Bruce's phone number
        SELECT phone_number
        FROM people
        WHERE name = 'Bruce'
    )
    -- Match the specific call details
    AND year = 2024
    AND month = 7
    AND day = 28
    AND duration < 60
);
