DELIMITER !
CREATE FUNCTION determineSalary(salary decimal(10,2))
RETURNS varchar(100)
DETERMINISTIC
BEGIN
    DECLARE result varchar(100);
    
    IF salary IS NULL THEN        
        SET result = 'Unknown';
    END IF;
    IF salary > (80 * 1000) then
		set result = 'High';
    end if;
    IF salary >= (40 * 1000) and salary <= (80 * 1000) then
		set result = 'Medium';
    end if;
    IF salary < (40 * 1000) then
		set result = 'Low';
    end if;
    RETURN result;
END !
DELIMITER ;