from protocol import (
    admin, clientadminsettings, clientmasters, clientreport,
    clienttransactions, clientuser, common, core, dashboard,
    general, knowledgemaster, knowledgereport, knowledgetransaction,
    login, technomasters, technoreports, technotransactions,
    mobileapi
)
from basics.validate import Validate
from basics.module import Module

def main():
    v = Validate(
        [
            Module(admin, "admin"),
            Module(clientadminsettings, "clientadminsettings"),
            Module(clientmasters, "clientmasters"),
            Module(clientreport, "clientreport"),
            Module(clienttransactions, "clienttransactions"),
            Module(clientuser, "clientuser"),
            Module(core, "core"),
            Module(dashboard, "dashboard"),
            Module(general, "general"),
            Module(knowledgemaster, "knowledgemaster"),
            Module(knowledgereport, "knowledgereport"),
            Module(knowledgetransaction, "knowledgetransaction"),
            Module(login, "login"),
            Module(technomasters, "technomasters"),
            Module(technoreports, "technoreports"),
            Module(technotransactions, "technotransactions"),
            Module(mobileapi, "mobileapi")
        ]
    )
    v.validate(globals())

if __name__ == "__main__":
    main()
