
--
-- Triggers `tbl_client_groups`
--

DROP TRIGGER IF EXISTS `after_tbl_client_groups_update`;

DELIMITER //
CREATE TRIGGER `after_tbl_client_groups_update` AFTER UPDATE ON `tbl_client_groups`
 FOR EACH ROW BEGIN
   SET @action = 1;
   SET @save = 0;

    IF OLD.email_id <> NEW.email_id THEN
       INSERT INTO tbl_audit_log(action,
                                 client_id,
                                 legal_entity_id,
                                 tbl_auto_id,
                                 column_name,
                                 value,
                                 tbl_name)
            VALUES (@action,
                    NEW.client_id,
                    0,
                    NEW.client_id,
                    'email_id',
                    NEW.email_id,
                    'tbl_client_groups');
        UPDATE tbl_client_replication_status set is_new_data = 1
        WHERE client_id = NEW.client_id and is_group = 1;

        UPDATE tbl_legal_entities set is_approved = 0, approved_by = null, approved_on = null
        WHERE client_id = NEW.client_id;

    END IF;
    IF OLD.total_view_licence <> NEW.total_view_licence THEN
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             legal_entity_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                0,
                NEW.client_id,
                'total_view_licence',
                NEW.total_view_licence,
                'tbl_client_groups');
        UPDATE tbl_client_replication_status set is_new_data = 1
        WHERE client_id = NEW.client_id and is_group = 1;

        UPDATE tbl_legal_entities set is_approved = 0, approved_by = null, approved_on = null
        WHERE client_id = NEW.client_id;

    END IF;

    INSERT INTO tbl_client_groups_history(
                             client_id,
                             email_id,
                             total_view_licence,
                             remarks,
                             updated_by,
                             updated_on)
        VALUES (OLD.client_id,
                OLD.email_id,
                OLD.total_view_licence,
                OLD.remarks,
                OLD.updated_by,
                OLD.updated_on);


END
//
DELIMITER ;

DROP TRIGGER IF EXISTS `after_tbl_client_groups_insert`;

DELIMITER //
CREATE TRIGGER `after_tbl_client_groups_insert` AFTER INSERT ON `tbl_client_groups`
 FOR EACH ROW BEGIN
   SET @action = 0;
   SET @save = 0;

    INSERT INTO tbl_audit_log(action,
                         client_id,
                         legal_entity_id,
                         tbl_auto_id,
                         column_name,
                         value,
                         tbl_name)
        VALUES (@action,
                NEW.client_id,
                0,
                NEW.client_id,
                'group_name',
                NEW.group_name,
                'tbl_client_groups');

   INSERT INTO tbl_audit_log(action,
                             client_id,
                             legal_entity_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                0,
                NEW.client_id,
                'short_name',
                NEW.short_name,
                'tbl_client_groups');
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             legal_entity_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                0,
                NEW.client_id,
                'email_id',
                NEW.email_id,
                'tbl_client_groups');
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             legal_entity_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                0,
                NEW.client_id,
                'total_view_licence',
                NEW.total_view_licence,
                'tbl_client_groups');

    INSERT INTO tbl_client_replication_status (client_id, is_new_data, is_group)
    values(new.client_id, 0, 1);

END
//
DELIMITER ;

-- ------
-- client_configuration_insert
-- ------

DROP TRIGGER IF EXISTS `after_tbl_client_configuration_insert`;
DELIMITER //
CREATE TRIGGER `after_tbl_client_configuration_insert` AFTER INSERT ON `tbl_client_configuration`
 FOR EACH ROW BEGIN
   SET @action = 0;

    INSERT INTO tbl_audit_log(action, client_id, legal_entity_id, tbl_auto_id, column_name, value, tbl_name)
        select @action, NEW.client_id, 0, cn_config_id, 'client_id' col_name, client_id value, 'tbl_client_configuration' from tbl_client_configuration
        where client_id = NEW.client_id
        union all
        select @action, NEW.client_id, 0, cn_config_id, 'country_id' col_name, country_id value, 'tbl_client_configuration' from tbl_client_configuration
        where client_id = NEW.client_id
        union all
        select @action, NEW.client_id, 0, cn_config_id, 'domain_id' col_name, domain_id value, 'tbl_client_configuration' from tbl_client_configuration
        where client_id = NEW.client_id
        union all
        select @action, NEW.client_id, 0, cn_config_id, 'month_from' col_name, month_from value, 'tbl_client_configuration' from tbl_client_configuration
        where client_id = NEW.client_id
        union all
        select @action, NEW.client_id, 0, cn_config_id, 'month_to' col_name, month_to value, 'tbl_client_configuration' from tbl_client_configuration
        where client_id = NEW.client_id

        order by cn_config_id, col_name;

    UPDATE tbl_legal_entities T01 
    INNER JOIN tbl_legal_entity_domains T02 ON T01.legal_entity_id = T02.legal_entity_id 
    INNER JOIN tbl_client_configuration T03 ON T01.client_id = T03.client_id AND T01.country_id = T03.country_id AND T02.domain_id = T03.domain_id
    SET is_approved = 0 
    WHERE T01.client_id = NEW.client_id and T01.country_id = NEW.country_id and T02.domain_id = NEW.domain_id
    AND T03.month_from <> NEW.month_from AND T03.month_to <> NEW.month_to;

END
//
DELIMITER ;

-- ------
-- client_configuration_update
-- ------

DROP TRIGGER IF EXISTS `after_tbl_client_configuration_update`;
DELIMITER //
CREATE TRIGGER `after_tbl_client_configuration_update` AFTER UPDATE ON `tbl_client_configuration`
FOR EACH ROW BEGIN
   SET @action = 0;

    INSERT INTO tbl_audit_log(action, client_id, legal_entity_id, tbl_auto_id, column_name, value, tbl_name)
        select @action, NEW.client_id, 0, cn_config_id, 'client_id' col_name, client_id value, 'tbl_client_configuration' from tbl_client_configuration
        where client_id = NEW.client_id
        union all
        select @action, NEW.client_id, 0, cn_config_id, 'country_id' col_name, country_id value, 'tbl_client_configuration' from tbl_client_configuration
        where client_id = NEW.client_id
        union all
        select @action, NEW.client_id, 0, cn_config_id, 'domain_id' col_name, domain_id value, 'tbl_client_configuration' from tbl_client_configuration
        where client_id = NEW.client_id
        union all
        select @action, NEW.client_id, 0, cn_config_id, 'month_from' col_name, month_from value, 'tbl_client_configuration' from tbl_client_configuration
        where client_id = NEW.client_id
        union all
        select @action, NEW.client_id, 0, cn_config_id, 'month_to' col_name, month_to value, 'tbl_client_configuration' from tbl_client_configuration
        where client_id = NEW.client_id

        order by cn_config_id, col_name;

        IF OLD.client_id = NEW.client_id and OLD.country_id = NEW.country_id and OLD.domain_id = NEW.domain_id and OLD.month_from <> NEW.month_from and OLD.month_to <> NEW.month_to THEN
            UPDATE tbl_legal_entities T01 INNER JOIN tbl_legal_entity_domains T02 ON T01.legal_entity_id = T02.legal_entity_id 
            SET is_approved = 0 
            WHERE T01.client_id = NEW.client_id and T01.country_id = NEW.country_id and T02.domain_id = NEW.domain_id;
        END IF;
