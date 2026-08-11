import { patch } from "@web/core/utils/patch";
import { WebClient } from "@web/webclient/webclient";

patch(WebClient.prototype, {
    _loadDefaultApp() {
        // Keep the theme home menu as the initial screen.
    },
});