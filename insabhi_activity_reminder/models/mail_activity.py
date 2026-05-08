# -*- coding: utf-8 -*-

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)

class MailActivity(models.Model):
    _inherit = 'mail.activity'

    reminder_mail_sent = fields.Boolean(
        string='Reminder Mail Sent',
        default=False,
    )

    @api.model
    def cron_activity_followers_reminder(self):
        """
        Send reminder email to all chatter followers
        when activity deadline date is reached.
        """

        today = fields.Date.today()

        activities = self.search([
            ('date_deadline', '=', today),
            ('reminder_mail_sent', '=', False),
        ])

        _logger.info(
            'Activity Followers Reminder Cron Started. Activities Found: %s',
            len(activities)
        )

        for activity in activities:
            try:
                if not activity.res_model or not activity.res_id:
                    continue

                record = self.env[activity.res_model].browse(activity.res_id)

                if not record.exists():
                    continue

                followers = record.message_partner_ids.filtered(lambda p: p.email)

                if not followers:
                    continue

                activity_link = f'/web#id={record.id}&model={record._name}&view_type=form'

                body = f"""
                           <div style="font-family: Arial, sans-serif;
                                       font-size:14px;
                                       color:#333;">

                               <p>Hello,</p>

                               <p>
                                   This is a reminder that an activity deadline
                                   has been reached.
                               </p>

                               <table cellpadding="5" cellspacing="0" border="0">

                                   <tr>
                                       <td><b>Document:</b></td>
                                       <td>{record.display_name}</td>
                                   </tr>

                                   <tr>
                                       <td><b>Activity:</b></td>
                                       <td>{activity.summary or ''}</td>
                                   </tr>

                                   <tr>
                                       <td><b>Deadline:</b></td>
                                       <td>{activity.date_deadline}</td>
                                   </tr>

                                   <tr>
                                       <td><b>Assigned To:</b></td>
                                       <td>{activity.user_id.name}</td>
                                   </tr>

                               </table>

                               <br/>

                               <a href="{activity_link}"
                                  style="
                                       background-color:#875A7B;
                                       color:white;
                                       padding:10px 15px;
                                       text-decoration:none;
                                       border-radius:4px;
                                       display:inline-block;
                                  ">
                                   Open Document
                               </a>

                               <br/><br/>

                               <p>Thank you.</p>

                           </div>
                       """

                mail_values = {
                    'subject': f'Reminder: Activity {activity.summary} is due',
                    'body_html': body,
                    'email_to': ','.join(followers.mapped('email')),
                }

                self.env['mail.mail'].create(mail_values).send()

                activity.reminder_mail_sent = True

                _logger.info(
                    'Reminder mail sent for activity ID %s',
                    activity.id
                )

            except Exception as e:
                _logger.exception(
                    'Error sending reminder for activity ID %s : %s',
                    activity.id,
                    str(e)
                )