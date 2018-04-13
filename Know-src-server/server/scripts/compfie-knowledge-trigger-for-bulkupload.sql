


CREATE TRIGGER `compfie_knowledge_new`.`tbl_units_organizations_AFTER_INSERT` 
AFTER INSERT ON `tbl_units_organizations` FOR EACH ROW
BEGIN

    SET @action = 0;

    IF (select is_approved from tbl_units where unit_id = NEW.unit_id) = 1 THEN

        INSERT INTO tbl_audit_log(action, client_id, legal_entity_id, tbl_auto_id, column_name, value, tbl_name)
        select @action, tbl_units.client_id, tbl_units.legal_entity_id, unit_org_id, 'unit_id' col_name, tbl_units_organizations.unit_id value, 'tbl_units_organizations' 
        from tbl_units_organizations 
        inner join tbl_units on tbl_units_organizations.unit_id = tbl_units.unit_id
        where tbl_units_organizations.unit_id = NEW.unit_id
        union all
        select @action, tbl_units.client_id, tbl_units.legal_entity_id, unit_org_id, 'domain_id' col_name, domain_id value, 'tbl_units_organizations' 
        from tbl_units_organizations
        inner join tbl_units on tbl_units_organizations.unit_id = tbl_units.unit_id
        where tbl_units_organizations.unit_id = NEW.unit_id
        union all
        select @action, tbl_units.client_id, tbl_units.legal_entity_id, unit_org_id, 'organisation_id' col_name, organisation_id value, 'tbl_units_organizations' 
        from tbl_units_organizations
        inner join tbl_units on tbl_units_organizations.unit_id = tbl_units.unit_id
        where tbl_units_organizations.unit_id = NEW.unit_id
        order by unit_org_id, col_name;
     END IF;        
END


CREATE TRIGGER `compfie_knowledge_new`.`tbl_compliances_AFTER_INSERT` AFTER INSERT ON `tbl_compliances` FOR EACH ROW
BEGIN
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


CREATE TRIGGER `compfie_knowledge_new`.`tbl_units_AFTER_INSERT` AFTER INSERT ON `tbl_units` FOR EACH ROW
BEGIN

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


CREATE TRIGGER `compfie_knowledge_new`.`tbl_client_statutories_AFTER_INSERT` AFTER INSERT ON `tbl_client_statutories` FOR EACH ROW
BEGIN

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


CREATE TRIGGER `compfie_knowledge_new`.`tbl_compliances_AFTER_INSERT` AFTER INSERT ON `tbl_compliances` FOR EACH ROW
BEGIN

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

CREATE TRIGGER `compfie_knowledge_new`.`tbl_statutory_mappings_AFTER_INSERT` AFTER INSERT ON `tbl_statutory_mappings` FOR EACH ROW
BEGIN

   SET @action = 1;
   -- IF OLD.statutory_mapping <> NEW.statutory_mapping THEN
   IF NEW.is_approved = 2 THEN
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
    client_id in (select distinct legal_entity_id from tbl_legal_entity_domains where domain_id = NEW.domain_id);
  END IF;
  
END


CREATE TRIGGER `compfie_knowledge_new`.`tbl_client_compliances_AFTER_INSERT` AFTER INSERT ON `tbl_client_compliances` FOR EACH ROW
BEGIN

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