END
//
DELIMITER ;

-- ------
-- business_groups
-- ------

DROP TRIGGER IF EXISTS `after_tbl_business_groups_insert`;
DELIMITER //
CREATE TRIGGER `after_tbl_business_groups_insert` AFTER INSERT ON `tbl_business_groups`
 FOR EACH ROW BEGIN
   SET @action = 0;


   INSERT INTO tbl_audit_log(action,
                             client_id,
                             legal_entity_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                0,
                NEW.business_group_id,
                'business_group_name',
                NEW.business_group_name,
                'tbl_business_groups');
    UPDATE tbl_client_replication_status set is_new_data = 1
    WHERE client_id = NEW.client_id and is_group = 1;
END
//
DELIMITER ;


DROP TRIGGER IF EXISTS `after_tbl_business_groups_update`;
DELIMITER //
CREATE TRIGGER `after_tbl_business_groups_update` AFTER UPDATE ON `tbl_business_groups`
 FOR EACH ROW BEGIN
   SET @action = 1;

   IF OLD.business_group_name <> NEW.business_group_name THEN
       INSERT INTO tbl_audit_log(action,
                                 client_id,
                                 legal_entity_id,
                                 tbl_auto_id,
                                 column_name,
                                 value,
                                 tbl_name)
            VALUES (@action,
                    NEW.client_id,
                    0,
                    NEW.business_group_id,
                    'business_group_name',
                    NEW.business_group_name,
                    'tbl_business_groups');
        UPDATE tbl_client_replication_status set is_new_data = 1
        WHERE client_id = NEW.client_id and is_group = 1;
    END IF ;
END
//
DELIMITER ;

-- ------------
-- legal entities
-- ------------

DROP TRIGGER IF EXISTS `after_tbl_legal_entities_insert`;
DELIMITER //
CREATE TRIGGER `after_tbl_legal_entities_insert` AFTER INSERT ON `tbl_legal_entities`
FOR EACH ROW BEGIN
    INSERT INTO tbl_client_replication_status (client_id, is_new_data, is_group) values(new.legal_entity_id, 0, 0);
END
//
DELIMITER ;


