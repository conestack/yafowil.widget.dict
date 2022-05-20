import $ from 'jquery';

import {DictWidget} from './widget.js';

export * from './widget.js';

$(function() {
    if (window.ts !== undefined) {
        ts.ajax.register(DictWidget.initialize, true);
    } else if (window.bdajax !== undefined) {
        bdajax.register(DictWidget.initialize, true);
    } else {
        DictWidget.initialize();
    }
    if (window.yafowil.array !== undefined) {
        $.extend(yafowil.array.hooks.add, {
            dictwidget_binder: DictWidget.initialize
        });
    }
});
