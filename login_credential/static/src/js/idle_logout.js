/** @odoo-module **/

import { registry } from "@web/core/registry";
import { session } from "@web/session";
import { browser } from "@web/core/browser/browser";
import { cookie } from "@web/core/browser/cookie";

let timeout = null;
let lastActivityTs = Date.now();
let lastLoggedActivityTs = 0;

const INACTIVE_TIME =60 * 60 * 1000; // 1 hour
const LOG_COOKIE_NAME = "auto_logout_log";
const LAST_ACTIVITY_LS_KEY = "odoo_last_activity_ts";



function readLog() {
    try {
        const raw = cookie.get(LOG_COOKIE_NAME);
        if (!raw) {
            return [];
        }
        const parsed = JSON.parse(decodeURIComponent(raw));
        return Array.isArray(parsed) ? parsed : [];
    } catch (e) {
        return [];
    }
}

function writeLogEntry(event, extra = {}) {
    const log = readLog();
    log.push({
        event, // "start" | "activity" | "logout"
        time: new Date().toISOString(),
        ...extra,
    });

    const trimmed = log.slice(-MAX_LOG_ENTRIES);

    try {
        cookie.set(
            LOG_COOKIE_NAME,
            encodeURIComponent(JSON.stringify(trimmed)),
            30 * 24 * 60 * 60
        );
    } catch (e) {
        console.warn("auto_logout_service: could not write log cookie", e);
    }
}

function exposeDebugHelper() {
    window.getAutoLogoutLog = () => {
        const log = readLog();
        console.table(log);
        return log;
    };
}

function resetTimer(fromOtherTab = false) {
    clearTimeout(timeout);
    lastActivityTs = Date.now();

    if (!fromOtherTab) {
        try {
            browser.localStorage.setItem(LAST_ACTIVITY_LS_KEY, String(lastActivityTs));
        } catch (e) {
        }
    }



    if (lastActivityTs - lastLoggedActivityTs > LOG_THROTTLE_MS) {
        lastLoggedActivityTs = lastActivityTs;
        writeLogEntry("activity", { tab: getTabId() });
    }

    timeout = setTimeout(logoutUser, INACTIVE_TIME);
}

function logoutUser() {
    const idleFor = Date.now() - lastActivityTs;
    writeLogEntry("logout", {
        tab: getTabId(),
        idle_ms: idleFor,
        reason: "inactivity_timeout",
    });
    browser.location.href = "/web/session/logout";
}





let _tabId = null;
function getTabId() {
    if (!_tabId) {
        _tabId = Math.random().toString(36).slice(2, 8);
    }
    return _tabId;
}





function listenForOtherTabsActivity() {
    window.addEventListener("storage", (ev) => {
        if (ev.key === LAST_ACTIVITY_LS_KEY && ev.newValue) {
            const ts = parseInt(ev.newValue, 10);
            if (!isNaN(ts) && ts > lastActivityTs) {
                resetTimer(true);
            }
        }
    });
}

function setupAutoLogout() {
    window.addEventListener("mousemove", () => resetTimer());
    window.addEventListener("keydown", () => resetTimer());
    window.addEventListener("click", () => resetTimer());
    window.addEventListener("scroll", () => resetTimer());

    listenForOtherTabsActivity();
    exposeDebugHelper();

    writeLogEntry("start", { tab: getTabId(), uid: session.uid });
    resetTimer();
}

registry.category("services").add("auto_logout_service", {
    start() {
        setupAutoLogout();
    },
});