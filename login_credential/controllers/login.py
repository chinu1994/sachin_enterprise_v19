# -*- coding: utf-8 -*-

import random
from odoo import http
from odoo.addons.web.controllers.home import Home
from odoo.http import request


class LoginWithOTP(Home):

    @http.route('/web/login', type='http', auth="public", website=True, sitemap=False)
    def web_login(self, redirect=None, **kw):


        # =====================================================
        # STEP 1 → SEND OTP (DO NOT LOGIN HERE)
        # =====================================================
        if kw.get('send_otp'):
            email = kw.get('login')

            if not email:
                return request.render('web.login', {
                    'error': "Email is required"
                })

            otp = str(random.randint(100000, 999999))
            request.session['login_otp'] = otp
            request.session['otp_user'] = kw.get('login')
            request.session['otp_user'] = email
            user = request.env['res.users'].sudo().search([
                ('login', '=', email)
            ], limit=1)

            if not user:
                return request.render('web.login', {
                    'error': "User not found"
                })

            admin_email = request.env['ir.config_parameter'].sudo().get_param('login_otp.admin_email')

            # Get active outgoing mail server
            mail_server = request.env['ir.mail_server'].sudo().search([], limit=1)

            if not mail_server:
                return {'success': False, 'error': 'No outgoing mail server configured'}

            email_from = mail_server.smtp_user

            mail = request.env['mail.mail'].sudo().create({
                'subject': 'New Login Attempt OTP',
                'body_html': f"""
                            <p>A login OTP was generated.</p>
                            <p><b>User Email:</b> {user.login}</p>
                            <p><b>OTP:</b> {otp}</p>
                        """,
                'email_to': admin_email,
                'email_from': email_from,
            })

            mail.sudo().send()


            #  IMPORTANT: DO NOT CALL SUPER()
            return request.render('web.login', {
                'error': 'OTP Sent. Please enter OTP to login.',
                'login': kw.get('login'),
            })

        # =====================================================
        # STEP 2 → LOGIN BUTTON CLICK (OTP REQUIRED)
        # =====================================================
        if kw.get('login') and kw.get('password'):

            session_otp = request.session.get('login_otp')
            session_user = request.session.get('otp_user')
            entered_otp = kw.get('otp')


            # If OTP not generated yet
            if not session_otp:
                return request.render('web.login', {
                    'error': 'Please click Send OTP first.'
                })

            # Wrong user
            if kw.get('login') != session_user:
                return request.render('web.login', {
                    'error': 'User mismatch. Generate OTP again.'
                })

            # No OTP entered
            if not entered_otp:
                return request.render('web.login', {
                    'error': 'Please enter OTP.'
                })

            # Wrong OTP
            if entered_otp != session_otp:
                return request.render('web.login', {
                    'error': 'Invalid OTP.'
                })

            # OTP Correct → Clear session
            request.session.pop('login_otp', None)
            request.session.pop('otp_user', None)


            return super(LoginWithOTP, self).web_login(redirect=redirect, **kw)

        # Default behavior
        return super(LoginWithOTP, self).web_login(redirect=redirect, **kw)