DROP TRIGGER IF EXISTS `after_tbl_legal_entities_update`;
DELIMITER //
CREATE TRIGGER `after_tbl_legal_entities_update` AFTER UPDATE ON `tbl_legal_entities`
 FOR EACH ROW BEGIN
   SET @action = 0;

    IF NEW.is_approved = 1 and NEW.is_created = 1 THEN
        INSERT INTO tbl_audit_log(action,
                                 client_id,
                                 legal_entity_id,
                                 tbl_auto_id,
                                 column_name,
                                 value,
                                 tbl_name)
            VALUES (@action,
                    NEW.client_id,
                    new.legal_entity_id,
                    NEW.legal_entity_id,
                    'legal_entity_name',
                    NEW.legal_entity_name,
                    'tbl_legal_entities');

        INSERT INTO tbl_audit_log(action,
                                 client_id,
                                 legal_entity_id,
                                 tbl_auto_id,
                                 column_name,
                                 value,
                                 tbl_name)
            VALUES (@action,
                    NEW.client_id,
                    new.legal_entity_id,
                    NEW.legal_entity_id,
                    'country_id',
                    NEW.country_id,
                    'tbl_legal_entities');

        INSERT INTO tbl_audit_log(action,
                                 client_id,
                                 legal_entity_id,
                                 tbl_auto_id,
                                 column_name,
                                 value,
                                 tbl_name)
            VALUES (@action,
                    NEW.client_id,
                    NEW.legal_entity_id,
                    NEW.legal_entity_id,
                    'business_group_id',
                    NEW.business_group_id,
                    'tbl_legal_entities');

        INSERT INTO tbl_audit_log(action,
                                 client_id,
                                 legal_entity_id,
                                 tbl_auto_id,
                                 column_name,
                                 value,
                                 tbl_name)
            VALUES (@action,
                    NEW.client_id,
                    NEW.legal_entity_id,
                    NEW.legal_entity_id,
                    'contract_from',
                    NEW.contract_from,
                    'tbl_legal_entities');

        INSERT INTO tbl_audit_log(action,
                                 client_id,
                                 legal_entity_id,
                                 tbl_auto_id,
                                 column_name,
                                 value,
                                 tbl_name)
            VALUES (@action,
                    NEW.client_id,
                    NEW.legal_entity_id,
                    NEW.legal_entity_id,
                    'contract_to',
                    NEW.contract_to,
                    'tbl_legal_entities');

        INSERT INTO tbl_audit_log(action,
                                 client_id,
                                 legal_entity_id,
                                 tbl_auto_id,
                                 column_name,
                                 value,
                                 tbl_name)
            VALUES (@action,
                    NEW.client_id,
                    NEW.legal_entity_id,
                    NEW.legal_entity_id,
                    'logo',
                    NEW.logo,
                    'tbl_legal_entities');

        INSERT INTO tbl_audit_log(action,
                                 client_id,
                                 legal_entity_id,
                                 tbl_auto_id,
                                 column_name,
                                 value,
                                 tbl_name)
            VALUES (@action,
                    NEW.client_id,
                    NEW.legal_entity_id,
                    NEW.legal_entity_id,
                    'logo_size',
                    NEW.logo_size,
                    'tbl_legal_entities');


        INSERT INTO tbl_audit_log(action,
                                 client_id,
                                 legal_entity_id,
                                 tbl_auto_id,
                                 column_name,
                                 value,
                                 tbl_name)
            VALUES (@action,
                    NEW.client_id,
                    NEW.legal_entity_id,
                    NEW.legal_entity_id,
                    'file_space_limit',
                    NEW.file_space_limit,
                    'tbl_legal_entities');

        INSERT INTO tbl_audit_log(action,
                                 client_id,
                                 legal_entity_id,
                                 tbl_auto_id,
                                 column_name,
                                 value,
                                 tbl_name)
            VALUES (@action,
                    NEW.client_id,
                    NEW.legal_entity_id,
                    NEW.legal_entity_id,
                    'total_licence',
                    NEW.total_licence,
                    'tbl_legal_entities');


        INSERT INTO tbl_audit_log(action,
                                 client_id,
                                 legal_entity_id,
                                 tbl_auto_id,
                                 column_name,
                                 value,
                                 tbl_name)
            VALUES (@action,
                    NEW.client_id,
                    NEW.legal_entity_id,
                    NEW.legal_entity_id,
                    'is_closed',
                    NEW.is_closed,
                    'tbl_legal_entities');

        INSERT INTO tbl_audit_log(action,
                                 client_id,
                                 legal_entity_id,
                                 tbl_auto_id,
                                 column_name,
                                 value,
                                 tbl_name)
            VALUES (@action,
                    NEW.client_id,
                    NEW.legal_entity_id,
                    NEW.legal_entity_id,
                    'closed_on',
                    NEW.closed_on,
                    'tbl_legal_entities');

        INSERT INTO tbl_audit_log(action,
                                 client_id,
                                 legal_entity_id,
                                 tbl_auto_id,
                                 column_name,
                                 value,
                                 tbl_name)
            VALUES (@action,
                    NEW.client_id,
                    NEW.legal_entity_id,
                    NEW.legal_entity_id,
                    'closed_by',
                    NEW.closed_by,
                    'tbl_legal_entities');

        INSERT INTO tbl_audit_log(action,
                                 client_id,
                                 legal_entity_id,
                                 tbl_auto_id,
                                 column_name,
                                 value,
                                 tbl_name)
            VALUES (@action,
                    NEW.client_id,
                    NEW.legal_entity_id,
                    NEW.legal_entity_id,
                    'closed_remarks',
                    NEW.closed_remarks,
                    'tbl_legal_entities');

        UPDATE tbl_client_replication_status set is_new_data = 1
        WHERE client_id = NEW.client_id and is_group = 1;

        INSERT INTO tbl_client_replication_status (client_id, is_new_data, is_group) values(new.legal_entity_id, 1, 0)
        on duplicate key update is_new_data = 1;

        -- legal entity domains insert

        INSERT INTO tbl_audit_log(action, client_id, legal_entity_id, tbl_auto_id, column_name, value, tbl_name)
        select @action, NEW.client_id, legal_entity_id, le_domain_id, 'legal_entity_id' col_name, legal_entity_id value, 'tbl_legal_entity_domains' from tbl_legal_entity_domains
        where legal_entity_id = NEW.legal_entity_id
        union all
        select @action, NEW.client_id, legal_entity_id, le_domain_id, 'domain_id' col_name, domain_id value, 'tbl_legal_entity_domains' from tbl_legal_entity_domains
        where legal_entity_id = NEW.legal_entity_id
        union all
        select @action, NEW.client_id, legal_entity_id, le_domain_id, 'activation_date' col_name, activation_date value, 'tbl_legal_entity_domains' from tbl_legal_entity_domains
        where legal_entity_id = NEW.legal_entity_id
        union all
        select @action, NEW.client_id, legal_entity_id, le_domain_id, 'organisation_id'  col_name, organisation_id value, 'tbl_legal_entity_domains' from tbl_legal_entity_domains
        where legal_entity_id = NEW.legal_entity_id
        union all
        select @action, NEW.client_id, legal_entity_id, le_domain_id,'count' col_name, count value, 'tbl_legal_entity_domains' from tbl_legal_entity_domains
        where legal_entity_id = NEW.legal_entity_id
        order by le_domain_id, col_name;

        INSERT INTO tbl_audit_log(action, client_id, legal_entity_id, tbl_auto_id, column_name, value, tbl_name)
        select @action, NEW.client_id, NEW.legal_entity_id, cn_config_id, 'client_id' col_name, client_id value, 'tbl_client_configuration' from tbl_client_configuration
        where client_id = NEW.client_id
        union all
        select @action, NEW.client_id, NEW.legal_entity_id, cn_config_id, 'country_id' col_name, country_id value, 'tbl_client_configuration' from tbl_client_configuration
        where client_id = NEW.client_id
        union all
        select @action, NEW.client_id, NEW.legal_entity_id, cn_config_id, 'domain_id' col_name, domain_id value, 'tbl_client_configuration' from tbl_client_configuration
        where client_id = NEW.client_id
        union all
        select @action, NEW.client_id, NEW.legal_entity_id, cn_config_id, 'month_from' col_name, month_from value, 'tbl_client_configuration' from tbl_client_configuration
        where client_id = NEW.client_id
        union all
        select @action, NEW.client_id, NEW.legal_entity_id, cn_config_id, 'month_to' col_name, month_to value, 'tbl_client_configuration' from tbl_client_configuration
        where client_id = NEW.client_id
        order by cn_config_id, col_name;

        INSERT INTO tbl_audit_log(action,client_id,legal_entity_id,tbl_auto_id,column_name,value,tbl_name)
        select distinct @action, NEW.client_id, legal_entity_id, t1.domain_id, 'domain_name' col_name,
            t1.domain_name, 'tbl_domains' from  tbl_domains as t1
            inner join tbl_legal_entity_domains as t2 on t1.domain_id = t2.domain_id
            where t2.legal_entity_id = NEW.legal_entity_id;


        INSERT INTO tbl_audit_log(action,client_id,legal_entity_id,tbl_auto_id,column_name,value,tbl_name)
        select distinct @action, NEW.client_id, legal_entity_id, t1.country_id, 'country_name' col_name,
            t1.country_name, 'tbl_countries' from  tbl_countries as t1
            inner join tbl_legal_entities as t2 on t1.country_id = t2.country_id
            where t2.legal_entity_id = NEW.legal_entity_id;

        IF OLD.business_group_id <> NEW.business_group_id THEN
           INSERT INTO tbl_audit_log(action,
                                     client_id,
                                     legal_entity_id,
                                     tbl_auto_id,
                                     column_name,
                                     value,
                                     tbl_name)
                select 1, NEW.client_id, NEW.legal_entity_id,
                    business_group_id, 'business_group_name',
                    business_group_name from tbl_business_groups
                    where ifnull(business_group_id,0) = new.business_group_id;
        END IF ;

   END IF ;

   INSERT INTO tbl_legal_entity_contract_history (
                             legal_entity_id,
                             client_id,
                             business_group_id,
                             legal_entity_name,
                             contract_from,
                             contract_to,
                             logo,
                             file_space_limit,
                             total_licence)
        VALUES (OLD.legal_entity_id,
                OLD.client_id,
                OLD.business_group_id,
                OLD.legal_entity_name,
                OLD.contract_from,
                OLD.contract_to,
                OLD.logo,
                OLD.file_space_limit,
                OLD.total_licence);

END
//
DELIMITER ;

DROP TRIGGER IF EXISTS `tbl_legal_entity_domains_BEFORE_DELETE`;

DELIMITER //

CREATE TRIGGER `tbl_legal_entity_domains_BEFORE_DELETE` BEFORE DELETE ON `tbl_legal_entity_domains` FOR EACH ROW
BEGIN

    INSERT INTO tbl_legal_entity_domains_history (
                             le_domain_id,
                             legal_entity_id,
                             domain_id,
                             activation_date,
                             organisation_id,
                             count)
        VALUES (OLD.le_domain_id,
                OLD.legal_entity_id,
                OLD.domain_id,
                OLD.activation_date,
                OLD.organisation_id,
                OLD.count);

