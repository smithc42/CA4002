CREATE TABLE FLIGHTS (
    id INT NOT NULL AUTO_INCREMENT,
    scrape_time TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    ORIGIN VARCHAR(50),
    FLIGHT_NUMBER VARCHAR(50),
    AIRLINE VARCHAR(50),
    ARRIVAL_SCHEDULED VARCHAR(50),
    ARRIVAL_ACTUAL VARCHAR(50),
    GATE VARCHAR(50),
    STATUS VARCHAR(50),
    EQUIPMENT VARCHAR(50)
)