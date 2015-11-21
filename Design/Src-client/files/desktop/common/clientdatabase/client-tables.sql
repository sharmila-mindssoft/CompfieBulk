DROP TABLE IF EXISTS tbl_statutories;
CREATE TABLE tbl_statutories (
  statutory_id int(11) NOT NULL,
  statutory_name varchar(50) DEFAULT NULL,
  level_id int(11) DEFAULT NULL,
  parent_ids longtext,
  is_active tinyint(4) DEFAULT '1',
  updated_on timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  updated_by int(11) DEFAULT NULL,
  PRIMARY KEY (statutory_id),
  KEY StatutoryLevels_idx (level_id)
);
DROP TABLE IF EXISTS tbl_compliances;
CREATE TABLE tbl_compliances (
  compliance_id int(11) NOT NULL,
  statutory_mapping varchar(500) DEFAULT NULL,
  statutory_provision varchar(250) DEFAULT NULL,
  compliance_task varchar(100) DEFAULT NULL,
  compliance_description longtext,
  document_name varchar(100) DEFAULT NULL,
  format_file varchar(100) DEFAULT NULL,
  penal_consequences longtext,
  compliance_frequency varchar(100) DEFAULT NULL,
  statutory_dates longtext,
  repeats_every varchar(100) DEFAULT NULL,
  repeats_type varchar(100) DEFAULT NULL,
  duration tinyint(4) DEFAULT NULL,
  duration_type varchar(50) DEFAULT NULL,
  statutory_mapping_id int(11) DEFAULT NULL,
  is_active tinyint(4) DEFAULT NULL,
  created_by int(11) DEFAULT NULL,
  created_on timestamp NULL DEFAULT NULL,
  updated_by int(11) DEFAULT NULL,
  updated_on timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (compliance_id)
);
DROP TABLE IF EXISTS tbl_countries;
CREATE TABLE tbl_countries (
  country_id int(11) NOT NULL,
  country_name varchar(50) DEFAULT NULL,
  is_active tinyint(4) DEFAULT '1',
  created_by int(11) DEFAULT NULL,
  created_on timestamp NULL DEFAULT NULL,
  updated_by int(11) DEFAULT NULL,
  updated_on timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (country_id)
);
DROP TABLE IF EXISTS tbl_domains;
CREATE TABLE tbl_domains (
  domain_id int(11) NOT NULL,
  domain_name varchar(50) NOT NULL,
  is_active tinyint(4) DEFAULT '1',
  created_by int(11) DEFAULT NULL,
  created_on timestamp NULL DEFAULT NULL,
  updated_by int(11) DEFAULT NULL,
  updated_on timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (domain_id)
);
DROP TABLE IF EXISTS tbl_industries;
CREATE TABLE tbl_industries (
  industry_id int(11) NOT NULL,
  industry_name varchar(50) DEFAULT NULL,
  is_active tinyint(4) DEFAULT '1',
  updated_on timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  updated_by int(11) DEFAULT NULL,
  PRIMARY KEY (industry_id)
);
DROP TABLE IF EXISTS tbl_service_providers;
CREATE TABLE tbl_service_providers (
  service_provider_id int(11) NOT NULL,
  service_provider_name varchar(50) DEFAULT NULL,
  address varchar(500) DEFAULT NULL,
  contract_from date DEFAULT NULL,
  contract_to date DEFAULT NULL,
  contact_person varchar(50) DEFAULT NULL,
  contact_no int(11) DEFAULT NULL,
  is_active tinyint(4) DEFAULT NULL,
  created_by int(11) DEFAULT NULL,
  created_on timestamp NULL DEFAULT NULL,
  updated_by int(11) DEFAULT NULL,
  updated_on timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (service_provider_id)
);
DROP TABLE IF EXISTS tbl_business_groups;
CREATE TABLE tbl_business_groups (
  business_group_id int(11) NOT NULL,
  business_group_name varchar(45) DEFAULT NULL,
  created_by int(11) DEFAULT NULL,
  created_on timestamp NULL DEFAULT NULL,
  updated_by int(11) DEFAULT NULL,
  updated_on timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (business_group_id)
);
DROP TABLE IF EXISTS tbl_client_groups;
CREATE TABLE tbl_client_groups (
  client_id int(11) NOT NULL,
  group_name varchar(50) DEFAULT NULL,
  domain_ids varchar(200) DEFAULT NULL,
  logo varchar(200) DEFAULT NULL,
  contract_from date DEFAULT NULL,
  contract_to date DEFAULT NULL,
  no_of_user_licence int(11) DEFAULT NULL,
  total_disk_space int(11) DEFAULT NULL,
  sms_notification tinyint(4) DEFAULT '0',
  is_active tinyint(4) DEFAULT '1',
  updated_by int(11) DEFAULT NULL,
  updated_on timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (client_id)
);
DROP TABLE IF EXISTS tbl_client_user_groups;
CREATE TABLE tbl_client_user_groups (
  user_group_id int(11) NOT NULL,
  user_group_name varchar(50) DEFAULT NULL,
  form_type int(11) DEFAULT NULL,
  form_ids longtext,
  is_active tinyint(4) DEFAULT '1',
  created_by int(11) DEFAULT NULL,
  created_on timestamp NULL DEFAULT NULL,
  updated_by int(11) DEFAULT NULL,
  updated_on timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (user_group_id)
);
DROP TABLE IF EXISTS tbl_client_settings;
CREATE TABLE tbl_client_settings (
  domain_ids varchar(250) NOT NULL,
  logo varchar(200) DEFAULT NULL,
  contract_from date DEFAULT NULL,
  contract_to date DEFAULT NULL,
  no_of_user_licence int(11) DEFAULT NULL,
  total_disk_space int(11) DEFAULT NULL,
  is_sms_subscribed tinyint(4) DEFAULT NULL,
  two_levels_of_approval tinyint(4) DEFAULT NULL,
  assignee_reminder int(11) DEFAULT NULL,
  escalation_reminder_In_advance int(11) DEFAULT NULL,
  escalation_reminder int(11) DEFAULT NULL,
  PRIMARY KEY (domain_ids)
);  
DROP TABLE IF EXISTS tbl_client_compliances;
CREATE TABLE tbl_client_compliances (
  client_compliance_id int(11) NOT NULL,
  statutory_id int(11) DEFAULT NULL,
  applicable varchar(500) DEFAULT NULL,
  not_applicable_remarks varchar(250) DEFAULT NULL,
  compliance_id int(11) DEFAULT NULL,
  compliance_applicable varchar(500) DEFAULT NULL,
  compliance_opted varchar(500) DEFAULT NULL,
  compliance_remarks varchar(250) DEFAULT NULL,
  updated_by int(11) DEFAULT NULL,
  updated_on timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  KEY fk_statutories_ccom_idx (statutory_id),
  CONSTRAINT fk_statutories_ccom FOREIGN KEY (statutory_id) REFERENCES tbl_statutories (statutory_id) ON DELETE NO ACTION ON UPDATE NO ACTION
);
DROP TABLE IF EXISTS tbl_geography_levels;
CREATE TABLE tbl_geography_levels (
  level_id int(11) NOT NULL,
  level_position int(11) DEFAULT NULL,
  level_name varchar(50) DEFAULT NULL,
  country_id int(11) DEFAULT NULL,
  is_active tinyint(4) DEFAULT '1',
  updated_on timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  updated_by int(11) DEFAULT NULL,
  PRIMARY KEY (level_id),
  KEY countries_idx (country_id),
  CONSTRAINT fk_countries_gl FOREIGN KEY (country_id) REFERENCES tbl_countries (country_id) ON DELETE NO ACTION ON UPDATE NO ACTION
);
DROP TABLE IF EXISTS tbl_geographies;
CREATE TABLE tbl_geographies (
  geography_id int(11) NOT NULL,
  geography_name varchar(45) DEFAULT NULL,
  level_id int(11) DEFAULT NULL,
  parent_ids varchar(500) DEFAULT NULL,
  is_active tinyint(4) DEFAULT '1',
  updated_on timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  updated_by int(11) DEFAULT NULL,
  PRIMARY KEY (geography_id),
  KEY GeographyLevels_idx (level_id),
  CONSTRAINT fk_geographylevels_geo FOREIGN KEY (level_id) REFERENCES tbl_geography_levels (level_id) ON DELETE NO ACTION ON UPDATE NO ACTION
);
DROP TABLE IF EXISTS tbl_legal_entities;
CREATE TABLE tbl_legal_entities (
  legal_entity_id int(11) NOT NULL,
  legal_entity_name varchar(100) DEFAULT NULL,
  business_group_id int(11) DEFAULT NULL,
  created_by int(11) DEFAULT NULL,
  created_on timestamp NULL DEFAULT NULL,
  updated_by int(11) DEFAULT NULL,
  updated_on timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (legal_entity_id),
  KEY fk_business_groups_le_idx (business_group_id),
  CONSTRAINT fk_business_groups_le FOREIGN KEY (business_group_id) REFERENCES tbl_business_groups (business_group_id) ON DELETE NO ACTION ON UPDATE NO ACTION
);
DROP TABLE IF EXISTS tbl_client_user_details;
CREATE TABLE tbl_client_user_details (
  user_id int(11) NOT NULL,
  email_id varchar(100) DEFAULT NULL,
  user_group_id int(11) DEFAULT NULL,
  employee_name varchar(50) DEFAULT NULL,
  employee_code varchar(50) DEFAULT NULL,
  contact_no int(11) DEFAULT NULL,
  seating_unit_id int(11) DEFAULT NULL,
  user_level int(11) DEFAULT NULL,
  country_ids varchar(250) DEFAULT NULL,
  domain_ids varchar(250) DEFAULT NULL,
  unit_ids longtext,
  is_admin tinyint(4) DEFAULT '0',
  is_service_provider tinyint(4) DEFAULT NULL,
  service_provider_id int(11) DEFAULT NULL,
  created_by int(11) DEFAULT NULL,
  created_on timestamp NULL DEFAULT NULL,
  updated_by int(11) DEFAULT NULL,
  updated_on timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (user_id),
  KEY fk_client_user_groups_cud_idx (user_group_id),
  KEY fk_service_provider_cud_idx (service_provider_id),
  CONSTRAINT fk_client_user_groups_cud FOREIGN KEY (user_group_id) REFERENCES tbl_client_user_groups (user_group_id) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT fk_service_provider_cud FOREIGN KEY (service_provider_id) REFERENCES tbl_service_providers (service_provider_id) ON DELETE NO ACTION ON UPDATE NO ACTION
);
DROP TABLE IF EXISTS tbl_divisions;
CREATE TABLE tbl_divisions (
  division_id int(11) NOT NULL,
  division_name varchar(100) DEFAULT NULL,
  legal_entity_id int(11) DEFAULT NULL,
  business_group_id int(11) DEFAULT NULL,
  created_by int(11) DEFAULT NULL,
  created_on timestamp NULL DEFAULT NULL,
  updated_by int(11) DEFAULT NULL,
  updated_on timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (division_id),
  KEY fk_legal_entities_div_idx (legal_entity_id),
  KEY fk_business_groups_div_idx (business_group_id),
  CONSTRAINT fk_business_groups_div FOREIGN KEY (business_group_id) REFERENCES tbl_business_groups (business_group_id) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT fk_legal_entities_div FOREIGN KEY (legal_entity_id) REFERENCES tbl_legal_entities (legal_entity_id) ON DELETE NO ACTION ON UPDATE NO ACTION
);
DROP TABLE IF EXISTS tbl_units;
CREATE TABLE tbl_units (
  unit_id int(11) NOT NULL,
  division_id int(11) DEFAULT NULL,
  legal_entity_id int(11) DEFAULT NULL,
  business_group_id int(11) DEFAULT NULL,
  country_id int(11) DEFAULT NULL,
  geography_id int(11) DEFAULT NULL,
  unit_code varchar(50) DEFAULT NULL,
  unit_name varchar(50) DEFAULT NULL,
  industry_id int(11) DEFAULT NULL,
  address varchar(500) DEFAULT NULL,
  postal_code int(11) DEFAULT NULL,
  domain_ids varchar(100) DEFAULT NULL,
  is_active tinyint(4) DEFAULT '1',
  created_by int(11) DEFAULT NULL,
  created_on timestamp NULL DEFAULT NULL,
  updated_by int(11) DEFAULT NULL,
  updated_on timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (unit_id),
  KEY fk_divisions_unit_idx (division_id),
  KEY fk_business_groups_unit_idx (business_group_id),
  KEY fk_legel_entities_unit_idx (legal_entity_id),
  KEY fk_countries_master_unit_idx (country_id),
  KEY fk_geographies_unit_idx (geography_id),
  KEY fk_industries_unit_idx (industry_id),
  CONSTRAINT fk_business_groups_unit FOREIGN KEY (business_group_id) REFERENCES tbl_business_groups (business_group_id) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT fk_countries_master_unit FOREIGN KEY (country_id) REFERENCES tbl_countries (country_id) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT fk_divisions_unit FOREIGN KEY (division_id) REFERENCES tbl_divisions (division_id) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT fk_geographies_unit FOREIGN KEY (geography_id) REFERENCES tbl_geographies (geography_id) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT fk_industries_unit FOREIGN KEY (industry_id) REFERENCES tbl_industries (industry_id) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT fk_legel_entities_unit FOREIGN KEY (legal_entity_id) REFERENCES tbl_legal_entities (legal_entity_id) ON DELETE NO ACTION ON UPDATE NO ACTION
);
DROP TABLE IF EXISTS tbl_notifications_log;
CREATE TABLE tbl_notifications_log (
  notification_id int(11) NOT NULL,
  notification_type varchar(20) DEFAULT NULL,
  country_id int(11) DEFAULT NULL,
  domain_id int(11) DEFAULT NULL,
  business_group_id int(11) DEFAULT NULL,
  legal_entity_id int(11) DEFAULT NULL,
  division_id int(11) DEFAULT NULL,
  unit_id int(11) DEFAULT NULL,
  statutory_provision varchar(250) DEFAULT NULL,
  compliance_id int(11) DEFAULT NULL,
  assignee int(11) DEFAULT NULL,
  concurrence_person int(11) DEFAULT NULL,
  approval_person int(11) DEFAULT NULL,
  notification_text longtext,
  extra_details longtext,
  updated_on timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (notification_id),
  KEY fk_countries_nl_idx (country_id),
  KEY fk_domains_nl_idx (domain_id),
  KEY fk_business_groups_nl_idx (business_group_id),
  KEY fk_legal_entities_nl_idx (legal_entity_id),
  KEY fk_divisions_nl_idx (division_id),
  KEY fk_units_nl_idx (unit_id),
  KEY fk_compliances_nl_idx (compliance_id),
  KEY fk_units_nl_as_idx (assignee),
  KEY fk_units_nl_cp_idx (concurrence_person),
  KEY fk_units_nl_ap_idx (approval_person),
  CONSTRAINT fk_business_groups_nl FOREIGN KEY (business_group_id) REFERENCES tbl_business_groups (business_group_id) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT fk_compliances_nl FOREIGN KEY (compliance_id) REFERENCES tbl_compliances (compliance_id) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT fk_countries_nl FOREIGN KEY (country_id) REFERENCES tbl_countries (country_id) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT fk_divisions_nl FOREIGN KEY (division_id) REFERENCES tbl_divisions (division_id) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT fk_domains_nl FOREIGN KEY (domain_id) REFERENCES tbl_domains (domain_id) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT fk_legal_entities_nl FOREIGN KEY (legal_entity_id) REFERENCES tbl_legal_entities (legal_entity_id) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT fk_units_nl FOREIGN KEY (unit_id) REFERENCES tbl_units (unit_id) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT fk_units_nl_ap FOREIGN KEY (approval_person) REFERENCES tbl_client_user_details (user_id) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT fk_units_nl_as FOREIGN KEY (assignee) REFERENCES tbl_client_user_details (user_id) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT fk_units_nl_cp FOREIGN KEY (concurrence_person) REFERENCES tbl_client_user_details (user_id) ON DELETE NO ACTION ON UPDATE NO ACTION
);
DROP TABLE IF EXISTS tbl_notification_user_log;
CREATE TABLE tbl_notification_user_log (
  notification_id int(11) NOT NULL,
  user_id int(11) DEFAULT NULL,
  read_status tinyint(4) DEFAULT NULL,
  updated_on timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  KEY fk_notifications_log_nul_idx (notification_id),
  KEY fk_user_details_nul_idx (user_id),
  CONSTRAINT fk_notifications_log_nul FOREIGN KEY (notification_id) REFERENCES tbl_notifications_log (notification_id) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT fk_user_details_nul FOREIGN KEY (user_id) REFERENCES tbl_client_user_details (user_id) ON DELETE NO ACTION ON UPDATE NO ACTION
);
DROP TABLE IF EXISTS tbl_client_configurations;
CREATE TABLE tbl_client_configurations (
  country_id int(11) DEFAULT NULL,
  domain_id int(11) DEFAULT NULL,
  period_from varchar(50) DEFAULT NULL,
  period_to varchar(50) DEFAULT NULL,
  created_by int(11) DEFAULT NULL,
  created_on timestamp NULL DEFAULT NULL,
  updated_by int(11) DEFAULT NULL,
  updated_on timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  KEY fk_countries_cc_idx (country_id),
  KEY fk_domain_master_Cc_idx (domain_id),
  CONSTRAINT fk_countries_cc FOREIGN KEY (country_id) REFERENCES tbl_countries (country_id) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT fk_domain_master_Cc FOREIGN KEY (domain_id) REFERENCES tbl_domains (domain_id) ON DELETE NO ACTION ON UPDATE NO ACTION
);
DROP TABLE IF EXISTS tbl_compliance_activity_log;
CREATE TABLE tbl_compliance_activity_log (
  compliance_activity_id int(11) NOT NULL,
  unit_id int(11) DEFAULT NULL,
  compliance_id int(11) DEFAULT NULL,
  activity_date date DEFAULT NULL,
  activity_status date DEFAULT NULL,
  compliance_status tinyint(4) DEFAULT NULL,
  remarks varchar(500) DEFAULT NULL,
  updated_on timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (compliance_activity_id),
  KEY fk_units_cal_idx (unit_id),
  KEY fk_compliancs_cal_idx (compliance_id),
  CONSTRAINT fk_compliancs_cal FOREIGN KEY (compliance_id) REFERENCES tbl_compliances (compliance_id) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT fk_units_cal FOREIGN KEY (unit_id) REFERENCES tbl_units (unit_id) ON DELETE NO ACTION ON UPDATE NO ACTION
);
DROP TABLE IF EXISTS tbl_client_users;
CREATE TABLE tbl_client_users (
  client_user_id int(11) NOT NULL,
  client_user_name varchar(50) DEFAULT NULL,
  client_user_group_id int(11) DEFAULT NULL,
  client_user_code varchar(50) DEFAULT NULL,
  contact_no int(11) DEFAULT NULL,
  user_level int(11) DEFAULT NULL,
  seating_unit_id int(11) DEFAULT NULL,
  email_id varchar(100) DEFAULT NULL,
  password varchar(50) DEFAULT NULL,
  unit_ids longtext,
  is_admin tinyint(4) DEFAULT '0',
  is_active tinyint(4) DEFAULT '1',
  updated_by int(11) DEFAULT NULL,
  updated_on timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (client_user_id),
  KEY fk_client_user_groups_cu_idx (client_user_group_id),
  KEY fk_units_cu_idx (seating_unit_id),
  CONSTRAINT fk_client_user_groups_cu FOREIGN KEY (client_user_group_id) REFERENCES tbl_client_user_groups (user_group_id) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT fk_units_cu FOREIGN KEY (seating_unit_id) REFERENCES tbl_units (unit_id) ON DELETE NO ACTION ON UPDATE NO ACTION
);
DROP TABLE IF EXISTS tbl_client_saved_statutories;
CREATE TABLE tbl_client_saved_statutories (
  client_id int(11) NOT NULL,
  assign_statutory_id int(11) DEFAULT NULL,
  country_id int(11) DEFAULT NULL,
  domain_id int(11) DEFAULT NULL,
  unit_ids varchar(250) DEFAULT NULL,
  client_compliance_id int(11) DEFAULT NULL,
  updated_by int(11) DEFAULT NULL,
  updated_on timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (client_id),
  KEY fk_countries_css_idx (country_id),
  KEY fk_domain_css_idx (domain_id),
  KEY fk_client_compliance_css_idx (client_compliance_id),
  CONSTRAINT fk_clientgroups_css FOREIGN KEY (client_id) REFERENCES tbl_client_groups (client_id) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT fk_countries_css FOREIGN KEY (country_id) REFERENCES tbl_countries (country_id) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT fk_domain_css FOREIGN KEY (domain_id) REFERENCES tbl_domains (domain_id) ON DELETE NO ACTION ON UPDATE NO ACTION
);
DROP TABLE IF EXISTS tbl_compliance_history;
CREATE TABLE tbl_compliance_history (
  compliance_history_id int(11) NOT NULL,
  unit_id int(11) DEFAULT NULL,
  compliance_id int(11) DEFAULT NULL,
  start_date date DEFAULT NULL,
  due_date date DEFAULT NULL,
  completion_date timestamp NULL DEFAULT NULL,
  documents longtext,
  validity_date date DEFAULT NULL,
  next_due_date date DEFAULT NULL,
  remarks varchar(500) DEFAULT NULL,
  completed_by int(11) DEFAULT NULL,
  completed_on timestamp NULL DEFAULT NULL,
  concurrence_status varchar(20) DEFAULT NULL,
  concurred_by int(11) DEFAULT NULL,
  concurred_on timestamp NULL DEFAULT NULL,
  approve_status varchar(20) DEFAULT NULL,
  approved_by int(11) DEFAULT NULL,
  approved_on timestamp NULL DEFAULT NULL,
  PRIMARY KEY (compliance_history_id),
  KEY fk_units_ch_idx (unit_id),
  KEY fk_compliances_ch_idx (compliance_id),
  KEY fk_client_users_ch_idx (completed_by,compliance_history_id),
  CONSTRAINT fk_client_user_ch FOREIGN KEY (completed_by) REFERENCES tbl_client_user_details (user_id) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT fk_compliances_ch FOREIGN KEY (compliance_id) REFERENCES tbl_compliances (compliance_id) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT fk_units_ch FOREIGN KEY (unit_id) REFERENCES tbl_units (unit_id) ON DELETE NO ACTION ON UPDATE NO ACTION
);  
DROP TABLE IF EXISTS tbl_client_statutories;
CREATE TABLE tbl_client_statutories (
  client_id int(11) NOT NULL,
  assign_statutory_id int(11) DEFAULT NULL,
  country_id int(11) DEFAULT NULL,
  domain_id int(11) DEFAULT NULL,
  unit_id int(11) DEFAULT NULL,
  client_compliance_id int(11) DEFAULT NULL,
  updated_by int(11) DEFAULT NULL,
  updated_on timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (client_id),
  KEY fk_countries_cs_idx (country_id),
  KEY fk_domains_master_cs_idx (domain_id),
  KEY fk_units_cs_idx (unit_id),
  CONSTRAINT fk_client_groups_cs FOREIGN KEY (client_id) REFERENCES tbl_client_groups (client_id) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT fk_countries_cs FOREIGN KEY (country_id) REFERENCES tbl_countries (country_id) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT fk_domains_master_cs FOREIGN KEY (domain_id) REFERENCES tbl_domains (domain_id) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT fk_units_cs FOREIGN KEY (unit_id) REFERENCES tbl_units (unit_id) ON DELETE NO ACTION ON UPDATE NO ACTION
);
DROP TABLE IF EXISTS tbl_reassigned_compliances_history;
CREATE TABLE tbl_reassigned_compliances_history (
  unit_id int(11) NOT NULL,
  compliance_id int(11) DEFAULT NULL,
  assignee int(11) DEFAULT NULL,
  reassigned_from int(11) DEFAULT NULL,
  reassigned_date date DEFAULT NULL,
  remarks varchar(500) DEFAULT NULL,
  created_by int(11) DEFAULT NULL,
  created_on timestamp NULL DEFAULT NULL,
  updated_by int(11) DEFAULT NULL,
  updated_on timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  KEY fk_units_rch_idx (unit_id),
  KEY fk_compliances_rch_idx (compliance_id),
  KEY fk_client_user_as_rch_idx (assignee),
  KEY fk_client_user_rf_rch_idx (reassigned_from),
  CONSTRAINT fk_client_user_as_rch FOREIGN KEY (assignee) REFERENCES tbl_client_user_details (user_id) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT fk_client_user_rf_rch FOREIGN KEY (reassigned_from) REFERENCES tbl_client_user_details (user_id) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT fk_compliances_rch FOREIGN KEY (compliance_id) REFERENCES tbl_compliances (compliance_id) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT fk_units_rch FOREIGN KEY (unit_id) REFERENCES tbl_units (unit_id) ON DELETE NO ACTION ON UPDATE NO ACTION
);
DROP TABLE IF EXISTS tbl_assigned_compliances;
CREATE TABLE tbl_assigned_compliances (
  country_id int(11) NOT NULL,
  unit_id int(11) DEFAULT NULL,
  compliance_id int(11) DEFAULT NULL,
  trigger_before_days longtext,
  due_date date DEFAULT NULL,
  validity_date date DEFAULT NULL,
  assignee int(11) DEFAULT NULL,
  concurrence_person int(11) DEFAULT NULL,
  approval_person int(11) DEFAULT NULL,
  is_reassigned tinyint(4) DEFAULT NULL,
  is_active tinyint(4) DEFAULT NULL,
  created_by int(11) DEFAULT NULL,
  created_on timestamp NULL DEFAULT NULL,
  updated_by int(11) DEFAULT NULL,
  updated_on timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  KEY fk_countries_as_idx (country_id),
  KEY fk_units_as_idx (unit_id),
  KEY fk_compliance_as_idx (compliance_id),
  KEY fk_client_user_as_as_idx (assignee),
  KEY fk_client_user_as_con_idx (concurrence_person),
  KEY fk_client_user_as_ap_idx (approval_person),
  CONSTRAINT fk_client_user_as_ap FOREIGN KEY (approval_person) REFERENCES tbl_client_user_details (user_id) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT fk_client_user_as_as FOREIGN KEY (assignee) REFERENCES tbl_client_user_details (user_id) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT fk_client_user_as_con FOREIGN KEY (concurrence_person) REFERENCES tbl_client_user_details (user_id) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT fk_compliance_as FOREIGN KEY (compliance_id) REFERENCES tbl_compliances (compliance_id) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT fk_countries_as FOREIGN KEY (country_id) REFERENCES tbl_countries (country_id) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT fk_units_as FOREIGN KEY (unit_id) REFERENCES tbl_units (unit_id) ON DELETE NO ACTION ON UPDATE NO ACTION
);