END
//
DELIMITER ;


--
-- divisions
--

DROP TRIGGER IF EXISTS `after_tbl_divisions_insert`;
DELIMITER //
CREATE TRIGGER `after_tbl_divisions_insert` AFTER INSERT ON `tbl_divisions`
 FOR EACH ROW BEGIN
   SET @action = 0;

   INSERT INTO tbl_audit_log(action,
                             client_id,
                             legal_entity_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.legal_entity_id,
                NEW.division_id,
                'division_name',
                NEW.division_name,
                'tbl_divisions');

    INSERT INTO tbl_audit_log(action,
                             client_id,
                             legal_entity_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.legal_entity_id,
                NEW.division_id,
                'legal_entity_id',
                NEW.legal_entity_id,
                'tbl_divisions');

    INSERT INTO tbl_audit_log(action,
                             client_id,
                             legal_entity_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.legal_entity_id,
                NEW.division_id,
                'business_group_id',
                NEW.business_group_id,
                'tbl_divisions');

    UPDATE tbl_client_replication_status set is_new_data = 1
    WHERE client_id = NEW.client_id and is_group = 1;

    UPDATE tbl_client_replication_status set is_new_data = 1
    WHERE client_id = NEW.legal_entity_id and is_group = 0 ;

END
//
DELIMITER ;


--
-- categories
--

DROP TRIGGER IF EXISTS `after_tbl_categories_insert`;
DELIMITER //
CREATE TRIGGER `after_tbl_categories_insert` AFTER INSERT ON `tbl_categories`
 FOR EACH ROW BEGIN
   SET @action = 0;

   INSERT INTO tbl_audit_log(action,
                             client_id,
                             legal_entity_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.legal_entity_id,
                NEW.category_id,
                'category_name',
                NEW.category_name,
                'tbl_categories');

    INSERT INTO tbl_audit_log(action,
                             client_id,
                             legal_entity_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.legal_entity_id,
                NEW.category_id,
                'legal_entity_id',
                NEW.legal_entity_id,
                'tbl_categories');

    INSERT INTO tbl_audit_log(action,
                             client_id,
                             legal_entity_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.legal_entity_id,
                NEW.category_id,
                'business_group_id',
                NEW.business_group_id,
                'tbl_categories');

    INSERT INTO tbl_audit_log(action,
                             client_id,
                             legal_entity_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                NEW.client_id,
                NEW.legal_entity_id,
                NEW.category_id,
                'division_id',
                NEW.division_id,
                'tbl_categories');

    UPDATE tbl_client_replication_status set is_new_data = 1
    WHERE client_id = NEW.client_id and is_group = 1;

    UPDATE tbl_client_replication_status set is_new_data = 1
    WHERE client_id = NEW.legal_entity_id and is_group = 0 ;

END
//
DELIMITER ;


--
-- units
--


