import $ from 'jquery';

import {DictWidget} from './widget_bs5.js';
import {register_array_subscribers} from './widget_bs5.js';

export * from './widget_bs5.js';

$(function() {
    if (window.ts !== undefined) {
        ts.ajax.register(DictWidget.initialize, true);
    } else if (window.bdajax !== undefined) {
        bdajax.register(DictWidget.initialize, true);
    } else {
        DictWidget.initialize();
    }
    register_array_subscribers();
});
