This module does the following:

* Adds the ability to hide parent's name from the presentation of the partners' names according to the settings of the partners.

The function provided by this module is needed when you have to set up a child partner
(e.g. a branch office of a company) as an 'individual' due to how Odoo recognizes the
commercial partner (i.e. if a child partner is a 'company', the partner becomes the
commercial partner itself), and you do not want to show the parent's name in QWeb report
or website where the partner is referenced (if the child partner is an individual, Odoo
by default shows the parent's name preceding the child's name).
