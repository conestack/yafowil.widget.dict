import $ from 'jquery';

import {DictWidget} from './widget.js';
import {register_array_subscribers} from './widget.js';

export * from './widget.js';

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
