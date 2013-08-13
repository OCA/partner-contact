{ "name"         : "Partner Identification Numbers"
, "version"      : "0.2"
, "author"       : "ChriCar Beteiligungs- und Beratungs- GmbH"
, "website"      : "http://www.chricar.at/ChriCar"
, "description"  : """This module allows to manage all sort of identification numbers
and certificates which are assigned to a partner and vary from country to country

 * Commercial register
 * VAT ID (eventually)
 * fiscal ID's
 * membership numbers
 * ...

"""
, "category"     : "Generic Modules/Others"
, "depends"      : ["base"]
, "init_xml"     : []
, "demo"         : ["partner_id_number_demo.xml"]
, "update_xml"   : ["partner_id_number_view.xml", "security/ir.model.access.csv"]
#, "update_xml"   : ["partner_id_number_view.xml","security/ir.model.access.csv"]
, "auto_install" : False
, "installable"  : True
, 'application'  : False
}
