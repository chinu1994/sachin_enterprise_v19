/** @odoo-module **/

import { registry } from "@web/core/registry";
import { session } from "@web/session";
import { browser } from "@web/core/browser/browser";

let timeout = null;
const INACTIVE_TIME =60 * 60 * 1000; // 1 hour

function resetTimer() {
    clearTimeout(timeout);
    timeout = setTimeout(logoutUser, INACTIVE_TIME);
}

function logoutUser() {
    browser.location.href = "/web/session/logout";
}

function setupAutoLogout() {
    window.addEventListener("mousemove", resetTimer);
    window.addEventListener("keydown", resetTimer);
    window.addEventListener("click", resetTimer);
    window.addEventListener("scroll", resetTimer);

    resetTimer();
}

registry.category("services").add("auto_logout_service", {
    start() {
        setupAutoLogout();
    },
});
