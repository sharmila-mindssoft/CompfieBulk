var BusinessGroupName = $(".business-group-name");
var BusinessGroupSelect = $(".business-group-select");
var LegalEntityName = $(".legal-entity-name");
var LegalEntitySelect = $(".legal-entity-select");
var FType = $(".frequency-type");
var Domain = $(".domain");

var ShowUnitButton = $(".show-unit-button");

var SearchUnit = $(".search-unit");
var SearchUnitCheckBox = $(".search-unit-selectall");

var UnitList = $(".unit-list"); 
var UnitList_li = $(".unit-list li"); 

var NextButton = $("#next-button");
var PreviousButton = $("#previous-button");
var SaveButton = $("#save-button");
var SubmitButton = $("#submit-button");

var le_id = null;

var r_s_page = null;


PageControls = function() {

}

ReviewSettingsPage = function () {
    this._TypeList = [];
    this._DomainList = [];
    this._UnitList = [];
    this._ComplianceList = [];
}

ReviewSettingsPage.prototype.showLegalEntity = function (){    
    var t_this = this;
    var userLegalentity = user.entity_info;
    if(userLegalentity.length > 1){
        BusinessGroupName.hide();
        BusinessGroupSelect.show();
        LegalEntityName.hide();
        LegalEntitySelect.show();
        var select = '<option value="">Select</option>';
        $.each(user.entity_info, function(k, val){
            select = select + '<option value="' + val["le_id"] + '"> ' + val["le_name"] + ' </option>';
        });        
        LegalEntitySelect.html(select);
        LegalEntitySelect.on("change", function(){
            t_this.showTypeDomainList();
        });
    }else{
        BusinessGroupSelect.hide();
        BusinessGroupName.show();
        LegalEntitySelect.hide();
        LegalEntityName.show();
        LegalEntityName.text(userLegalentity[0]["le_name"]);
        BusinessGroupName.text(userLegalentity[0]["bg_name"]);
        le_id = userLegalentity[0]["le_id"]
        t_this.showTypeDomainList();
    }
}

ReviewSettingsPage.prototype.showTypeDomainList = function(){
    t_this = this;
    client_mirror.getReviewSettingsFilters(le_id, function(error, response) {
        if (error == null) {
            t_this._TypeList = response.type_list;
            t_this.__DomainList = response.domain_list;
            t_this.renderDomainList(t_this.__DomainList);
            t_this.renderTypeList(t_this._TypeList);
        } else {
            t_this.possibleFailures(error);
        }
    });
}

ReviewSettingsPage.prototype.possibleFailures = function(error) {
    if (error == "UserGroupNameAlreadyExists") {
        displayMessage(message.domainname_required);
    } else if (error == 'InvalidUserGroupId') {
        displayMessage(message.invalid_usergroupid);
    } else if (error == 'InvalidPassword') {
        displayMessage(message.invalid_password);
    } else {
        displayMessage(error);
    }
};

ReviewSettingsPage.prototype.renderDomainList = function(data) {
     Domain.empty()
}

ReviewSettingsPage.prototype.renderTypeList = function(data) {
     FType.empty()
}


r_s_page = new ReviewSettingsPage();

$(document).ready(function() {
    PageControls();    
    r_s_page.showLegalEntity();
    r_s_page.showTypeDomainList();
});
