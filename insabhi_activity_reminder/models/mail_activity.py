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

                body = f'''
                    Hello,<br/><br/>

                    This is a reminder regarding the activity
                    <b>{activity.summary or ""}</b>
                    with deadline <b>{activity.date_deadline}</b>.<br/><br/>

                    Document: <b>{record.display_name}</b><br/>
                    Assigned User: <b>{activity.user_id.name}</b><br/><br/>

                    <a href="{activity_link}">
                        Open Document
                    </a>
                '''

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