DROP TRIGGER IF EXISTS `after_tbl_units_update`;
DELIMITER //
CREATE TRIGGER `after_tbl_units_update` AFTER UPDATE ON `tbl_units`
 FOR EACH ROW BEGIN
   SET @action = 0;

   IF NEW.is_approved = 1 THEN

        IF NEW.category_id != 0 THEN
            INSERT INTO tbl_audit_log(action, client_id, legal_entity_id, tbl_auto_id, column_name, value, tbl_name)
            select 1, NEW.client_id, NEW.legal_entity_id, category_id, 'category_name' col_name, category_name value, 'tbl_categories' from tbl_categories
            where category_id = NEW.category_id;
        END IF;
        
        IF NEW.division_id != 0 THEN
            INSERT INTO tbl_audit_log(action, client_id, legal_entity_id, tbl_auto_id, column_name, value, tbl_name)
            select 1, NEW.client_id, NEW.legal_entity_id, division_id, 'division_name' col_name, division_name value, 'tbl_divisions' from tbl_divisions
            where division_id = NEW.division_id;
        END IF;


        INSERT INTO tbl_audit_log(action,
                             client_id,
                             legal_entity_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
            VALUES (@action,
                    NEW.client_id,
                    NEW.legal_entity_id,
                    NEW.unit_id,
                    'client_id',
                    NEW.client_id,
                    'tbl_units');


       INSERT INTO tbl_audit_log(action,
                                 client_id,
                                 legal_entity_id,
                                 tbl_auto_id,
                                 column_name,
                                 value,
                                 tbl_name)
            VALUES (@action,
                    NEW.client_id,
                    NEW.legal_entity_id,
                    NEW.unit_id,
                    'business_group_id',
                    NEW.business_group_id,
                    'tbl_units');

        INSERT INTO tbl_audit_log(action,
                                 client_id,
                                 legal_entity_id,
                                 tbl_auto_id,
                                 column_name,
                                 value,
                                 tbl_name)
            VALUES (@action,
                    NEW.client_id,
                    NEW.legal_entity_id,
                    NEW.unit_id,
                    'legal_entity_id',
                    NEW.legal_entity_id,
                    'tbl_units');

        INSERT INTO tbl_audit_log(action,
                                 client_id,
                                 legal_entity_id,
                                 tbl_auto_id,
                                 column_name,
                                 value,
                                 tbl_name)
            VALUES (@action,
                    NEW.client_id,
                    NEW.legal_entity_id,
                    NEW.unit_id,
                    'division_id',
                    NEW.division_id,
                    'tbl_units');

        INSERT INTO tbl_audit_log(action,
                                 client_id,
                                 legal_entity_id,
                                 tbl_auto_id,
                                 column_name,
                                 value,
                                 tbl_name)
            VALUES (@action,
                    NEW.client_id,
                    NEW.legal_entity_id,
                    NEW.unit_id,
                    'category_id',
                    NEW.category_id,
                    'tbl_units');

        INSERT INTO tbl_audit_log(action,
                                 client_id,
                                 legal_entity_id,
                                 tbl_auto_id,
                                 column_name,
                                 value,
                                 tbl_name)
            VALUES (@action,
                    NEW.client_id,
                    NEW.legal_entity_id,
                    NEW.unit_id,
                    'country_id',
                    NEW.country_id,
                    'tbl_units');

        INSERT INTO tbl_audit_log(action,
                                 client_id,
                                 legal_entity_id,
                                 tbl_auto_id,
                                 column_name,
                                 value,
                                 tbl_name)
        SELECT @action, new.client_id,
        NEW.legal_entity_id, new.unit_id, 'geography_name',
            parent_names, 'tbl_units' FROM tbl_geographies where geography_id = new.geography_id;


        INSERT INTO tbl_audit_log(action,
                                 client_id,
                                 legal_entity_id,
                                 tbl_auto_id,
                                 column_name,
                                 value,
                                 tbl_name)
            VALUES (@action,
                    NEW.client_id,
                    NEW.legal_entity_id,
                    NEW.unit_id,
                    'unit_code',
                    NEW.unit_code,
                    'tbl_units');


        INSERT INTO tbl_audit_log(action,
                                 client_id,
                                 legal_entity_id,
                                 tbl_auto_id,
                                 column_name,
                                 value,
                                 tbl_name)
            VALUES (@action,
                    NEW.client_id,
                    NEW.legal_entity_id,
                    NEW.unit_id,
                    'unit_name',
                    NEW.unit_name,
                    'tbl_units');


        INSERT INTO tbl_audit_log(action,
                                 client_id,
                                 legal_entity_id,
                                 tbl_auto_id,
                                 column_name,
                                 value,
                                 tbl_name)
            VALUES (@action,
                    NEW.client_id,
                    NEW.legal_entity_id,
                    NEW.unit_id,
                    'address',
                    NEW.address,
                    'tbl_units');


        INSERT INTO tbl_audit_log(action,
                                 client_id,
                                 legal_entity_id,
                                 tbl_auto_id,
                                 column_name,
                                 value,
                                 tbl_name)
            VALUES (@action,
                    NEW.client_id,
                    NEW.legal_entity_id,
                    NEW.unit_id,
                    'postal_code',
                    NEW.postal_code,
                    'tbl_units');


        UPDATE tbl_client_replication_status set is_new_data = 1
        WHERE client_id = NEW.client_id and is_group = 1;

        UPDATE tbl_client_replication_status set is_new_data = 1
        WHERE client_id = NEW.legal_entity_id and is_group = 0 ;

        INSERT INTO tbl_audit_log(action, client_id, legal_entity_id, tbl_auto_id, column_name, value, tbl_name)
        select @action, NEW.client_id, NEW.legal_entity_id, unit_org_id, 'unit_id' col_name, unit_id value, 'tbl_units_organizations' from tbl_units_organizations
        where unit_id = NEW.unit_id
        union all
        select @action, NEW.client_id, NEW.legal_entity_id, unit_org_id, 'domain_id' col_name, domain_id value, 'tbl_units_organizations' from tbl_units_organizations
        where unit_id = NEW.unit_id
        union all
        select @action, NEW.client_id, NEW.legal_entity_id, unit_org_id, 'organisation_id' col_name, organisation_id value, 'tbl_units_organizations' from tbl_units_organizations
        where unit_id = NEW.unit_id
        order by unit_org_id, col_name;

   END IF;

END
//
DELIMITER ;



-- -------------------
-- Triggers `tbl_compliances`
-- ---------------

DROP TRIGGER IF EXISTS `after_tbl_compliances_update`;
DELIMITER //
CREATE TRIGGER `after_tbl_compliances_update` AFTER UPDATE ON `tbl_compliances`
 FOR EACH ROW BEGIN
    SET @action = 0;
   IF NEW.is_approved = 2 or NEW.is_approved = 3 THEN
        INSERT INTO tbl_audit_log(action,
                             client_id,
                             legal_entity_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
      SELECT @action, 0, 0, NEW.compliance_id,
      'statutory_mapping', statutory_mapping,
      'tbl_compliances' FROM tbl_statutory_mappings
      WHERE statutory_mapping_id=NEW.statutory_mapping_id;

        INSERT INTO tbl_audit_log(action,
                                 client_id,
                                 legal_entity_id,
                                 tbl_auto_id,
                                 column_name,
                                 value,
                                 tbl_name)
            VALUES (@action,
                    0, 0,
                    NEW.compliance_id,
                    'statutory_mapping_id',
                    NEW.statutory_mapping_id,
                    'tbl_compliances');

        INSERT INTO tbl_audit_log(action,
                                 client_id,
                                 legal_entity_id,
                                 tbl_auto_id,
                                 column_name,
                                 value,
                                 tbl_name)
            VALUES (@action,
                    0, 0,
                    NEW.compliance_id,
                    'country_id',
                    NEW.country_id,
                    'tbl_compliances');

       INSERT INTO tbl_audit_log(action,
                                 client_id,
                                 legal_entity_id,
                                 tbl_auto_id,
                                 column_name,
                                 value,
                                 tbl_name)
            VALUES (@action,
                    0, 0,
                    NEW.compliance_id,
                    'domain_id',
                    NEW.domain_id,
                    'tbl_compliances');

        INSERT INTO tbl_audit_log(action,
                                 client_id,
                                 legal_entity_id,
                                 tbl_auto_id,
                                 column_name,
                                 value,
                                 tbl_name)
            VALUES (@action,
                    0, 0,
                    NEW.compliance_id,
                    'statutory_provision',
                    NEW.statutory_provision,
                    'tbl_compliances');


       INSERT INTO tbl_audit_log(action,
                                 client_id,
                                 legal_entity_id,
                                 tbl_auto_id,
                                 column_name,
                                 value,
                                 tbl_name)
            VALUES (@action,
                    0, 0,
                    NEW.compliance_id,
                    'compliance_task',
                    NEW.compliance_task,
                    'tbl_compliances');

        INSERT INTO tbl_audit_log(action,
                                 client_id,
                                 legal_entity_id,
                                 tbl_auto_id,
                                 column_name,
                                 value,
                                 tbl_name)
            VALUES (@action,
                    0, 0,
                    NEW.compliance_id,
                    'document_name',
                    NEW.document_name,
                    'tbl_compliances');

        INSERT INTO tbl_audit_log(action,
                                 client_id,
                                 legal_entity_id,
                                 tbl_auto_id,
                                 column_name,
                                 value,
                                 tbl_name)
            VALUES (@action,
                    0, 0,
                    NEW.compliance_id,
                    'compliance_description',
                    NEW.compliance_description,
                    'tbl_compliances');

        INSERT INTO tbl_audit_log(action,
                                 client_id,
                                 legal_entity_id,
                                 tbl_auto_id,
                                 column_name,
                                 value,
                                 tbl_name)
            VALUES (@action,
                    0, 0,
                    NEW.compliance_id,
                    'penal_consequences',
                    NEW.penal_consequences,
                    'tbl_compliances');

        INSERT INTO tbl_audit_log(action,
                                 client_id,
                                 legal_entity_id,
                                 tbl_auto_id,
                                 column_name,
                                 value,
                                 tbl_name)
            VALUES (@action,
                    0, 0,
                    NEW.compliance_id,
                    'reference_link',
                    NEW.reference_link,
                    'tbl_compliances');

       INSERT INTO tbl_audit_log(action,
                                 client_id,
                                 legal_entity_id,
                                 tbl_auto_id,
                                 column_name,
                                 value,
                                 tbl_name)
            VALUES (@action,
                    0, 0,
                    NEW.compliance_id,
                    'frequency_id',
                    NEW.frequency_id,
                    'tbl_compliances');

        INSERT INTO tbl_audit_log(action,
                                 client_id,
                                 legal_entity_id,
                                 tbl_auto_id,
                                 column_name,
                                 value,
                                 tbl_name)
            VALUES (@action,
                    0, 0,
                    NEW.compliance_id,
                    'statutory_dates',
                    NEW.statutory_dates,
                    'tbl_compliances');

       INSERT INTO tbl_audit_log(action,
                                 client_id,
                                 legal_entity_id,
                                 tbl_auto_id,
                                 column_name,
                                 value,
                                 tbl_name)
            VALUES (@action,
                    0, 0,
                    NEW.compliance_id,
                    'repeats_type_id',
                    NEW.repeats_type_id,
                    'tbl_compliances');


       INSERT INTO tbl_audit_log(action,
                                 client_id,
                                 legal_entity_id,
                                 tbl_auto_id,
                                 column_name,
                                 value,
                                 tbl_name)
            VALUES (@action,
                    0, 0,
                    NEW.compliance_id,
                    'duration_type_id',
                    NEW.duration_type_id,
                    'tbl_compliances');


       INSERT INTO tbl_audit_log(action,
                                 client_id,
                                 legal_entity_id,
                                 tbl_auto_id,
                                 column_name,
                                 value,
                                 tbl_name)
            VALUES (@action,
                    0, 0,
                    NEW.compliance_id,
                    'repeats_every',
                    NEW.repeats_every,
                    'tbl_compliances');


       INSERT INTO tbl_audit_log(action,
                                 client_id,
                                 legal_entity_id,
                                 tbl_auto_id,
                                 column_name,
                                 value,
                                 tbl_name)
            VALUES (@action,
                    0, 0,
                    NEW.compliance_id,
                    'duration',
                    NEW.duration,
                    'tbl_compliances');


       INSERT INTO tbl_audit_log(action,
                                 client_id,
                                 legal_entity_id,
                                 tbl_auto_id,
                                 column_name,
                                 value,
                                 tbl_name)
            SELECT @action, 0, 0, NEW.compliance_id,
               'statutory_nature', statutory_nature_name,
              'tbl_compliances' FROM tbl_statutory_natures
              WHERE statutory_nature_id in (
                select distinct statutory_nature_id from tbl_statutory_mappings where statutory_mapping_id = new.statutory_mapping_id
            );


       INSERT INTO tbl_audit_log(action,
                                 client_id,
                                 legal_entity_id,
                                 tbl_auto_id,
                                 column_name,
                                 value,
                                 tbl_name)
            VALUES (@action,
                    0, 0,
                    NEW.compliance_id,
                    'is_active',
                    NEW.is_active,
                    'tbl_compliances');

        INSERT INTO tbl_audit_log(action,
                                 client_id,
                                 legal_entity_id,
                                 tbl_auto_id,
                                 column_name,
                                 value,
                                 tbl_name)
            VALUES (@action,
                    0, 0,
                    NEW.compliance_id,
                    'status_changed_on',
                    NEW.status_changed_on,
                    'tbl_compliances');



       INSERT INTO tbl_audit_log(action,
                                 client_id,
                                 legal_entity_id,
                                 tbl_auto_id,
                                 column_name,
                                 value,
                                 tbl_name)
            VALUES (@action,
                    0, 0,
                    NEW.compliance_id,
                    'format_file',
                    NEW.format_file,
                    'tbl_compliances');


       INSERT INTO tbl_audit_log(action,
                                 client_id,
                                 legal_entity_id,
                                 tbl_auto_id,
                                 column_name,
                                 value,
                                 tbl_name)
            VALUES (@action,
                    0, 0,
                    NEW.compliance_id,
                    'format_file_size',
                    NEW.format_file_size,
                    'tbl_compliances');

        UPDATE tbl_client_replication_status set is_new_data = 1 where
        is_group = 0 and
        client_id in (select legal_entity_id from tbl_legal_entity_domains where domain_id = NEW.domain_id);
   END IF;

END
//
DELIMITER ;


DROP TRIGGER IF EXISTS `after_tbl_mapped_industries_insert`;
DELIMITER //
CREATE TRIGGER `after_tbl_mapped_industries_insert` AFTER INSERT ON `tbl_mapped_industries`
 FOR EACH ROW BEGIN
   SET @action = 0;
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             legal_entity_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                0,
                0,
                NEW.statutory_mapping_id,
                'organisation_id',
                NEW.organisation_id,
                'tbl_mapped_industries');


    UPDATE tbl_client_replication_status set is_new_data = 1 where
    is_group = 0 and
    client_id in (select distinct l.legal_entity_id from
        tbl_legal_entity_domains as l
        inner join tbl_statutory_mappings as s
        on s.domain_id = l.domain_id where s.statutory_mapping_id = NEW.statutory_mapping_id);
END
//
DELIMITER ;



-- ------------------
-- Triggers `tbl_client_statutories` `tbl_client_compliances`
-- -------------------
DROP TRIGGER IF EXISTS `after_tbl_client_statutories_update`;
DELIMITER //
CREATE TRIGGER `after_tbl_client_statutories_update` AFTER UPDATE ON `tbl_client_statutories`
 FOR EACH ROW BEGIN
    SET @action = 0;
    set @legal_entity_id = (select legal_entity_id from tbl_units where unit_id = new.unit_id limit 1);

    IF new.status = 3 then
        INSERT INTO tbl_audit_log(action,
                                 client_id,
                                 legal_entity_id,
                                 tbl_auto_id,
                                 column_name,
                                 value,
                                 tbl_name)
            VALUES (@action,
                    0,
                    @legal_entity_id,
                    NEW.client_statutory_id,
                    'unit_id',
                    NEW.unit_id,
                    'tbl_client_statutories');

        INSERT INTO tbl_audit_log(action,
                                 client_id,
                                 legal_entity_id,
                                 tbl_auto_id,
                                 column_name,
                                 value,
                                 tbl_name)
            VALUES (@action,
                    0,
                    @legal_entity_id,
                    NEW.client_statutory_id,
                    'domain_id',
                    new.domain_id,
                    'tbl_client_statutories');

        UPDATE tbl_client_replication_status set is_new_data = 1
        WHERE client_id = @legal_entity_id and is_group = 0;
    END IF ;

END
//
DELIMITER ;


DROP TRIGGER IF EXISTS `after_tbl_client_compliances_update`;
DELIMITER //
CREATE TRIGGER `after_tbl_client_compliances_update` AFTER UPDATE ON `tbl_client_compliances`
 FOR EACH ROW BEGIN
    SET @action = 0;

    IF new.is_submitted = 1 then
        INSERT INTO tbl_audit_log(action,
                                 client_id,
                                 legal_entity_id,
                                 tbl_auto_id,
                                 column_name,
                                 value,
                                 tbl_name)
            VALUES (@action,
                    0,
                    NEW.legal_entity_id,
                    NEW.client_compliance_id,
                    'legal_entity_id',
                    NEW.legal_entity_id,
                    'tbl_client_compliances');


        INSERT INTO tbl_audit_log(action,
                                 client_id,
                                 legal_entity_id,
                                 tbl_auto_id,
                                 column_name,
                                 value,
                                 tbl_name)
            VALUES (@action,
                    0,
                    new.legal_entity_id,
                    NEW.client_compliance_id,
                    'unit_id',
                    NEW.unit_id,
                    'tbl_client_compliances');


        INSERT INTO tbl_audit_log(action,
                                 client_id,
                                 legal_entity_id,
                                 tbl_auto_id,
                                 column_name,
                                 value,
                                 tbl_name)
            VALUES (@action,
                    0,
                    new.legal_entity_id,
                    NEW.client_compliance_id,
                    'domain_id',
                    NEW.domain_id,
                    'tbl_client_compliances');


        INSERT INTO tbl_audit_log(action,
                                 client_id,
                                 legal_entity_id,
                                 tbl_auto_id,
                                 column_name,
                                 value,
                                 tbl_name)
            VALUES (@action,
                    0,
                    new.legal_entity_id,
                    NEW.client_compliance_id,
                    'statutory_applicable_status',
                    NEW.statutory_applicable_status,
                    'tbl_client_compliances');


        INSERT INTO tbl_audit_log(action,
                                 client_id,
                                 legal_entity_id,
                                 tbl_auto_id,
                                 column_name,
                                 value,
                                 tbl_name)
            VALUES (@action,
                    0,
                    NEW.legal_entity_id,
                    NEW.client_compliance_id,
                    'remarks',
                    NEW.remarks,
                    'tbl_client_compliances');

        INSERT INTO tbl_audit_log(action,
                                 client_id,
                                 legal_entity_id,
                                 tbl_auto_id,
                                 column_name,
                                 value,
                                 tbl_name)
            VALUES (@action,
                    0,
                    NEW.legal_entity_id,
                    NEW.client_compliance_id,
                    'compliance_id',
                    NEW.compliance_id,
                    'tbl_client_compliances');

        INSERT INTO tbl_audit_log(action,
                                 client_id,
                                 legal_entity_id,
                                 tbl_auto_id,
                                 column_name,
                                 value,
                                 tbl_name)
            VALUES (@action,
                    0,
                    NEW.legal_entity_id,
                    NEW.client_compliance_id,
                    'compliance_applicable_status',
                    NEW.compliance_applicable_status,
                    'tbl_client_compliances');

        INSERT INTO tbl_audit_log(action,
                                 client_id,
                                 legal_entity_id,
                                 tbl_auto_id,
                                 column_name,
                                 value,
                                 tbl_name)
            VALUES (@action,
                    0,
                    NEW.legal_entity_id,
                    NEW.client_compliance_id,
                    'is_new',
                    1,
                    'tbl_client_compliances');


        INSERT INTO tbl_audit_log(action,
                                 client_id,
                                 legal_entity_id,
                                 tbl_auto_id,
                                 column_name,
                                 value,
                                 tbl_name)
            SELECT @action, 0, new.legal_entity_id, NEW.client_compliance_id,
              'statutory_name', case parent_names when '' then statutory_name else concat(parent_names, ' >> ', statutory_name) end as statutory_name,
              'tbl_client_compliances'
              FROM tbl_statutories
              WHERE statutory_id=NEW.statutory_id;

        UPDATE tbl_client_replication_status set is_new_data = 1
        WHERE client_id = NEW.legal_entity_id and is_group = 0;
    END IF ;

END
//
DELIMITER ;


--
-- Triggers `tbl_geographies`
--
DROP TRIGGER IF EXISTS `after_tbl_geographies_update`;
DELIMITER //
CREATE TRIGGER `after_tbl_geographies_update` AFTER UPDATE ON `tbl_geographies`
 FOR EACH ROW BEGIN
   SET @action = 1;

    IF OLD.parent_names <> NEW.parent_names THEN
        INSERT INTO tbl_audit_log(action,
                             client_id,
                             legal_entity_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        SELECT @action, @client_id := client_id, legal_entity_id,
        unit_id, 'geography', NEW.parent_names, 'tbl_units'
        FROM tbl_units WHERE geography_id=NEW.geography_id;

        UPDATE tbl_client_replication_status set is_new_data = 1
        WHERE client_id = @client_id and is_group = 1;
    END IF;

END
//
DELIMITER ;


-- Triggers `tbl_statutory_mappings`
--
DROP TRIGGER IF EXISTS `after_tbl_statutory_mappings_update`;
DELIMITER //
CREATE TRIGGER `after_tbl_statutory_mappings_update` AFTER UPDATE ON `tbl_statutory_mappings`
 FOR EACH ROW BEGIN
   SET @action = 1;
   IF OLD.statutory_mapping <> NEW.statutory_mapping THEN
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             legal_entity_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
  SELECT @action, 0,0, compliance_id, 'statutory_mapping', NEW.statutory_mapping, 'tbl_compliances'  FROM tbl_compliances WHERE statutory_mapping_id=NEW.statutory_mapping_id;
    UPDATE tbl_client_replication_status set is_new_data = 1 where
    is_group = 0 and
    client_id in (select distinct legal_entity_id from tbl_legal_entity_domains where domain_id = OLD.domain_id);
  END IF;
END
//
DELIMITER ;

--
-- Trigger after_tbl_countries_update
--


DROP TRIGGER IF EXISTS `after_tbl_countries_insert`;


DROP TRIGGER IF EXISTS `after_tbl_countries_update`;
DELIMITER //
CREATE TRIGGER `after_tbl_countries_update` AFTER UPDATE ON `tbl_countries`
 FOR EACH ROW BEGIN
   SET @action = 1;

   IF OLD.country_name <> NEW.country_name THEN
   INSERT INTO tbl_audit_log(action,
                            client_id,
                            legal_entity_id,
                            tbl_auto_id,
                            column_name,
                            value,
                            tbl_name)
        VALUES (@action,
                0, 0,
                NEW.country_id,
                'country_name',
                NEW.country_name,
                "tbl_countries"
                );
    END IF;
    UPDATE tbl_client_replication_status set is_new_data = 1 where
    client_id in (select distinct legal_entity_id from tbl_legal_entities where country_id = NEW.country_id) or
    client_id in (select distinct client_id from tbl_legal_entities where country_id = NEW.country_id);

END
//
DELIMITER ;

--
-- Trigger after_tbl_domains_update
--

DROP TRIGGER IF EXISTS `after_tbl_domains_update`;
DELIMITER //
CREATE TRIGGER `after_tbl_domains_update` AFTER UPDATE ON `tbl_domains`
 FOR EACH ROW BEGIN
   SET @action = 1;

   IF OLD.domain_name <> NEW.domain_name THEN
   INSERT INTO tbl_audit_log(action,
                            client_id,
                            legal_entity_id,
                            tbl_auto_id,
                            column_name,
                            value,
                            tbl_name)
        VALUES (@action,
                0,0,
                NEW.domain_id,
                'domain_name',
                NEW.domain_name,
                "tbl_domains"
                );
    UPDATE tbl_client_replication_status set is_new_data = 1 where
    client_id in (
        select distinct legal_entity_id from tbl_legal_entity_domains where domain_id = new.domain_id
    );
    END IF;
END
//
DELIMITER ;


--
-- Trigger after_tbl_statutories_update
--


DROP TRIGGER IF EXISTS `after_tbl_statutories_update`;
DELIMITER //
CREATE TRIGGER `after_tbl_statutories_update` AFTER UPDATE ON `tbl_statutories`
 FOR EACH ROW BEGIN
    SET @action = 1;
    IF NEW.parent_names = '' then
        set @name = new.statutory_name;
    ELSE
        set @name = concat(new.parent_names, ' >> ', new.statutory_name);
    ENd IF;

    -- updating statutory_name in client_compliance table
    IF OLD.statutory_name <> NEW.statutory_name THEN
        INSERT INTO tbl_audit_log(action,
                                 client_id,
                                 legal_entity_id,
                                 tbl_auto_id,
                                 column_name,
                                 value,
                                 tbl_name)
        SELECT @action, client_id, legal_entity_id,
            client_compliance_id,
            'statutory_name', @name,
            'tbl_client_compliances'
            FROM tbl_client_compliances
            WHERE statutory_id=NEW.statutory_id;

        UPDATE tbl_client_replication_status set is_new_data = 1 where
        is_group = 0 and
        client_id in (select distinct legal_entity_id from tbl_client_compliances
                      where statutory_id = new.statutory_id);

    END IF;

END //

DELIMITER ;

--
-- trigger for tbl_statutory_notifications
--

DROP TRIGGER IF EXISTS `after_tbl_statutory_notifications_insert`;
DELIMITER //
CREATE TRIGGER `after_tbl_statutory_notifications_insert` AFTER INSERT ON `tbl_statutory_notifications`
 FOR EACH ROW BEGIN

        INSERT INTO tbl_audit_log(action,
                                 client_id,
                                 legal_entity_id,
                                 tbl_auto_id,
                                 column_name,
                                 value,
                                 tbl_name)
        VALUES (0, 0, 0,
                NEW.notification_id,
                'notification_text',
                NEW.notification_text,
                'tbl_statutory_notifications');

        INSERT INTO tbl_audit_log(action,
                                 client_id,
                                 legal_entity_id,
                                 tbl_auto_id,
                                 column_name,
                                 value,
                                 tbl_name)
        VALUES (0,
                0,0,
                NEW.notification_id,
                'compliance_id',
                NEW.compliance_id,
                'tbl_statutory_notifications');



        INSERT INTO tbl_audit_log(action,
                                 client_id,
                                 legal_entity_id,
                                 tbl_auto_id,
                                 column_name,
                                 value,
                                 tbl_name)
        VALUES (0,
                0,0,
                NEW.notification_id,
                'created_by',
                NEW.created_by,
                'tbl_statutory_notifications');


        INSERT INTO tbl_audit_log(action,
                                 client_id,
                                 legal_entity_id,
                                 tbl_auto_id,
                                 column_name,
                                 value,
                                 tbl_name)
        VALUES (0,
                0,0,
                NEW.notification_id,
                'created_on',
                NEW.created_on,
                'tbl_statutory_notifications');

        UPDATE tbl_client_replication_status set is_new_data = 1 where
        is_group = 0 and
        client_id in (select distinct legal_entity_id from tbl_client_compliances
                      where compliance_id = new.compliance_id);

END //

DELIMITER ;


--
-- trigger for tbl_validity_date_settings
--


DROP TRIGGER IF EXISTS `after_tbl_validity_date_settings_insert`;
DELIMITER //
CREATE TRIGGER `after_tbl_validity_date_settings_insert` AFTER INSERT ON `tbl_validity_date_settings`
 FOR EACH ROW BEGIN
   SET @action = 0;
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             legal_entity_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                0,0,
                NEW.validity_date_id,
                'country_id',
                NEW.country_id,
                'tbl_validity_date_settings');

    INSERT INTO tbl_audit_log(action,
                             client_id,
                             legal_entity_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                0,0,
                NEW.validity_date_id,
                'domain_id',
                NEW.domain_id,
                'tbl_validity_date_settings');

    INSERT INTO tbl_audit_log(action,
                             client_id,
                             legal_entity_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                0,0,
                NEW.validity_date_id,
                'days',
                NEW.days,
                'tbl_validity_date_settings');

        UPDATE tbl_client_replication_status set is_new_data = 1
        WHERE  client_id  in (
            select distinct t1.legal_entity_id from tbl_legal_entities as t1
                inner join tbl_legal_entity_domains as t2 on t1.legal_entity_id = t2.legal_entity_id
                where t1.country_id = new.country_id and t2.domain_id = new.domain_id
        );


END
//
DELIMITER ;

DROP TRIGGER IF EXISTS `after_tbl_validity_date_settings_update`;
DELIMITER //
CREATE TRIGGER `after_tbl_validity_date_settings_update` AFTER UPDATE ON `tbl_validity_date_settings`
 FOR EACH ROW BEGIN
   SET @action = 1;
   SET @save = 0;
   IF OLD.country_id <> NEW.country_id THEN
   SET @save = 1;
   INSERT INTO tbl_audit_log(action,
                             client_id,
                             legal_entity_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                0,0,
                NEW.validity_date_id,
                'country_id',
                NEW.country_id,
                'tbl_validity_date_settings');
    END IF ;
    IF OLD.domain_id <> NEW.domain_id THEN
    INSERT INTO tbl_audit_log(action,
                             client_id,
                             legal_entity_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                0,0,
                NEW.validity_date_id,
                'domain_id',
                NEW.domain_id,
                'tbl_validity_date_settings');
    END IF;
    IF OLD.days <> NEW.days THEN

    INSERT INTO tbl_audit_log(action,
                             client_id,
                             legal_entity_id,
                             tbl_auto_id,
                             column_name,
                             value,
                             tbl_name)
        VALUES (@action,
                0,0,
                NEW.validity_date_id,
                'days',
                NEW.days,
                'tbl_validity_date_settings');

   END IF;

    IF @save = 1 THEN
        UPDATE tbl_client_replication_status set is_new_data = 1
        WHERE  client_id  in (
            select distinct t1.legal_entity_id from tbl_legal_entities as t1
                inner join tbl_legal_entity_domains as t2 on t1.legal_entity_id = t2.legal_entity_id
                where t1.country_id = new.country_id and t2.domain_id = new.domain_id
        );
    END IF;

END
//
DELIMITER ;

