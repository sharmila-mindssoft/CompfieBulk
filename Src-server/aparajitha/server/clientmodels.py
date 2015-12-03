from aparajitha.misc.dates import *

__all__ = [
    "ServiceProvider"
]

class ServiceProvider(object):
    def __init__(self, clientId, serviceProviderId, serviceProviderName, address, 
                contractFrom, contractTo, contactPerson, contactNo, isActive) :
        self.clientId = clientId
        self.serviceProviderId =  serviceProviderId
        self.serviceProviderName =  serviceProviderName
        self.address =  address
        self.contractFrom =  contractFrom
        self.contractTo =  contractTo
        self.contactPerson =  contactPerson
        self.contactNo =  contactNo
        self.isActive = isActive if isActive != None else 1

    @classmethod
    def initializeWithRequest(self, request, serviceProviderId, clientId):
    	serviceProviderName = str(request["service_provider_name"])
    	address = str(request["address"])
    	contractFrom =  str(request["contract_from"])
    	contractTo =  str(request["contract_to"])
    	contactPerson =  str(request["contact_person"])
    	contactNo =  str(request["contact_no"])
    	contractFrom = datetimeToTimestamp(stringToDatetime(contractFrom))
    	contractTo = datetimeToTimestamp(stringToDatetime(contractTo))
    	return ServiceProvider(clientId, serviceProviderId, serviceProviderName, address, 
                contractFrom, contractTo, contactPerson, contactNo, None)

    def toStructure(self):
        return {
	        "service_provider_id": self.serviceProviderId,
	        "service_provider_name": self.serviceProviderName, 
	        "address": self.address,
	        "contract_from": self.contractFrom,
	        "contract_to": self.contractTo, 
	        "contact_person": self.contactPerson,
	        "contact_no": self.contactNo,
	        "is_active": self.isActive
    	}

    @classmethod
    def getList(self, db):
        servcieProviderList = []
        rows = db.getServiceProviders()
        for row in rows:
            serviceProviderId = int(row[0])
            serviceProviderName = row[1]
            address = row[2]
            contractFrom = datetimeToString(timestampToDatetime(row[3]))
            contractTo = datetimeToString(timestampToDatetime(row[4]))
            contactPerson = row[5]
            contactNo = row[6]
            isActive = row[7]
            serviceProvider = ServiceProvider(None, serviceProviderId, serviceProviderName, address, 
                contractFrom, contractTo, contactPerson, contactNo, isActive)
            servcieProviderList.append(serviceProvider.toStructure())
        return servcieProviderList