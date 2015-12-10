from protocol.common import FORM_ID
__all__ = [
	"frm", "Form", "Menu"
]

frm = EnumType("FORM_TYPE", [
	"IT", 
	"Knowledge",
	"Blah"
])

Form = RecordType("Form", [
	Filed("form_id", FORM_ID),
	Filed("form_name", Text)
])

Geography = RecordType("Geography",[fields...])

FormList = StaticArrayType(Form, 100)
FormListvector = VectorType(Form)

Menu = RecordType("Menu", [
	Field("masters", FormList),
	Field("masters2", FormListvector),
	Field("masters3", Maptype(Text50, Form)),
	Filed("geographies", Maptype(COUNTry_ID, VectorType(Geography)))
])