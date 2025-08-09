DELIMITER !
CREATE FUNCTION calculateBonus(salary decimal(10,2), bonus double)
RETURNS decimal(10,2)
DETERMINISTIC
BEGIN
    DECLARE amount decimal(10,2) default 0;
    IF salary < 0 OR salary IS NULL THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Salary is null or negative';
    END IF;
    IF bonus < 0 OR bonus IS NULL THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Bonus is null or negative';
    END IF;
    SET amount = salary * bonus;
    RETURN amount;
END !
DELIMITER ;