DELIMITER !
CREATE FUNCTION calculateAge(birthdate date)
RETURNS int
DETERMINISTIC
BEGIN
    DECLARE age int default 0;
    DECLARE y int default 0;
    declare n int default 0;
    IF birthdate IS NULL THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'birthdate is null';
    END IF;
    SELECT EXTRACT(YEAR FROM birthdate) INTO y;
    select extract(YEAR FrOM now()) INTO n;
    SET age = n - y;
    RETURN age;
END !
DELIMITER ;