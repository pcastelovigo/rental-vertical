# Part of rental-vertical See LICENSE file for full copyright and licensing details.
from odoo import api, models
from odoo.exceptions import UserError
from odoo.exceptions import Warning

#https://stackoverflow.com/questions/42950/get-the-last-day-of-the-month
import datetime
from datetime import timedelta
from dateutil.relativedelta import *
def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)
    return next_month - datetime.timedelta(days=next_month.day)


class ContractLine(models.Model):
    _inherit = "contract.line"

    def _prepare_invoice_line(self, move_form):
        def offday_calc(self, end, start):
            offday_count = 0

            for offday in self.sale_order_line_id.fixed_offday_ids:
                if start <= offday.date <= end:
                    offday_count = offday_count + 1
            for offday in self.sale_order_line_id.add_offday_ids:
                if start <= offday.date <= end:
                    offday_count = offday_count + 1
            return offday_count

        self.ensure_one()
        res = super(ContractLine, self)._prepare_invoice_line(move_form)

        if self.recurring_next_date:
            if self.recurring_next_date == self.date_start:
                start = self.date_start
            else:
                start = self.recurring_next_date

        if self.recurring_rule_type == "monthlylastday":
            if self.recurring_next_date:
                if self.recurring_next_date.month == self.date_end.month:
                    end = self.date_end
                else:
                    end = last_day_of_month(self.recurring_next_date)
         
                invoice_period = (end - start)
                offday_count = offday_calc(self,end,start)
                res.update({"quantity": self.sale_order_line_id.rental_qty * (invoice_period.days + 1 - offday_count),})

        elif self.recurring_rule_type == "weekly":
            if self.recurring_next_date:
                week_next_date = self.recurring_next_date.isocalendar()[1]
                week_end_date = self.date_end.isocalendar()[1]

                if week_next_date == week_end_date:
                    end = self.date_end
                else:
                    end = self.recurring_next_date + timedelta(days=(6 - self.recurring_next_date.weekday()))
                
                invoice_period = (end - start)
                offday_count = offday_calc(self,end,start)
                res.update({"quantity": self.sale_order_line_id.rental_qty * (invoice_period.days + 1 - offday_count),})

        elif self.recurring_rule_type == "monthly":
            if self.recurring_next_date:
                if self.recurring_next_date.month == self.date_end.month:
                    end = self.date_end
                else:
                    end = start + relativedelta(months=+1)

                invoice_period = (end - start)
                offday_count = offday_calc(self,end,start)
                res.update({"quantity": self.sale_order_line_id.rental_qty * (invoice_period.days - offday_count),}) #relativedelta ya cuenta los dias
                

        else:
            raise Warning('Module will calculate monthy last day only, insert values manually')

        return res