
from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils.email_lib import sendmail
from frappe.utils import nowdate, cstr, flt, now, getdate, add_months,add_days,cint,nowdate,formatdate



@frappe.whitelist()
def generate_pin(PR, method):
	frappe.errprint("in the generate pin")
	frappe.errprint(PR.name)
	import string
	import random
	code=''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(6))
	frappe.db.sql("update `tabPurchase Receipt` set pin='%s' where name='%s'"%(code,PR.name))
	# PR.pin=code
	# PR.update({"pin":code})
	frappe.errprint(code)
	frappe.errprint("code")
	send_email(PR, method,code)



def send_email(PR, method,code):
	frappe.errprint(code)
	recipients=[]
	expiry_date=''
	customer=frappe.db.sql("""select email_id from `tabBuy Back Requisition` where name='%s' """%(PR.buy_back_requisition_ref),as_list=1,debug=1)
	if customer:
		recipients.append(cstr(customer[0][0]))
	recipient=frappe.db.sql("""select parent from `tabUserRole` where role in('MSE','Slot Cashier','Slot Representative')""",as_dict=1,debug=1)
	if recipient:
		for resp in recipient:
			recipients.append(resp['parent'])

	no_of_days=frappe.db.sql("""select value from `tabSingles` where field='no_of_days'""",as_dict=1,debug=1)
	if no_of_days:
		expiry_date=add_days(nowdate(),cint(no_of_days[0]['value']))
	frappe.errprint("recipients")
	frappe.errprint(recipients)
	if recipients:
		subject = "Voucher Generation"
		message ="""<h3>Dear </h3><p>Below PIN is generated against the device sold at Matrix store </p>
		<p>PIN:%s</p>
		<p>PIN Expiry Date:%s </p>
		<p>Kindly redeem the voucher before the expiry date.</p>
		<p>Thank You,</p>
		""" %(code,formatdate(expiry_date))
		sendmail(recipients, subject=subject, msg=message)	
	# recipients = frappe.db.get_value("", None, "send_notifications_to").split(",")






