SET FOREIGN_KEY_CHECKS = 0;

ALTER TABLE `compfie_knowledge`.`tbl_industries`
CHANGE COLUMN `industry_id` `industry_id` INT(11) NOT NULL AUTO_INCREMENT ;


ALTER TABLE `compfie_knowledge`.`tbl_statutory_natures`
CHANGE COLUMN `statutory_nature_id` `statutory_nature_id` INT(11) NOT NULL AUTO_INCREMENT ;
